def setup_extension(app):
    from .babel import init_babel

    app.config["BABEL_DEFAULT_LOCALE"] = "en"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"

    # inisialisasi babel
    init_babel(app)