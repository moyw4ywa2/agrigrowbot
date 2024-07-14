from flask import Flask, render_template, request, redirect, jsonify
import requests  # Add requests library for making HTTP requests
from agric_bot import AgricultureBot
from gemini_api import GeminiAPI

app = Flask(__name__)

# Initialize the Agriculture Bot and Agriculture API
agriculture_bot = AgricultureBot()
gemini_api = GeminiAPI()

@app.route('/')
def index():
    return render_template('index.html', agriculture_advice=None, agriculture_response=None)

@app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input:
            agriculture_advice, agriculture_response = get_response(user_input)
            return render_template('index.html', agriculture_advice=agriculture_advice, agriculture_response=agriculture_response)
        else:
            return "Please enter a question or describe an agricultural concern."

@app.route('/main_app')
def main_app():
    return redirect("https://www.example.com")

@app.route('/subscribe', methods=['POST'])
def subscribe():
    if request.method == 'POST':
        email = request.form['email']
        if email:
            # Send the email data to Zapier via webhook
            zapier_webhook_url = 'https://hooks.zapier.com/hooks/catch/19332064/223pmxy/'
            data = {'email': email}
            response = requests.post(zapier_webhook_url, json=data)

            # Optionally handle response from Zapier if needed
            if response.status_code == 200:
                return "Subscribed successfully!"
            else:
                return "Failed to subscribe. Please try again later."

        else:
            return "Please enter a valid email address."

def get_response(user_input):
    agriculture_advice = agriculture_bot.get_agricultural_advice(user_input)
    
    try:
        agriculture_response = gemini_api.generate_response(user_input)
        response_text = agriculture_response.text  # Attempt to access text attribute
    except Exception as e:
        print(f"Error accessing response text: {str(e)}")
        agriculture_response = None  # Handle the case where response is invalid or empty
        response_text = None
    
    return agriculture_advice, response_text

if __name__ == '__main__':
    app.run(debug=True)
