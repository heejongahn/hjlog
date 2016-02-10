from flask import render_template

def register(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', code=404), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('error.html', code=405), 405

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', code=500), 500
