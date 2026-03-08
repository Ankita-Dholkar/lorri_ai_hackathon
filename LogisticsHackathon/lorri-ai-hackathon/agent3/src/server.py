from flask import Flask, request, jsonify
import re
import os
import uuid
import traceback
import pytesseract
from PIL import Image

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_from_image(image_path):
    """
    Standard OCR extraction using pytesseract.
    """
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

@app.route('/api/extract-toll', methods=['POST'])
def extract_toll():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        temp_filename = f"toll_{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
        file.save(filepath)

        raw_text = extract_from_image(filepath)
        
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)

        # Extraction logic
        total_match = re.search(r'(?i)(?:total|amount|rs\.?|inr|₹)\s*[:.-]?\s*([\d,]+\.?\d*)', raw_text)
        extracted_total = 0
        if total_match:
            try:
                extracted_val = total_match.group(1).replace(',', '')
                extracted_total = float(extracted_val)
            except ValueError:
                pass

        return jsonify({
            'type': 'toll',
            'amount': extracted_total,
            'rawText': raw_text
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extract-fuel', methods=['POST'])
def extract_fuel():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        temp_filename = f"fuel_{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        filepath = os.path.join(UPLOAD_FOLDER, temp_filename)
        file.save(filepath)

        raw_text = extract_from_image(filepath)
        
        # Clean up
        if os.path.exists(filepath):
            os.remove(filepath)

        # Extraction logic
        total_match = re.search(r'(?i)(?:total|amount|rs\.?|inr|₹)\s*[:.-]?\s*([\d,]+\.?\d*)', raw_text)
        extracted_total = 0
        if total_match:
            try:
                extracted_val = total_match.group(1).replace(',', '')
                extracted_total = float(extracted_val)
            except ValueError:
                pass

        return jsonify({
            'type': 'fuel',
            'amount': extracted_total,
            'rawText': raw_text
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8002, debug=True)
