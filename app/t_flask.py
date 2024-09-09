'''
Description: This file contains the code for the Flask application that will 
serve the model.
'''

# Import modules
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Create a Flask app
app = Flask(__name__)

# Set the device to CUDA if available, otherwise fall back to CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the model and tokenizer globally, move model to the appropriate device
model = AutoModelForCausalLM.from_pretrained("Ishreet1/FinanceLLM", torch_dtype=torch.float16).to(device)
tokenizer = AutoTokenizer.from_pretrained("Ishreet1/FinanceLLM")


# Function to generate a response based on the input messages
'''
@method: GET, POST
@return: jsonify
'''
@app.route('/predict', methods=['GET', 'POST'])
def predict():
	if request.method == 'GET':
		messages = "What colour is an apple?"

		# Check if messages are provided
		if not messages:
			return jsonify({"error": "No messages provided"}), 400

		try:
			# Encode the messages
			inputs = tokenizer(messages, return_tensors="pt", padding=True)

			# Move inputs to the same device as the model
			inputs = inputs.to(device)

			# Generate response from the model
			generated_ids = model.generate(**inputs, max_new_tokens=10, do_sample=True)
			decoded = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

			# Return the model output
			return jsonify({"response": decoded[0]})
		except Exception as e:
			return jsonify({"error": str(e)}), 500


# Function to check the health of the service
'''
@method: GET
@return: jsonify
'''
@app.route('/health', methods=['GET'])
def health_check():
	return jsonify({"status": "ok", "message": "infer service is ready"}), 200

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port=8080)
