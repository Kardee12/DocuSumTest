import fileinput
import os

from flask import Flask, redirect, render_template, request, session, flash
import helpers
import llmhelpers
from llmhelpers import huggingFaceAPis
app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.secret_key = 'egjkerhgbhegfe'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/workspace', methods=['GET', 'POST'])
def workspace():
    if request.method == 'POST':
        action = request.form.get('action')
        model = request.form.get('model')
        extracted_text = session.get('extracted_text')
        print("TESTeejnerjne")
        print(extracted_text)
        if not extracted_text:
            flash('No text available for processing.', 'error')
            return redirect('workspace')
        try:
            if action == 'summarize':
                summary = huggingFaceAPis.sumQuery(model, extracted_text, max_length=150, min_length=50)
                return render_template('workspace.html', results=summary, extracted_text=extracted_text)
            elif action == 'translate':
                target_language = request.form.get('targetLanguage')
                translation = huggingFaceAPis.translateQuery(model, extracted_text, target_language)
                return render_template('workspace.html', results=translation, extracted_text=extracted_text)
            elif action == 'question':
                question = request.form.get('textInputQuestion')
                answer = huggingFaceAPis.questionQuery(model, extracted_text, question)
                return render_template('workspace.html', results=answer, extracted_text=extracted_text)
            elif action == 'sentiment':
                sentiment = huggingFaceAPis.sentimentQuery(model, extracted_text)
                return render_template('workspace.html', results=sentiment, extracted_text=extracted_text)
            else:
                flash('Invalid action.', 'error')
                return redirect('workspace')
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect('workspace')
    extracted_text = session.get('extracted_text')
    return render_template('workspace.html', extracted_text=extracted_text)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    session['extracted_text'] = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if 'file' in request.files and helpers.allowed_file(file.filename):
            # Save the file to the uploads folder
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            # Extract text from the file
            extracted_text = helpers.extract_text_from_pdf(file_path)
            # Store the extracted text in the session
            session['extracted_text'] = extracted_text
            return redirect("workspace")
        else:
            flash('Invalid file type')
            return redirect(request.url)


if __name__ == '__main__':
    app.run()
