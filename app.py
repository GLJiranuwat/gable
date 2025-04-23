from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from readability import Document
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = 'AIzaSyDcTr-I7uai-_FiDaUlooYOw0ImTClo9mA'
SEARCH_ENGINE_ID = '83dd639853d3e4a2b&q'

def google_search(query):
    url = f'https://www.googleapis.com/customsearch/v1?key=AIzaSyDcTr-I7uai-_FiDaUlooYOw0ImTClo9mA&cx=83dd639853d3e4a2b&q={query}'
    res = requests.get(url).json()
    print(res['items'][0]['link'])
    return res['items'][0]['link'] if 'items' in res else None

def extract_clean_content(url):
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    doc = Document(res.text)
    soup = BeautifulSoup(doc.summary(), 'html.parser')
    return soup.get_text(strip=True)

@app.route('/extract', methods=['POST'])
def extract():
    data = request.get_json()
    query = data.get('text')
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

if __name__ == '__main__':
    app.run()
