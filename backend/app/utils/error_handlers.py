def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "resource not found"}, 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return {"error": "method not allowed"}, 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return {"error": "an unexpected error occurred"}, 500
