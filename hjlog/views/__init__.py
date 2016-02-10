def init_app(app):
    from .main import register; register(app)
    from .login import register; register(app)
    from .post import register; register(app)
    from .photo import register; register(app)
    from .error import register; register(app)
