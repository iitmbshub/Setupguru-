from flask import Flask, render_template, request, jsonify
import json
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
import os
api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDyEejMGMHNSfZu8AzD5W0yvbYHECDq5bU')
genai.configure(api_key=api_key)

def load_data_from_jsonl(file_path):
    """Load company data from JSONL file."""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line))
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    return data

# Data will be loaded fresh on each request

@app.route('/')
def index():
    return render_template('support.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/test')
def test():
    return jsonify({'message': 'Server is working!', 'status': 'success'})

@app.route('/debug')
def debug():
    import sys
    return jsonify({
        'python_version': sys.version,
        'flask_working': True,
        'gemini_key_set': bool(api_key),
        'data_file_exists': os.path.exists('my_data.jsonl')
    })

@app.route('/chat', methods=['POST'])
def chat():
    print(f"Received chat request")  # Debug log
    
    try:
        user_message = request.json.get('message', '')
        print(f"User message: {user_message}")  # Debug log
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Load fresh data on each request
        company_data = load_data_from_jsonl("my_data.jsonl")
        data_context = "\n".join([f"Q: {item['question']}\nA: {item['answer']}" for item in company_data])
        print(f"Loaded {len(company_data)} data entries")  # Debug log
        
        # Create business-focused prompt for Gemini
        prompt = f"""
        You are SetupGuru Support AI. Your goal is to convert every conversation into a sale.
        
        RULES:
        1. Keep responses SHORT (max 2-3 sentences)
        2. NO emojis - be professional
        3. ALWAYS push for purchase - be direct about buying
        4. Connect ANY topic to desk setup products
        5. Use company data when available, otherwise relate to business
        
        SALES APPROACH:
        - Direct: "You should buy our [product] because..."
        - Urgent: "Limited time WELCOME code gives 10% off"
        - Specific: Mention exact product categories
        - Action: "Visit www.setupguru.shop now" or "Call 9499473347 to order"
        
        BUSINESS INFO:
        Company: SetupGuru.shop | Founders: Rao Jatin & Aryan Soni | Helpline: 9499473347
        Products: Laptop accessories, desk organization, lighting, ergonomic items, smart gadgets
        Discount: WELCOME code for 10% off | Website: www.setupguru.shop
        
        EXAMPLES:
        Q: "What's the weather?"
        A: "I focus on desk setups, not weather. However, our LED lighting solutions work perfectly in any weather condition. Use WELCOME code for 10% off at www.setupguru.shop."
        
        Q: "How to study better?"
        A: "Better study requires proper desk setup. Our ergonomic accessories and lighting improve focus significantly. Order now with WELCOME code at www.setupguru.shop."
        
        ---
        Company Data:
        {data_context}
        ---
        
        Question: "{user_message}"
        
        Be direct, professional, and push for immediate purchase.
        """
        
        try:
            print("Calling Gemini API...")  # Debug log
            
            # Test without Gemini first
            if user_message.lower() == 'test':
                return jsonify({
                    'response': 'Test successful! Server and chat endpoint working.',
                    'status': 'success'
                })
            
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            print(f"Gemini response received")  # Debug log
            
            return jsonify({
                'response': response.text,
                'status': 'success'
            })
            
        except Exception as gemini_error:
            print(f"Gemini API error: {gemini_error}")  # Debug log
            return jsonify({
                'response': f"API Error: {str(gemini_error)}. Contact support at 9499473347.",
                'status': 'error'
            }), 500
            
    except Exception as e:
        print(f"General error: {e}")  # Debug log
        return jsonify({
            'response': "I'm sorry, something went wrong. Please try again.",
            'status': 'error'
        }), 500

if __name__ == '__main__':
    print("Starting SetupGuru Chat Server...")
    print("Server will be available at: http://localhost:5000")
    print("Data will be loaded fresh on each request - no restart needed for updates!")
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))