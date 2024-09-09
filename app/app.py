# Import modules
from flask import Flask, jsonify, render_template, request, make_response
from transformers import MistralForCausalLM, AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer, AutoModel
import torch
import transformers
import requests

app = Flask(__name__)

listOfKeys = ["Ishreet1/FinanceLLM"]


# Function to get prediction based on the input message and model
'''
@param message: str, model: AutoModel
'''
def get_prediction(message, model):
    # Inference
    results = model(message)  
    return results


# Function to render the home page
'''
@method: GET
@return: render_template
'''
@app.route('/', methods=['GET'])
def get():
    # in the select we will have each key of the list in option
    return render_template("home.html", len = len(listOfKeys), listOfKeys = listOfKeys)


# Function to get the prediction based on the input message and model
'''
@method: POST
@return: render_template
'''
@app.route('/', methods=['GET', 'POST'])
def predict():
    
    if request.method == 'POST':
        # Get the model name from the form
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": request.form['message']}]
            }
        
        # API URL for accessing model
        api_url = "http://127.0.0.1:8000/v1/chat/completions"
            
        # Headers for the API
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        # Send the request to the API
        response = requests.post(api_url, headers=headers, json=data)
        response_data = response.json()
        choices = response_data.get("choices", [])
        message_content = choices[0].get("message", {}).get("content", "")

        return render_template('result.html', text = request.form['message'], prediction = message_content)
    
    # Handling GET requests, returning JSON as a response
    else:
        return """{
            "object": "list",
            "data": [
                {
                "id": "instructlab-merlinite-7b-lab-trained/instructlab-merlinite-7b-lab-Q4_K_M.gguf",
                "object": "model",
                "owned_by": "me",
                "permissions": []
                }
            ]
            }"""


# Main function
if __name__ == '__main__':
    # starting app
    app.run(debug=True,host='0.0.0.0')

