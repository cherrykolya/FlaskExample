import os
from app import create_app, db
from app.models import User, Role
#from flask_script import Manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

if __name__ == '__main__':
    app.run()

