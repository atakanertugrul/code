"""Product Description AI Application - Flask Backend."""

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_description():
    """Generate product description using AI."""
    try:
        data = request.json

        # Extract product information
        product_name = data.get('product_name', '')
        category = data.get('category', '')
        features = data.get('features', '')
        target_audience = data.get('target_audience', '')
        tone = data.get('tone', 'professional')
        language = data.get('language', 'Turkish')

        # Validate input
        if not product_name:
            return jsonify({'error': 'Ürün adı gereklidir'}), 400

        # Create prompt for AI
        prompt = f"""Sen bir ürün açıklaması yazan profesyonel bir yazarsın. Aşağıdaki bilgilere göre çekici ve detaylı bir ürün açıklaması oluştur.

Ürün Adı: {product_name}
Kategori: {category}
Özellikler: {features}
Hedef Kitle: {target_audience}
Ton: {tone}
Dil: {language}

Lütfen aşağıdaki formatta bir ürün açıklaması oluştur:

1. Çekici bir başlık
2. Ana açıklama (2-3 paragraf)
3. Önemli özellikler (madde madde)
4. Kullanım alanları
5. Neden tercih edilmeli?

Açıklama {language} dilinde olmalı ve {tone} bir tonla yazılmalıdır."""

        # Call OpenAI API
        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME", "gpt-4-turbo-preview"),
            messages=[
                {"role": "system", "content": "Sen profesyonel bir ürün açıklaması yazarısın. Yaratıcı, çekici ve ikna edici açıklamalar yazarsın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        description = response.choices[0].message.content

        return jsonify({
            'success': True,
            'description': description,
            'product_info': {
                'name': product_name,
                'category': category,
                'features': features,
                'target_audience': target_audience,
                'tone': tone,
                'language': language
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        exit(1)

    print("🚀 Starting Product Description AI Application...")
    print("📝 Server running at: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
