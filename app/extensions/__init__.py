def setup_extension(app):
    from .babel import init_babel

    # inisialisasi babel
    init_babel(app)