from flask import Flask, render_template, request, jsonify
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, ChatSession

# Initialize Flask app
app = Flask(__name__)

# Initialize Vertex AI
vertexai.init(project="866939629489", location="us-central1")
model = GenerativeModel(
    "projects/866939629489/locations/us-central1/endpoints/3281304436609122304",
)

# Configure safety settings
safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

# Route for index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chat message generation
@app.route('/generate', methods=['POST'])
def generate_message():
    try:
        user_input = request.form['user_input']
        
        # Start a new chat session
        chat_session = model.start_chat()

        # Send user input to the model with generation settings
        response = chat_session.send_message(
            user_input,
            safety_settings=safety_settings
        )

        return jsonify({'response': response.text})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
