# -*- coding:utf-8 -*-


from flask_script.commands import ShowUrls, Clean, Shell
from flask_script import Manager
from flask_migrate import MigrateCommand
from apps import config, commands
from apps.main import app_factory

manager = Manager(app_factory)
manager.add_option("-n", "--name", dest="app_name", required=False, default=config.project_name)
manager.add_option("-c", "--config", dest="config", required=False, default=config.Dev)

manager.add_command('shell', Shell())
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())

manager.add_command("db", MigrateCommand)

manager.add_command("test", commands.Test())
manager.add_command("create_db", commands.CreateDB())
manager.add_command("drop_db", commands.DropDB())

if __name__ == "__main__":
    manager.run()