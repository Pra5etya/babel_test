def setup_cli(app): 
    from .register import register_translate_cli

    # inisialisasi translate cli
    register_translate_cli(app)