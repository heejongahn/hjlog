from hjlog import app
import os

basedir = os.path.abspath(os.path.dirname(__file__))
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
