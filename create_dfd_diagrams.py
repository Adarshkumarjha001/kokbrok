from PIL import Image, ImageDraw, ImageFont
import os

def create_context_diagram():
    """Create Level 0 DFD (Context Diagram)"""
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_medium = ImageFont.truetype("arial.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((400, 30), "Level 0 DFD - Context Diagram", fill='black', font=font_large)
    
    # External Entity - User (left)
    draw.rectangle([50, 300, 250, 400], outline='blue', width=3)
    draw.text((120, 340), "User", fill='blue', font=font_medium)
    
    # Process - System (center)
    draw.ellipse([450, 250, 750, 450], outline='green', width=3)
    draw.text((500, 330), "Kokborok NLP", fill='green', font=font_medium)
    draw.text((530, 360), "System", fill='green', font=font_medium)
    
    # External Entity - Model Repository (right)
    draw.rectangle([950, 300, 1150, 400], outline='blue', width=3)
    draw.text((970, 330), "Hugging Face", fill='blue', font=font_medium)
    draw.text((1000, 360), "Model Hub", fill='blue', font=font_medium)
    
    # Data Flows
    # User to System
    draw.line([250, 350, 450, 350], fill='red', width=2)
    draw.polygon([(450, 350), (440, 345), (440, 355)], fill='red')
    draw.text((300, 320), "Kokborok Text", fill='red', font=font_small)
    
    # System to User
    draw.line([450, 380, 250, 380], fill='red', width=2)
    draw.polygon([(250, 380), (260, 375), (260, 385)], fill='red')
    draw.text((300, 390), "Tagged Results", fill='red', font=font_small)
    
    # System to Model Hub
    draw.line([750, 330, 950, 330], fill='red', width=2)
    draw.polygon([(950, 330), (940, 325), (940, 335)], fill='red')
    draw.text((800, 300), "Model Request", fill='red', font=font_small)
    
    # Model Hub to System
    draw.line([950, 370, 750, 370], fill='red', width=2)
    draw.polygon([(750, 370), (760, 365), (760, 375)], fill='red')
    draw.text((800, 380), "Model Weights", fill='red', font=font_small)
    
    img.save('DFD_Level0_Context.png')
    print("Created: DFD_Level0_Context.png")

def create_level1_diagram():
    """Create Level 1 DFD"""
    width, height = 1400, 1000
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_medium = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((500, 30), "Level 1 DFD - Detailed Process", fill='black', font=font_large)
    
    # External Entity - User
    draw.rectangle([50, 450, 200, 550], outline='blue', width=3)
    draw.text((100, 490), "User", fill='blue', font=font_medium)
    
    # Process 1: Input Validation
    draw.ellipse([300, 100, 500, 200], outline='green', width=2)
    draw.text((340, 140), "1. Validate", fill='green', font=font_medium)
    
    # Process 2: Tokenization
    draw.ellipse([600, 100, 800, 200], outline='green', width=2)
    draw.text((630, 140), "2. Tokenize", fill='green', font=font_medium)
    
    # Process 3: Model Inference
    draw.ellipse([900, 100, 1100, 200], outline='green', width=2)
    draw.text((920, 130), "3. Model", fill='green', font=font_medium)
    draw.text((920, 155), "Inference", fill='green', font=font_medium)
    
    # Process 4: Format Results
    draw.ellipse([900, 400, 1100, 500], outline='green', width=2)
    draw.text((930, 440), "4. Format", fill='green', font=font_medium)
    
    # Process 5: Display
    draw.ellipse([600, 400, 800, 500], outline='green', width=2)
    draw.text((650, 440), "5. Display", fill='green', font=font_medium)
    
    # Data Store 1: Model Weights
    draw.rectangle([1200, 100, 1350, 150], outline='purple', width=2)
    draw.text((1210, 115), "D1: Model", fill='purple', font=font_small)
    draw.text((1210, 130), "Weights", fill='purple', font=font_small)
    
    # Data Store 2: Config
    draw.rectangle([1200, 180, 1350, 230], outline='purple', width=2)
    draw.text((1210, 195), "D2: Config", fill='purple', font=font_small)
    
    # Data Store 3: POS Tags
    draw.rectangle([1200, 400, 1350, 450], outline='purple', width=2)
    draw.text((1210, 415), "D3: POS", fill='purple', font=font_small)
    draw.text((1210, 430), "Definitions", fill='purple', font=font_small)
    
    # Data Flows
    # User to Process 1
    draw.line([200, 500, 350, 200], fill='red', width=2)
    draw.polygon([(350, 200), (345, 210), (355, 205)], fill='red')
    draw.text([210, 350], "Input Text", fill='red', font=font_small)
    
    # Process 1 to Process 2
    draw.line([500, 150, 600, 150], fill='red', width=2)
    draw.polygon([(600, 150), (590, 145), (590, 155)], fill='red')
    draw.text([520, 130], "Validated", fill='red', font=font_small)
    
    # Process 2 to Process 3
    draw.line([800, 150, 900, 150], fill='red', width=2)
    draw.polygon([(900, 150), (890, 145), (890, 155)], fill='red')
    draw.text([820, 130], "Tokens", fill='red', font=font_small)
    
    # Process 3 to Data Store 1
    draw.line([1100, 125, 1200, 125], fill='red', width=2)
    draw.text([1120, 105], "Read", fill='red', font=font_small)
    
    # Process 3 to Data Store 2
    draw.line([1100, 180, 1200, 205], fill='red', width=2)
    draw.text([1120, 185], "Read", fill='red', font=font_small)
    
    # Process 3 to Process 4
    draw.line([1000, 200, 1000, 400], fill='red', width=2)
    draw.polygon([(1000, 400), (995, 390), (1005, 390)], fill='red')
    draw.text([1010, 290], "Predictions", fill='red', font=font_small)
    
    # Data Store 3 to Process 4
    draw.line([1200, 425, 1100, 450], fill='red', width=2)
    draw.text([1120, 430], "Read", fill='red', font=font_small)
    
    # Process 4 to Process 5
    draw.line([900, 450, 800, 450], fill='red', width=2)
    draw.polygon([(800, 450), (810, 445), (810, 455)], fill='red')
    draw.text([820, 430], "Formatted", fill='red', font=font_small)
    
    # Process 5 to User
    draw.line([650, 500, 200, 520], fill='red', width=2)
    draw.polygon([(200, 520), (210, 515), (210, 525)], fill='red')
    draw.text([350, 520], "Tagged Output", fill='red', font=font_small)
    
    img.save('DFD_Level1_Detailed.png')
    print("Created: DFD_Level1_Detailed.png")

def create_er_diagram():
    """Create E-R Diagram"""
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_medium = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((450, 30), "Entity-Relationship Diagram", fill='black', font=font_large)
    
    # Entity 1: Model Configuration
    draw.rectangle([100, 150, 350, 350], outline='blue', width=3)
    draw.text((150, 170), "Model Configuration", fill='blue', font=font_medium)
    draw.line([100, 200, 350, 200], fill='blue', width=2)
    attributes = [
        "architecture",
        "hidden_size: 768",
        "num_layers: 12",
        "vocab_size: 250002",
        "num_labels: 17"
    ]
    y = 220
    for attr in attributes:
        draw.text((110, y), attr, fill='black', font=font_small)
        y += 25
    
    # Entity 2: POS Tags
    draw.rectangle([500, 150, 750, 400], outline='blue', width=3)
    draw.text((580, 170), "POS Tags", fill='blue', font=font_medium)
    draw.line([500, 200, 750, 200], fill='blue', width=2)
    tags = [
        "tag_id",
        "tag_code (NOUN, VERB...)",
        "tag_name",
        "description",
        "color_code",
        "examples"
    ]
    y = 220
    for tag in tags:
        draw.text((510, y), tag, fill='black', font=font_small)
        y += 30
    
    # Entity 3: Token
    draw.rectangle([850, 150, 1100, 350], outline='blue', width=3)
    draw.text((930, 170), "Token", fill='blue', font=font_medium)
    draw.line([850, 200, 1100, 200], fill='blue', width=2)
    token_attrs = [
        "token_text",
        "token_id",
        "position",
        "confidence_score"
    ]
    y = 220
    for attr in token_attrs:
        draw.text((860, y), attr, fill='black', font=font_small)
        y += 30
    
    # Relationship: Model uses POS Tags
    draw.line([350, 250, 500, 275], fill='green', width=2)
    draw.polygon([(500, 275), (490, 270), (490, 280)], fill='green')
    draw.text((380, 250), "defines", fill='green', font=font_small)
    
    # Relationship: Token assigned POS Tag
    draw.line([750, 275, 850, 250], fill='green', width=2)
    draw.polygon([(850, 250), (840, 255), (840, 245)], fill='green')
    draw.text((770, 250), "assigned", fill='green', font=font_small)
    
    # Legend
    draw.text((100, 450), "Legend:", fill='black', font=font_medium)
    draw.rectangle([100, 480, 200, 530], outline='blue', width=2)
    draw.text((220, 495), "= Entity", fill='black', font=font_small)
    draw.line([100, 560, 200, 560], fill='green', width=2)
    draw.polygon([(200, 560), (190, 555), (190, 565)], fill='green')
    draw.text((220, 550), "= Relationship", fill='black', font=font_small)
    
    img.save('ER_Diagram.png')
    print("Created: ER_Diagram.png")

# Generate all diagrams
if __name__ == "__main__":
    create_context_diagram()
    create_level1_diagram()
    create_er_diagram()
    print("\nAll diagrams created successfully!")
