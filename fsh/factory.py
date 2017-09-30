from flask import Flask


def create_app(config=None):
    app = Flask('fsh')
    app.config.from_object('fsh.config')
    app.config.update(config or {})

    register_db(app)
    register_cli(app)
    register_blueprints(app)

    return app


def register_db(app):
    from .models import db
    db.init_app(app)


def register_blueprints(app):
    import fsh.blueprints.api
    app.register_blueprint(fsh.blueprints.api.bp)


def register_cli(app):

    @app.cli.command("initdb")
    def init_db():
        from .models import db
        import fsh.models.models  # make sure all models are imported
        db.create_all()

    @app.cli.command("prepopulate")
    def prepopulate():
        from .models.models import Category, Product, db
        c = Category(name="Backwaren")
        p = Product(name="Brot", category=c)
        db.session.add(c)
        db.session.commit()
