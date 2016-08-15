from flask import render_template


def register(app):
    @app.route('/')
    def about():
        return render_template('about.html')

    @app.route('/.well-known/acme-challenge/<tmp>')
    def letsencrpyt(tmp):
        with open('.well-known/acme-challenge/{}'.format(tmp)) as f:
            answer = f.readline().strip()

        return answer
