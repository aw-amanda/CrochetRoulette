from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import requests
from urllib.parse import quote
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
api = Api(app)

# Get API Key and Engine ID from environment variables
API_KEY = os.getenv("API_KEY")
ENGINE_ID = os.getenv("ENGINE_ID")

class SearchPattern(Resource):
    def get(self):
        project = request.args.get('project')

        # Build and encode the query
        query = f"{project} crochet pattern OR crochet project"
        encoded_query = quote(query)
        url = f"https://www.googleapis.com/customsearch/v1?q={encoded_query}&key={API_KEY}&cx={ENGINE_ID}"

        # Make the API request
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get('items', [])
            if results:
                return jsonify({"url": results[0]['link']})
        return jsonify({"url": "No result found."})

api.add_resource(SearchPattern, '/search')

if __name__ == '__main__':
    app.run(debug=True)