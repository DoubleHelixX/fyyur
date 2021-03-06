# ----------------------------------------------------------------------------#
# * Migration Imports
# ----------------------------------------------------------------------------#
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

# ----------------------------------------------------------------------------#
# * Manage Migration
# ----------------------------------------------------------------------------#
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


#   ?----------------------------------------------------------------------------#
#   ?                               OPTIONAL
#   ?                      Localize Migration setup
#   ?----------------------------------------------------------------------------#

# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager

# #----------------------------------------------------------------------------#
# # Manage Migration
# #----------------------------------------------------------------------------#
# def migration(app,db):
#     migrate = Migrate(app, db)
#     manager = Manager(app)
#     manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
else:
    print('Something Went Wrong. __name__ != __main__')


