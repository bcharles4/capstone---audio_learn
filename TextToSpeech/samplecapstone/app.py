import os
from flask import Flask, request, render_template, send_file
from gtts import gTTS
from PyPDF2 import PdfReader
from docx import Document

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def extract_text_from_file(file_path, file_type):
    text = ""
    if file_type == 'txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    elif file_type == 'pdf':
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text()
    elif file_type == 'docx':
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Determine file type (txt, pdf, docx)
        file_type = file.filename.rsplit('.', 1)[1].lower()
        text = extract_text_from_file(file_path, file_type)
        
        # Convert text to speech using gTTS
        tts = gTTS(text)
        audio_file = os.path.join(app.config['UPLOAD_FOLDER'], 'output.mp3')
        tts.save(audio_file)

        return send_file(audio_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
