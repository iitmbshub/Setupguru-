from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running!"

@app.route('/test')
def test():
    return jsonify({'message': 'Test successful', 'status': 'ok'})

if __name__ == '__main__':
    print("Starting simple test server...")
    app.run(debug=True, host='127.0.0.1', port=5001)