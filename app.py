from flask import Flask, request, jsonify
from mysql.connector import connect, Error
import nltk
from nltk.tokenize import word_tokenize
import re
import datetime

nltk.download("popular")

app = Flask(__name__)

start_time = datetime.datetime.now()
end_time = datetime.datetime.now()
processing_time = end_time - start_time
text_processing = processing_time.total_seconds()
text_processing = int(text_processing)


# Database connection function


def create_db_connection():
    connection = None
    try:
        connection = connect(
            host="localhost",
            user="root",
            password="12345678",
            database="datamining"
        )
        print("Database connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# API endpoint for file upload


@app.route('/api/v1/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    text_collections = file.read().decode('utf-8')

    # ... bagian kode lainnya ...

    # Menghitung lamanya waktu pemrosesan data
    start_time = datetime.datetime.now()

    # Convert the text to lowercase
    text_collections = text_collections.lower()

    # Tokenize the text
    tokens = word_tokenize(text_collections)

    # Remove symbols and other unwanted characters
    cleaned_tokens = [re.sub(r'\W+', '', token) for token in tokens]

    # Remove empty tokens
    cleaned_tokens = [token for token in cleaned_tokens if token]

    # Join the cleaned tokens back into a string
    cleaned_text = ' '.join(cleaned_tokens)

    # Menghitung lamanya waktu pemrosesan data
    end_time = datetime.datetime.now()
    processing_time = end_time - start_time
    text_processing = int(processing_time.total_seconds())

    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO data_collection (text_collections, text_processing) VALUES (%s, %s)"
        values = (cleaned_text, text_processing)
        cursor.execute(query, values)
        connection.commit()

        return 'File uploaded successfully'
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()


# Run the application at http://localhost:5000/
if __name__ == '__main__':
    app.run(debug=True)
