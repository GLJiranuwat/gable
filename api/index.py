from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from readability import Document

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = 'AIzaSyDcTr-I7uai-_FiDaUlooYOw0ImTClo9mA'
SEARCH_ENGINE_ID = '83dd639853d3e4a2b'

def google_search(query):
    url = f'https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}'
    res = requests.get(url).json()
    print(res.get('items', [{}])[0].get('link'))
    return res.get('items', [{}])[0].get('link')

def extract_clean_content(url):
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    doc = Document(res.text)
    soup = BeautifulSoup(doc.summary(), 'html.parser')
    return soup.get_text(strip=True)

@app.route('/extract', methods=['POST'])
def extract():
    try:
        print("Headers:", request.headers)
        print("Raw Data:", request.data)
        data = request.get_json()
        print("Parsed JSON:", data)
    except Exception as e:
        return jsonify({'error': f'Invalid JSON format: {str(e)}'}), 400

    query = data.get('text') if data else None
    if not query:
        return jsonify({'error': 'Missing text field'}), 400

    url = google_search(query)
    if not url:
        return jsonify({'error': 'No search result found'}), 404

    try:
        content = extract_clean_content(url)
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel will look for this
app = app
