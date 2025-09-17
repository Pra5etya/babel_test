def setup_secret(app): 

    from config.translate import LANGS

    app.config.update(
        SECRET_KEY="your-secret-key",
        BABEL_DEFAULT_LOCALE="en",
        BABEL_SUPPORTED_LOCALES=LANGS
    )