from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Route to serve the chatbot UI
@app.route('/')
def index():
    return render_template('index.html')

# API route to handle user questions
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    user_question = request.json.get('question')  # Get the user's question from the request

    # Define the AnythingLLM endpoint
    anythingllm_url = 'http://localhost:3001/api/v1/workspace/job_keyword_extractor/chat'
    
    payload = {
    "message": user_question,
    "mode": "chat",
    "sessionId": "identifier-to-partition-chats-by-external-id"
    }
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer X7CK00F-K764AVE-KBSF5Q7-ET2JKRH'
    }
    
    # Forward the question to AnythingLLM
    try:
        # Send the request to AnythingLLM with the user's question
        response = requests.post(anythingllm_url, headers=headers, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            anythingllm_response = response.json().get('textResponse', 'No response from AnythingLLM')
        else:
            anythingllm_response = "Error: Could not get a valid response from AnythingLLM."

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        anythingllm_response = "Error: Could not connect to AnythingLLM server."
        
    # chatbot_response = "This is a sample response from the chatbot."

    # Return the response from AnythingLLM back to the client
    return jsonify({"response": anythingllm_response})
    # return jsonify({"response": chatbot_response})

if __name__ == '__main__':
    app.run(debug=True, port=3000)