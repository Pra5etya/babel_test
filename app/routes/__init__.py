def register_routes(app):
    from .main_route import main_bp

    # 
    app.register_blueprint(main_bp)         # Main Routes