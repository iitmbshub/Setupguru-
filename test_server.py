from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is working!"

@app.route('/test-chat', methods=['POST'])
def test_chat():
    try:
        data = request.get_json()
        message = data.get('message', 'No message')
        
        return jsonify({
            'response': f'Test response for: {message}',
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'response': f'Error: {str(e)}',
            'status': 'error'
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)