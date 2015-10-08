# -*- coding: utf-8 -*-

from __future__ import absolute_import
from datetime import datetime
from flask.ext.sqlalchemy import BaseQuery
import simplejson
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.types import TEXT, UserDefinedType, TypeDecorator


__all_mixins = ['IdMixin', 'TimestampMixin', 'PermissionMixin', 'UrlForMixin',
    'BaseMixin']


class Query(BaseQuery):
    """
    Extends flask.ext.sqlalchemy.BaseQuery to add additional helper methods.
    """
    def one_or_none(self):
        """
        Like :meth:`one` but returns None if no results are found. Raises an exception
        if multiple results are found.
        """
        try:
            return self.one()
        except NoResultFound:
            return None

    def notempty(self):
        """
        Returns the equivalent of ``bool(query.count())`` but using an efficient
        SQL EXISTS function, so the database stops counting after the first result
        is found.
        """
        return self.session.query(self.exists()).first()[0]

    def isempty(self):
        """
        Returns the equivalent of ``not bool(query.count())`` but using an efficient
        SQL EXISTS function, so the database stops counting after the first result
        is found.
        """
        return not self.session.query(self.exists()).first()[0]


class IdMixin(object):
    """
    Provides the :attr:`id` primary key column
    """
    query_class = Query
    #: Database identity for this model, used for foreign key
    #: references from other models
    id = Column(Integer, primary_key=True)


def make_timestamp_columns():
    return (
        Column('created_at', DateTime, default=datetime.utcnow, nullable=False),
        Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False),
        )


class TimestampMixin(object):
    """
    Provides the :attr:`created_at` and :attr:`updated_at` audit timestamps
    """
    #: Timestamp for when this instance was created, in UTC
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    #: Timestamp for when this instance was last updated (via the app), in UTC
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class PermissionMixin(object):
    """
    Provides the :meth:`permissions` method used by BaseMixin and derived classes
    """
    def permissions(self, user, inherited=None):
        """
        Return permissions available to the given user on this object
        """
        if inherited is not None:
            return set(inherited)
        else:
            return set()


class UrlForMixin(object):
    """
    Provides a placeholder :meth:`url_for` method used by BaseMixin-derived classes
    """
    def url_for(self, action='view', **kwargs):
        """
        Return public URL to this instance for a given action (default 'view')
        """
        return None


class BaseMixin(IdMixin, TimestampMixin, PermissionMixin, UrlForMixin):
    """
    Base mixin class for all tables that adds id and timestamp columns and includes
    stub :meth:`permissions` and :meth:`url_for` methods
    """
    def _set_fields(self, fields):
        for f in fields:
            if hasattr(self, f):
                setattr(self, f, fields[f])
            else:
                raise TypeError("'{arg}' is an invalid argument for {instance_type}".format(arg=f, instance_type=self.__class__.__name__))


# --- Column types ------------------------------------------------------------

__all_columns = ['JsonDict']


class JsonType(UserDefinedType):
    """The PostgreSQL JSON type."""

    def get_col_spec(self):
        return "JSON"


class JsonbType(UserDefinedType):
    """The PostgreSQL JSONB type."""

    def get_col_spec(self):
        return "JSONB"


# Adapted from http://docs.sqlalchemy.org/en/rel_0_8/orm/extensions/mutable.html#establishing-mutability-on-scalar-column-values

class JsonDict(TypeDecorator):
    """
    Represents a JSON data structure. Usage::
        column = Column(JsonDict)
    """

    impl = TEXT

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            version = tuple(dialect.server_version_info[:2])
            if version in [(9, 2), (9, 3)]:
                return dialect.type_descriptor(JsonType)
            elif version >= (9, 4):
                return dialect.type_descriptor(JsonbType)
        return dialect.type_descriptor(self.impl)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = simplejson.dumps(value, default=lambda o: unicode(o))
        return value

    def process_result_value(self, value, dialect):
        if value is not None and isinstance(value, basestring):
            # Psycopg2 >= 2.5 will auto-decode JSON columns, so
            # we only attempt decoding if the value is a string.
            # Since this column stores dicts only, processed values
            # can never be strings.
            value = simplejson.loads(value, use_decimal=True)
        return value


__all__ = __all_mixins + __all_columns