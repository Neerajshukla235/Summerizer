import pandas as pd
import nltk
from googletrans import Translator
nltk.download('punkt')  # Download NLTK's sentence tokenizer
from transformers import pipeline
data= pd.read_csv('/Users/neerajshukla/PycharmProjects/Web scrapper bot/news.csv')

# Load the CSV data into a DataFrame
data = pd.read_csv('/Users/neerajshukla/PycharmProjects/Web scrapper bot/news.csv')

# Select the last scrapped news
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

# Save the modified DataFrame back to the CSV file
data.to_csv('/Users/neerajshukla/PycharmProjects/Web scrapper bot/news_with_summery.csv', index=False)




