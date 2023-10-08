from flask import Flask, render_template, request, Response
import pandas as pd
from googletrans import Translator
from transformers import pipeline
import io
import traceback  # Import the traceback module for detailed error messages
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # Read the uploaded CSV file into a DataFrame
            data = pd.read_csv(uploaded_file)

            # Translate and summarize the last news detail
            if not data.empty and 'Detail' in data.columns:
                last_row_index = data.index[-1]
                last_news_detail = data.at[last_row_index, 'Detail']

                # Translate the last news detail from Telugu to English
                translator = Translator()
                translated_text = translator.translate(last_news_detail, src='te', dest='en').text

                # Summarize the translated text
                summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
                summary = summarizer(
                    translated_text,
                    max_length=70,
                    min_length=5,
                    do_sample=True
                )

                # Extract the summary text
                translated_summary = ' '.join([str(item['summary_text']) for item in summary])
                translated_summary = translator.translate(translated_summary, src='en', dest='te').text

                # Add the translated summary to the 'Summary' column of the last row
                data.at[last_row_index, 'Summary'] = translated_summary

                # Create a downloadable link for the modified CSV file
                output_buffer = io.StringIO()
                data.to_csv(output_buffer, index=False)
                csv_data = output_buffer.getvalue()
                response = Response(csv_data, content_type='text/csv')
                response.headers["Content-Disposition"] = "attachment; filename=news_with_summary.csv"
                return response
            else:
                return "No 'Detail' column found in the CSV file or the CSV file is empty."
        else:
            return "No file uploaded."
    except Exception as e:
        # Log the detailed error message
        traceback.print_exc()
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
