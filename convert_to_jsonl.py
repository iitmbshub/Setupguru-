import json

# Read the current file (which is in JSON array format)
with open('my_data.jsonl', 'r', encoding='utf-8') as f:
    content = f.read()

# Try to parse as JSON array
try:
    data = json.loads(content)
    
    # Write back in proper JSONL format
    with open('my_data.jsonl', 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"Successfully converted {len(data)} entries to JSONL format!")
    
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    print("File might already be in JSONL format or has syntax errors.")