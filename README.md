# Mini Q&A System

A functional Q&A system that accepts user queries, performs real-time web search using the Google Custom Search API, and generates concise, coherent answers using Hugging Face Transformers. The system also provides citations from the sources used.

---

## Project Objectives

This project demonstrates a lightweight question-answering pipeline combining:

- Real-time web search
- Abstractive summarization using transformer-based models
- Basic frontend-backend integration
- Structured output with source transparency

---

## Tech Stack

- Backend: Python, Flask, Hugging Face Transformers, Google Custom Search API
- Frontend: HTML, CSS, JavaScript
- Language Model: facebook/bart-large-cnn

---

## Setup Instructions

### Backend Setup

1. Clone the repository:
   git clone https://github.com/gsaanchi/mini-qna.git  
   cd mini-qna

2. Install dependencies:
   pip install -r requirements.txt

3. Configure environment variables in a `.env` file:
   GOOGLE_API_KEY=your_api_key  
   GOOGLE_CSE_CX=your_search_engine_id

4. Run the Flask server:
   python app.py

---

### Frontend Setup

1. Create the following files:
   - index.html – for layout
   - style.css – for styling
   - script.js – for handling frontend logic

2. Open index.html in a browser or serve it through a local development server.

---

## How It Works

1. User submits a question through the input field.
2. The backend:
   - Validates the query
   - Calls the Google Search API and retrieves snippets from the top results
   - Combines and truncates the snippets
   - Passes the text to a summarization model (BART)
3. The system returns a concise answer along with the source links used to generate it.

---

## Example Interactions

User Input:  
What is generative AI?

System Output:  
Generative AI refers to models that can create new content such as text, images, and audio using deep learning techniques.

Sources:  
- Titles and links of the top 3–5 search results

---

### Screenshots

<img width="600" alt="input-example" src="https://github.com/user-attachments/assets/618b4650-3457-4a78-b064-ed0f1fd9842c" />

<img width="600" alt="output-example-1" src="https://github.com/user-attachments/assets/1de67719-d151-48cc-9b47-7a8eec496a5b" />

<img width="600" alt="output-example-2" src="https://github.com/user-attachments/assets/cbd824be-8e04-4ea9-a000-d6e891a19829" />

---

## Potential Improvements

- Add extractive summarization fallback
- Support document-based question answering (PDF input)
- Rank and filter sources by relevance
- Optional UI enhancements with modern JS frameworks
