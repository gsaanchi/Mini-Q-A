from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests
from transformers import pipeline
from flask_cors import CORS
import logging
import asyncio
import re


load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

#logging
logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv('GOOGLE_API_KEY')
CX_ID = os.getenv('GOOGLE_CSE_CX')
if not API_KEY or not CX_ID:
    logging.error("API_KEY or CX_ID environment variable is missing")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

async def google_search(query):
    """
    Performs a Google Custom Search asynchronously for the given query and returns results.
    """
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX_ID}&q={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()
        search_results = [
            {"title": item["title"], "link": item["link"], "snippet": item["snippet"]}
            for item in results.get("items", [])
        ]
        return search_results
    except requests.exceptions.RequestException as e:
        logging.error(f"Google Search API request failed: {e}")
        return []

def validate_query(query):
    """
    Sanitizes and validates the query to prevent unwanted characters or issues.
    """
    return re.sub(r'[^\w\s]', '', query)

async def generate_answer_with_sources(query):
    """
    Generates an answer with sources for the given query.
    """
    query = validate_query(query)
    search_results = await google_search(query)

    if not search_results:
        return {"answer": "No relevant information found.", "sources": []}

    combined_snippets = " ".join(result["snippet"] for result in search_results)[:1000]

    try:
        summary = summarizer(combined_snippets, max_length=100, min_length=30, do_sample=False)[0]["summary_text"]
    except Exception as e:
        logging.error(f"Summarization failed: {e}")
        summary = "Could not summarize the information. Try refining your query."

    response_data = {
        "answer": summary,
        "sources": [
            {"title": result["title"], "link": result["link"], "snippet": result["snippet"]}
            for result in search_results
        ]
    }
    return response_data

@app.route("/generate_answer", methods=["POST"])
async def generate_answer():
    """
    API endpoint to get an answer and sources based on the query provided in JSON payload.
    """
    data = request.json
    query = data.get("query", "").strip()
    
    if not query:
        return jsonify({"error": "Query parameter is required."}), 400

    result = await generate_answer_with_sources(query)
    
    return jsonify(result)

# Run the Flask app
if __name__ == "__main__":
    # Set the port dynamically with a default value for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
