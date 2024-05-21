# Importing libraries
import io
from flask import Flask, render_template, request, send_file
import os
import time
import pandas as pd
from script import sentence_parser
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

# Defining testing user creds
user_credentials = {
    'Tanvi&Cindy': 'ANZ123'
}

# First page
@app.route('/')
def index():
    return render_template('login.html', body_class='login')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Getting values from login page
    user_name = request.form['user_name']
    pwd = request.form['password']

    # Checking if the credentials are valid
    if user_name in user_credentials.keys():
        if user_credentials[user_name] == pwd:
            return render_template('pdfParser.html', username=user_name.title(), body_class='pdfParser')
    else:
        # If credentials are invalid, display error message
        error_msg = 'Invalid credentials. Please try again!!'
        return render_template('login.html', error=error_msg, body_class='login')


# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('registration.html', body_class='register')


# Check for user registration
@app.route('/register_check', methods=['GET', 'POST'])
def register_check():
    """
    !!!!!!!!!!..To be implemented..!!!!!!!!!!
    """
    # Render the registration form
    return render_template('login.html', body_class='login')


# PDF Parsing and Similarity Scoring
@app.route('/parse', methods=['POST'])
def parse():
    uploaded_files = request.files.getlist("file")
    query_input = request.form['query_input']
    use_pypdf = request.form.get('use_pypdf')
    use_ocr = request.form.get('use_ocr')

    upload_folder = 'input'
    app.config['UPLOAD_FOLDER'] = upload_folder

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    print("Input folder created")

    sentences_with_metadata = []

    for file in uploaded_files:
        # Save the uploaded file to a temporary location
        temp_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(temp_file_path)
        print(f"{file.filename} - saved to {temp_file_path}")

        if use_pypdf:
            print("Sentence parsing initiated!!")
            parsed_sentences = sentence_parser(temp_file_path, parsing_method="pypdf")
        if use_ocr:
            parsed_sentences = sentence_parser(temp_file_path, parsing_method="ocr")

        # Add page number, filename, and sentence metadata
        for idx, item in enumerate(parsed_sentences):
            sentences_with_metadata.append({
                'Page Number': item['Page'],
                'Filename': item['Filename'],
                'Sentence': item['Sentence']
            })

        # Delete the temporary file after processing
        os.remove(temp_file_path)
        print("Uploads folder removed")

    df = pd.DataFrame(sentences_with_metadata)

    if not df.empty:
        mvp_v2_model = SentenceTransformer("all-mpnet-base-v2")
        start_time = time.time()
        query_embedding = mvp_v2_model.encode(query_input)

        sentence_embedding = mvp_v2_model.encode(df['Sentence']).tolist()
        scores = util.cos_sim(query_embedding, sentence_embedding)[0]
        
        df['Score'] = scores.tolist()

        end_time = time.time()
        total_time = end_time - start_time
        print(f"Total execution time: {total_time} seconds")

        sorted_df = df.sort_values(by='Score', ascending=False)

        return render_template('results.html', tables=[sorted_df.to_html(classes='data', index=False)],
                               titles=sorted_df.columns.values, body_class='results', sorted_df=sorted_df)
    else:
        return "No data found."


# Download results to CSV
@app.route('/download', methods=['POST'])
def download():
    csv_data = request.form['csv_data']
    df = pd.read_csv(io.StringIO(csv_data))
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return send_file(csv_buffer,
                     mimetype='text/csv',
                     download_name='results.csv',
                     as_attachment=True)


# Main function
if __name__ == "__main__":
    app.run(debug=True)
