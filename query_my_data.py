import os
import json
import google.generativeai as genai

def load_data_from_jsonl(file_path):
    """Loads data from a JSON Lines file."""
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line))
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file '{file_path}'. Please check its format.")
        return None
    return data

def main():
    """Main function to run the AI query."""
    # 1. CONFIGURE API KEY
    # Direct API key configuration
    api_key = "AIzaSyDyEejMGMHNSfZu8AzD5W0yvbYHECDq5bU"
    if not api_key:
        print("Error: API key not configured.")
        return
        
    genai.configure(api_key=api_key)

    # 2. LOAD YOUR CUSTOM DATA
    data_file = "my_data.jsonl"
    my_data = load_data_from_jsonl(data_file)
    if my_data is None:
        return

    # Convert your structured data into a single string for the prompt
    data_context = "\n".join([f"Q: {item['question']}\nA: {item['answer']}" for item in my_data])

    # 3. DEFINE YOUR QUESTION
    # This is the question you want to ask the AI about your data.
    # Try changing it to "Who is the CEO?" or "What was the main product last year?"
    user_question = "Where is Innovate Inc. based?"

    # 4. CREATE THE PROMPT FOR THE GEMINI MODEL
    # We create a detailed prompt that tells the model exactly how to behave.
    prompt = f"""
    You are an expert assistant for a company called Innovate Inc.
    Your task is to answer questions based *only* on the information provided below.
    If the answer is not in the provided information, you must say "I'm sorry, that information is not available in my dataset."

    ---
    Information Dataset:
    {data_context}
    ---

    Based on the information above, please answer the following question:
    Question: "{user_question}"
    """

    # 5. CALL THE GEMINI API
    print("Asking Gemini...")
    try:
        # Use latest available models from the list
        model_names = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-flash-latest']
        
        for model_name in model_names:
            try:
                print(f"Trying model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                
                # 6. DISPLAY THE RESULT
                print("\n" + "="*20)
                print(f"Your Question: {user_question}")
                print("-" * 20)
                print(f"Gemini's Answer:\n{response.text}")
                print("="*20 + "\n")
                return  # Success, exit
                
            except Exception as model_error:
                print(f"Model {model_name} failed: {model_error}")
                continue
        
        print("All models failed. Trying to list available models...")
        
        # Try to list models as fallback
        try:
            models = genai.list_models()
            print("Available models:")
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    print(f"- {model.name}")
        except Exception as list_error:
            print(f"Could not list models: {list_error}")

    except Exception as e:
        print(f"An error occurred while calling the Gemini API: {e}")

if __name__ == "__main__":
    main()
