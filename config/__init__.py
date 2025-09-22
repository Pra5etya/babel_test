def register_config(app): 
    # 2.1 log setup
    # =================
    from config.logger import setup_logger

    logger = setup_logger()


    import os
    
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':   # log dimulai ketika restart
        boundary = "="  * 30

        logger.info(f"{boundary} LOGGER STARTING POINT {boundary} \n")
        logger.info("Flask is restarting...")
        logger.info("Log Start ... \n")

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