from flask import Flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# takes POSTed JSON in the format {'search': 'search term'} and returns the text of the first paragraph of the wikipedia page that matches the search term
@app.route('/wiki-service', methods=['GET', 'POST'])
@cross_origin()
def wiki_service():
    if request.method == 'POST':
        data = request.get_json()
        search = data['search']
        page = requests.get('https://en.wikipedia.org/wiki/' + search)
        page = BeautifulSoup(page.content, 'html.parser')

        # get the first paragraph of the page
        body = page.find('div', {'id': 'mw-content-text'})
        body = body.find('div', {'class': 'mw-parser-output'})

        # for pages that don't exist
        if body is None:
            summary = 'No summary found'

        # some wikipedia pages have an empty first paragraph, so we need to get the first one that has text
        else:
            i = 0
            summary = body.findChildren('p', recursive=False)[i]
            while (summary.get_text() == '\n' or summary.get_text() == '' or summary.findChildren('span', {'id': 'coordinates'})):
                i += 1
                summary = body.findChildren('p', recursive=False)[i]
            summary = summary.get_text()
            summary = re.sub(r'\[[0-9]*\]', '', summary)

        return summary
    
    if request.method == 'GET':
        return 'Running'
    
if __name__ == '__main__':
    app.run()