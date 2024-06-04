from flask import Flask, render_template, request, redirect, url_for
import os
from docx import Document

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'docx'}

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('show_results', filename=filename))
    return redirect(request.url)

@app.route('/results/<filename>')
def show_results(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    document = Document(file_path)

    data = {}
    for para in document.paragraphs:
        text = para.text
        if 'Estimated Survey Duration' in text:
            data['Estimated Survey Duration'] = text.split(':')[-1].strip()
        elif 'Number of Questions' in text:
            data['Number of Questions'] = text.split(':')[-1].strip()
        elif 'Number of Words' in text:
            data['Number of Words'] = text.split(':')[-1].strip()
        elif 'Level of Reader' in text:
            data['Level of Reader'] = text.split(':')[-1].strip()

    return render_template('results.html', data=data)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
