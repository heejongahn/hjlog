from hjlog import app
import os

from hjlog import db
from hjlog.models import User

db.drop_all()
db.create_all()

u = User()
u.username = 'admin'
u.password = 'supersecret'

db.session.add(u)
db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
