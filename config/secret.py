import os

def setup_secret(app):
    from config.translate import LANGS

    BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # dir to root project
    TRANS_DIR = os.path.join(BASEDIR, "translations")  # dir to translations

    app.config.update(
        # Secret
        SECRET_KEY = "your-secret-key",                     # secret key

        # Babel
        BABEL_DEFAULT_LOCALE = "en",                        # default language
        BABEL_SUPPORTED_LOCALES = LANGS,                    # supported language
        BABEL_TRANSLATION_DIRECTORIES = TRANS_DIR,          # get babel translations
        BABEL_DEFAULT_TIMEZONE = "UTC",                     # default timezone
        BABEL_DEFAULT_DOMAIN = "messages",                  # default .po & .mo file name
    )
