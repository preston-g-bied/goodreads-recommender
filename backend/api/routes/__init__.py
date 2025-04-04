# backend/api/routes/__init__.py

"""
Route registration module for Flask blueprints
"""

from flask import Blueprint

def register_routes(app):
    """Register all API routes with the Flask application"""

    # API version prefix
    api_prefix = '/api/v1'

    # import blueprints
    from .books import books_bp
    from .users import users_bp
    from .auth import auth_bp
    from .recommendations import recommendations_bp

    # register blueprints with URL prefixes
    app.register_blueprint(books_bp, url_prefix=f'{api_prefix}/books')
    app.register_blueprint(users_bp, url_prefix=f'{api_prefix}/users')
    app.register_blueprint(auth_bp, url_prefix=f'{api_prefix}/auth')
    app.register_blueprint(recommendations_bp, url_prefix=f'{api_prefix}/recommendations')

    # register error handlers
    from backend.api.utils.responses import handle_not_found, handle_servor_error

    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(500, handle_servor_error)

    # root endpoint
    @app.route('/')
    def index():
        """Root endpoint"""
        return {
            'message': 'Welcome to the Goodbooks API',
            'version': app.config['API_VERSION'],
            'status': 'operational'
        }