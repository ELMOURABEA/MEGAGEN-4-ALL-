"""
Example: Integrating MEGA-Bot with a Flask application
"""
from flask import Flask, render_template_string, request, jsonify
from megabot import MegaBot, Config
import asyncio

app = Flask(__name__)

# Initialize MEGA-Bot
config = Config()
bot = MegaBot(config)
bot_started = False

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>MEGA-Bot Flask Integration</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .query-box { margin: 20px 0; }
        textarea { width: 100%; padding: 10px; margin: 10px 0; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { background: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .status.running { background: #d4edda; color: #155724; }
        .status.stopped { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>🤖 MEGA-Bot Flask Integration Demo</h1>
    
    <div class="status" id="status">
        <strong>Status:</strong> <span id="status-text">Loading...</span>
    </div>
    
    <div class="query-box">
        <h2>Ask MEGA-Bot</h2>
        <textarea id="query" rows="3" placeholder="Enter your question here..."></textarea>
        <button onclick="submitQuery()">Submit Query</button>
    </div>
    
    <div id="result" class="result" style="display: none;">
        <h3>Response:</h3>
        <div id="response-text"></div>
    </div>
    
    <script>
        // Update status on load
        fetch('/api/status')
            .then(r => r.json())
            .then(data => {
                const statusDiv = document.getElementById('status');
                const statusText = document.getElementById('status-text');
                statusText.textContent = data.running ? 'Running' : 'Stopped';
                statusDiv.className = 'status ' + (data.running ? 'running' : 'stopped');
            });
        
        function submitQuery() {
            const query = document.getElementById('query').value;
            if (!query.trim()) {
                alert('Please enter a question');
                return;
            }
            
            const resultDiv = document.getElementById('result');
            const responseDiv = document.getElementById('response-text');
            
            resultDiv.style.display = 'block';
            responseDiv.innerHTML = 'Processing...';
            
            fetch('/api/query', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: query})
            })
            .then(r => r.json())
            .then(data => {
                if (data.error) {
                    responseDiv.innerHTML = '<strong>Error:</strong> ' + data.error;
                } else {
                    let html = '<strong>Platforms responded:</strong> ' + 
                              data.synthesis.platforms_responded + '<br><br>';
                    
                    for (const [platform, resp] of Object.entries(data.responses)) {
                        html += '<strong>[' + platform + ']</strong><br>' + 
                               resp.response + '<br><br>';
                    }
                    responseDiv.innerHTML = html;
                }
            })
            .catch(err => {
                responseDiv.innerHTML = '<strong>Error:</strong> ' + err.message;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def status():
    """Get bot status"""
    global bot_started
    status = bot.get_status()
    return jsonify(status)

@app.route('/api/query', methods=['POST'])
def query():
    """Process query"""
    global bot_started
    
    # Start bot if not started
    if not bot_started:
        asyncio.run(bot.start())
        bot_started = True
    
    data = request.get_json()
    query_text = data.get('query', '')
    
    if not query_text:
        return jsonify({'error': 'No query provided'}), 400
    
    # Execute query
    result = asyncio.run(bot.query(query_text))
    return jsonify(result)

if __name__ == '__main__':
    print("=" * 80)
    print("MEGA-Bot Flask Integration Example")
    print("=" * 80)
    print("Starting server on http://localhost:5001")
    print("Open your browser to interact with MEGA-Bot")
    print("=" * 80)
    
    # Note: In production, use a proper WSGI server like gunicorn
    # For development only:
    app.run(host='127.0.0.1', port=5001, debug=False)
