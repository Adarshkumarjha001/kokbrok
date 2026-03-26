import gradio as gr
from transformers import pipeline

print("=" * 60)
print("Loading Kokborok NLP Model from Hugging Face...")
print("This may take a minute on first run...")
print("=" * 60)

try:
    # Load model from Hugging Face Hub
    nlp = pipeline(
        "token-classification", 
        model="ritik3412/Kokborok_model", 
        aggregation_strategy="simple"
    )
    print("✓ Model loaded successfully!")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    exit(1)

# POS tag colors
TAG_COLORS = {
    "NOUN": "#4ade80", "VERB": "#3b82f6", "ADJ": "#fbbf24",
    "PRON": "#818cf8", "ADV": "#34d399", "DET": "#fb923c",
    "ADP": "#a78bfa", "CCONJ": "#f472b6", "PUNCT": "#94a3b8",
    "PROPN": "#10b981", "NUM": "#22d3ee", "AUX": "#60a5fa",
    "INTJ": "#f87171", "PART": "#c084fc", "SCONJ": "#ec4899",
    "UNK": "#6b7280", "X": "#64748b"
}

def analyze_text(text):
    """Analyze Kokborok text and return color-coded POS tags"""
    if not text.strip():
        return "<p style='color: #94a3b8; padding: 1rem;'>Please enter Kokborok text to analyze.</p>"
    
    try:
        # Get predictions from model
        tokens = nlp(text)
        
        # Build HTML output
        html = "<div style='font-size: 1.1em; line-height: 2.5em; padding: 1rem;'>"
        
        for token in tokens:
            word = token["word"].strip()
            label = token["entity_group"]
            score = round(float(token["score"]) * 100, 1)
            color = TAG_COLORS.get(label, "#6b7280")
            
            html += (
                f"<span style='background:{color}; color:white; padding:6px 12px; "
                f"border-radius:6px; margin:4px; display:inline-block; font-weight:500;' "
                f"title='Confidence: {score}%'>"
                f"{word} <sub style='font-size:0.75em;'>{label}</sub></span> "
            )
        
        html += "</div>"
        
        # Add legend
        html += "<div style='margin-top: 2rem; padding: 1rem; background: #f8fafc; border-radius: 8px;'>"
        html += "<h4 style='margin-bottom: 1rem; color: #1e293b;'>POS Tags Legend:</h4>"
        html += "<div style='display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 0.5rem;'>"
        
        tag_info = {
            "NOUN": "Noun", "VERB": "Verb", "ADJ": "Adjective", "PRON": "Pronoun",
            "ADV": "Adverb", "DET": "Determiner", "ADP": "Adposition", "CCONJ": "Conjunction",
            "PUNCT": "Punctuation", "PROPN": "Proper Noun", "NUM": "Numeral", "AUX": "Auxiliary",
            "INTJ": "Interjection", "PART": "Particle", "SCONJ": "Sub. Conjunction", 
            "UNK": "Unknown", "X": "Other"
        }
        
        for tag, name in tag_info.items():
            color = TAG_COLORS.get(tag, "#6b7280")
            html += (
                f"<div style='display: flex; align-items: center; gap: 0.5rem;'>"
                f"<div style='width: 20px; height: 20px; background: {color}; border-radius: 4px;'></div>"
                f"<span style='font-size: 0.85em; color: #475569;'><b>{tag}</b> - {name}</span>"
                f"</div>"
            )
        
        html += "</div></div>"
        return html
        
    except Exception as e:
        return f"<p style='color: #ef4444; padding: 1rem;'>Error: {str(e)}</p>"

# About section
about_html = """
<div style='padding: 2rem; background: linear-gradient(135deg, #2563eb, #7c3aed); color: white; border-radius: 12px; margin-bottom: 2rem;'>
    <h1 style='margin: 0 0 0.5rem 0; font-size: 2.5rem;'>🌐 Kokborok Language NLP Model</h1>
    <p style='margin: 0; font-size: 1.2rem; opacity: 0.9;'>Advanced Part-of-Speech Tagging for Kokborok</p>
</div>

<div style='padding: 1.5rem; background: #f8fafc; border-radius: 8px; margin-bottom: 1.5rem;'>
    <h3 style='color: #2563eb; margin-top: 0;'>📚 About Kokborok Language</h3>
    <p>Kokborok (also known as Tripuri) is a Tibeto-Burman language spoken by approximately 1 million people in Tripura, India. 
    This NLP system helps preserve and promote the language through digital technology.</p>
</div>

<div style='padding: 1.5rem; background: #f8fafc; border-radius: 8px;'>
    <h3 style='color: #7c3aed; margin-top: 0;'>🤖 About This Model</h3>
    <p>This model uses <b>XLM-RoBERTa</b> (125M parameters) fine-tuned for token classification. 
    It identifies 17 different parts of speech in Kokborok text with high accuracy.</p>
</div>
"""

# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="Kokborok NLP") as demo:
    gr.HTML(about_html)
    
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(
                lines=5,
                placeholder="Enter Kokborok text here...\nExample: Angni bwisani rwchapha khamwi.",
                label="📝 Input Kokborok Text",
                info="Type or paste Kokborok sentences to analyze"
            )
            analyze_btn = gr.Button("🔍 Analyze Text", variant="primary", size="lg")
    
    output_html = gr.HTML(label="📊 Analysis Results")
    
    # Example sentences
    gr.Examples(
        examples=[
            ["Angni bwisani rwchapha khamwi."],
            ["Bwrwi rwchapha bwisani."],
            ["Chini rwchapha bwrwi angni khamwi."],
            ["Kokborok tei Tripura ni rajya tei."],
            ["Ang nwng kwrwi sa."]
        ],
        inputs=input_text,
        label="💡 Try These Examples"
    )
    
    # Event handlers
    analyze_btn.click(fn=analyze_text, inputs=input_text, outputs=output_html)
    input_text.submit(fn=analyze_text, inputs=input_text, outputs=output_html)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Starting Gradio interface...")
    print("=" * 60 + "\n")
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860)
