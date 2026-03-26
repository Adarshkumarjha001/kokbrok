from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from transformers import pipeline
import os

app = Flask(__name__)
CORS(app)

# Load model from Hugging Face Hub
MODEL_NAME = "ritik3412/Kokborok_model"
print("=" * 60)
print(f"Loading model from Hugging Face: {MODEL_NAME}")
print("This may take a minute on first run...")
print("=" * 60)

try:
    nlp = pipeline(
        "token-classification", 
        model=MODEL_NAME, 
        aggregation_strategy="simple"
    )
    print("✓ Model loaded successfully!")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    nlp = None

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    if nlp is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Use pipeline to get predictions
        tokens = nlp(text)
        
        # Format results
        results = []
        for token in tokens:
            results.append({
                'text': token['word'].strip(),
                'tag': token['entity_group'],
                'score': round(float(token['score']) * 100, 1)
            })
        
        return jsonify({'tokens': results})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    return jsonify({
        'architecture': model.config.architectures[0],
        'num_labels': len(id2label),
        'labels': list(id2label.values()),
        'vocab_size': model.config.vocab_size,
        'max_length': tokenizer.model_max_length
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
