from flask import Flask, render_template, request, redirect, url_for
from agric_bot import AgricultureBot
from gemini_api import GeminiAPI
import requests

app = Flask(__name__)

# Initialize the Agriculture Bot and Agriculture API
agriculture_bot = None  # Initialize as None for lazy loading
gemini_api = None  # Initialize as None for lazy loading

def get_agriculture_bot():
    global agriculture_bot
    if agriculture_bot is None:
        agriculture_bot = AgricultureBot()
    return agriculture_bot

def get_gemini_api():
    global gemini_api
    if gemini_api is None:
        gemini_api = GeminiAPI()
    return gemini_api

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
    email = request.form['email']
    if email:
        zapier_webhook_url = "https://hooks.zapier.com/hooks/catch/19332064/223pmxy/"
        data = {'email': email}
        response = requests.post(zapier_webhook_url, json=data)
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
            return "Failed to subscribe. Please try again."
    else:
        return "Please enter a valid email address."

def get_response(user_input):
    agriculture_advice = get_agriculture_bot().get_agricultural_advice(user_input)
    
    try:
        agriculture_response = get_gemini_api().generate_response(user_input)
    except Exception as e:
        print(f"Error accessing response: {str(e)}")
        agriculture_response = "There was an error processing your request. Please try again."

    return agriculture_advice, agriculture_response

if __name__ == '__main__':
    app.run(debug=True)
