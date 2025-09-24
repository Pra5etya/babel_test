def register_config(app): 
    # 2.1 log setup
    # =================
    from config.logger import setup_logger

    setup_logger()    

    # 2.2 Secret setup
    # =================
    from config.secret import setup_secret

    setup_secret(app)
    

    # 2.3 Extension setup
    # =================
    from app.extensions import setup_extension

    setup_extension(app)


    # 2.4 CLI setup
    # =================
    from app.cli import setup_cli

    setup_cli(app)