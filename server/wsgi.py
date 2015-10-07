# coding:utf-8

from apps.main import app_factory
from apps import config

app = app_factory(config.Config, config.project_name)