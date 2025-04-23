from quart import Quart, request, jsonify, render_template
import os
import base64
import requests

app = Quart(__name__)

# Configuration
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
async def index():
    return await render_template('index.html')

@app.route('/upload', methods=['POST'])
async def upload_image():
    if 'file' not in await request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = (await request.files)['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    form_data = await request.form
    additional_prompt = form_data.get('prompt', '')

    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        await file.save(file_path)
        
        # Encode image to base64
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Call Llava API
        try:
            prompt = f"{additional_prompt} and Describe this image in detail."
            response = requests.post('http://host.docker.internal:11434/api/generate', json={
                'model': 'llava',
                'prompt': prompt.strip(),
                'images': [encoded_string],
                'stream': False
            })
            response.raise_for_status()
            description = response.json().get('response', 'No description provided')
        except requests.RequestException as e:
            return jsonify({'error': f'Failed to get description: {str(e)}'}), 500
        
        return jsonify({'description': description}), 200
    
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)