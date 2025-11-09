"""
Flask REST API for MEGA-Bot
Provides HTTP endpoints for integration with web applications and systems
"""
import asyncio
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
import concurrent.futures
from ..core import MegaBot
from ..config import Config

def async_route(f):
    """Decorator to handle async routes in Flask using a thread pool"""
    @wraps(f)
    def wrapped(*args, **kwargs):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, f(*args, **kwargs))
            return future.result()
    return wrapped


def create_app(config=None):
    """
    Create and configure Flask application for MEGA-Bot API
    
    Args:
        config: Optional Config object
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    CORS(app)  # Enable CORS for web applications
    
    # Initialize MEGA-Bot
    bot_config = config or Config()
    bot = MegaBot(bot_config)
    
    # Store bot in app config
    app.config['MEGABOT'] = bot
    app.config['BOT_STARTED'] = False
    
    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'service': 'MEGA-Bot API'
        })
    
    @app.route('/api/v1/start', methods=['POST'])
    @async_route
    async def start_bot():
        """Start the MEGA-Bot service"""
        bot = app.config['MEGABOT']
        if app.config['BOT_STARTED']:
            return jsonify({'message': 'Bot already started', 'status': 'running'}), 200
        
        await bot.start()
        app.config['BOT_STARTED'] = True
        return jsonify({'message': 'Bot started successfully', 'status': 'running'}), 200
    
    @app.route('/api/v1/stop', methods=['POST'])
    @async_route
    async def stop_bot():
        """Stop the MEGA-Bot service"""
        bot = app.config['MEGABOT']
        if not app.config['BOT_STARTED']:
            return jsonify({'message': 'Bot not running', 'status': 'stopped'}), 200
        
        await bot.stop()
        app.config['BOT_STARTED'] = False
        return jsonify({'message': 'Bot stopped successfully', 'status': 'stopped'}), 200
    
    @app.route('/api/v1/status', methods=['GET'])
    def get_status():
        """Get bot status"""
        bot = app.config['MEGABOT']
        status = bot.get_status()
        return jsonify(status), 200
    
    @app.route('/api/v1/capabilities', methods=['GET'])
    def get_capabilities():
        """Get bot capabilities"""
        bot = app.config['MEGABOT']
        capabilities = bot.get_capabilities()
        return jsonify({
            'capabilities': capabilities,
            'count': len(capabilities)
        }), 200
    
    @app.route('/api/v1/query', methods=['POST'])
    @async_route
    async def query():
        """
        Query all AI platforms
        
        Request body:
        {
            "prompt": "Your query here"
        }
        """
        if not app.config['BOT_STARTED']:
            return jsonify({'error': 'Bot not started. Call /api/v1/start first'}), 400
        
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing required field: prompt'}), 400
        
        bot = app.config['MEGABOT']
        result = await bot.query(data['prompt'])
        return jsonify(result), 200
    
    @app.route('/api/v1/research', methods=['POST'])
    @async_route
    async def research():
        """
        Perform deep research
        
        Request body:
        {
            "topic": "Your topic here",
            "depth": "shallow|medium|deep"  // optional, default: medium
        }
        """
        if not app.config['BOT_STARTED']:
            return jsonify({'error': 'Bot not started. Call /api/v1/start first'}), 400
        
        data = request.get_json()
        if not data or 'topic' not in data:
            return jsonify({'error': 'Missing required field: topic'}), 400
        
        depth = data.get('depth', 'medium')
        if depth not in ['shallow', 'medium', 'deep']:
            return jsonify({'error': 'Invalid depth. Must be shallow, medium, or deep'}), 400
        
        bot = app.config['MEGABOT']
        result = await bot.research(data['topic'], depth=depth)
        return jsonify(result), 200
    
    @app.route('/api/v1/workflow', methods=['POST'])
    @async_route
    async def execute_workflow():
        """
        Execute a workflow
        
        Request body:
        {
            "workflow_name": "comprehensive_analysis",
            "params": {
                "topic": "Your topic here"
            }
        }
        """
        if not app.config['BOT_STARTED']:
            return jsonify({'error': 'Bot not started. Call /api/v1/start first'}), 400
        
        data = request.get_json()
        if not data or 'workflow_name' not in data:
            return jsonify({'error': 'Missing required field: workflow_name'}), 400
        
        bot = app.config['MEGABOT']
        params = data.get('params', {})
        result = await bot.execute_workflow(data['workflow_name'], **params)
        return jsonify(result), 200
    
    @app.route('/api/v1/updates', methods=['GET'])
    def get_updates():
        """Get latest platform updates"""
        bot = app.config['MEGABOT']
        limit = request.args.get('limit', default=10, type=int)
        updates = bot.get_updates(limit=limit)
        return jsonify({
            'updates': updates,
            'count': len(updates)
        }), 200
    
    @app.route('/api/v1/sync', methods=['POST'])
    @async_route
    async def sync_documents():
        """Sync documents from all platforms"""
        if not app.config['BOT_STARTED']:
            return jsonify({'error': 'Bot not started. Call /api/v1/start first'}), 400
        
        bot = app.config['MEGABOT']
        await bot.sync_documents()
        return jsonify({'message': 'Documents synchronized successfully'}), 200
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


def main():
    """Main entry point for Flask server"""
    import sys
    
    # Parse command line arguments
    port = 5000
    debug = False
    
    if '--port' in sys.argv:
        try:
            port = int(sys.argv[sys.argv.index('--port') + 1])
        except (IndexError, ValueError):
            print("Invalid port number")
            sys.exit(1)
    
    if '--debug' in sys.argv:
        debug = True
    
    # Create and run app
    app = create_app()
    
    print("=" * 80)
    print("MEGA-Bot REST API Server")
    print("=" * 80)
    print(f"Server running on http://localhost:{port}")
    print(f"API Documentation: http://localhost:{port}/health")
    print("\nEndpoints:")
    print("  POST /api/v1/start        - Start the bot")
    print("  POST /api/v1/stop         - Stop the bot")
    print("  GET  /api/v1/status       - Get bot status")
    print("  GET  /api/v1/capabilities - Get bot capabilities")
    print("  POST /api/v1/query        - Query AI platforms")
    print("  POST /api/v1/research     - Perform deep research")
    print("  POST /api/v1/workflow     - Execute workflow")
    print("  GET  /api/v1/updates      - Get platform updates")
    print("  POST /api/v1/sync         - Sync documents")
    print("=" * 80)
    
    # Note: For production, use a proper WSGI server like gunicorn or waitress
    # Debug mode is disabled by default for security
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    main()
