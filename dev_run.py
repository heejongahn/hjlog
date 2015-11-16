from hjlog import app
import os

basedir = os.path.abspath(os.path.dirname(__file__))
if __name__ == '__main__':
    os.environ['DATABASE_URL'] = (
            'sqlite:///' + os.path.join(basedir, 'hjlog.db') +
            '?check_same_thread=False')

    app.run(host='0.0.0.0', debug=True)
