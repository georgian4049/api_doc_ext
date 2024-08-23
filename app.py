import os
from flask import Flask
import google.generativeai as genai
from flask import Flask, request, jsonify
from pathlib import Path
import json
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)
MODEL_CONFIG = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]
genai.configure(api_key = os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=MODEL_CONFIG, safety_settings=safety_settings)

@app.route('/')
def home():
    return "What do you wanna do with this empty link?"

# @app.post("/api/process")
# def process_image():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     file_path = Path(f"/tmp/{file.filename}")
#     file.save(file_path)
#     for key, value in request.form.items():
#         print(f"{key}: {value}")

#     system_prompt = request.form.get('system_prompt', "You are a specialist in comprehending receipts.")
#     user_prompt = "Convert Invoice data into json format with appropriate json tags as required for the data in image "
#     system_prompt = """
#                You are a specialist in comprehending receipts.
#                Input images in the form of receipts will be provided to you,
#                and your task is to respond to questions based on the content of the input image.
#                """
#     response = gemini_output(file_path, system_prompt, user_prompt)

#     try:
#         json_str = response.replace('```json\n', '').replace('\n```', '')
       
#         json_data = json.loads(json_str)
        
#         return jsonify(json_data)
#     except json.JSONDecodeError:
#         return jsonify({"error": "Failed to decode JSON from response"}), 500

#     finally:
#         # Clean up the uploaded file
#         if file_path.exists():
#             file_path.unlink()


@app.post("/api/process")
def process_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = Path(f"/tmp/{file.filename}")
    file.save(file_path)
    
    allowed_keys = []
    for key in request.form.keys():
        if key.startswith('labels'):
            allowed_keys.append(request.form[key])
    
    allowed_keys_lower = [key.lower() for key in allowed_keys]  # Convert all allowed keys to lowercase


    system_prompt = request.form.get('system_prompt', "You are a specialist in comprehending receipts.")
    user_prompt = "Convert Invoice data into json format with appropriate json tags as required for the data in image "
    system_prompt = """
               You are a specialist in comprehending receipts.
               Input images in the form of receipts will be provided to you,
               and your task is to respond to questions based on the content of the input image.
               """
    
    response = gemini_output(file_path, system_prompt, user_prompt)

    try:
        json_str = response.replace('```json\n', '').replace('\n```', '')
        json_data = json.loads(json_str)

        # Convert JSON keys to lowercase for case-insensitive comparison
        filtered_data = {
            key: value
            for key, value in json_data.items()
            if key.lower() in allowed_keys_lower
        }

        return jsonify(filtered_data)
    
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to decode JSON from response"}), 500

    finally:
        # Clean up the uploaded file
        if file_path.exists():
            file_path.unlink()
            
            
def gemini_output(image_path, system_prompt, user_prompt):
    image_info = image_format(image_path)
    input_prompt = [system_prompt, image_info[0], user_prompt]
    response = model.generate_content(input_prompt)
    return response.text

def image_format(image_path):
    img = Path(image_path)
    if not img.exists():
        raise FileNotFoundError(f"Could not find image: {img}")

    return [{"mime_type": "image/png", "data": img.read_bytes()}]  # Adjust MIME type as needed


if __name__ == "__main__":
    app.run(debug=True)
