import os

try:
    import openai
    from flask import Flask, render_template, request, Markup
    from dotenv import load_dotenv, set_key, find_dotenv
    from flask_bootstrap import Bootstrap
    from form.InputPromptForm import InputPromptForm
except Exception:
    # import all package
    os.system("pip install -r requirements.txt")

    import openai
    from flask import Flask, render_template, request, Markup
    from dotenv import load_dotenv, set_key, find_dotenv
    from flask_bootstrap import Bootstrap
    from form.InputPromptForm import InputPromptForm

load_dotenv()  # take environment variables from .env.

SECRET_KEY = os.getenv("SECRET_KEY")
PORT = os.getenv("PORT")
API_KEY = os.getenv("API_KEY")
MODEL_ENGINE = os.getenv("MODEL_ENGINE")
MAX_TOKENS = os.getenv("MAX_TOKENS")
TEMPERATURE = os.getenv("TEMPERATURE")
TOP_P = os.getenv("TOP_P")
FREQUENCY_PENALTY = os.getenv("FREQUENCY_PENALTY")
PRESENCE_PENALTY = os.getenv("PRESENCE_PENALTY")

app = Flask(__name__)

Bootstrap(app)

app.config['SECRET_KEY'] = SECRET_KEY

# Setup api key
API_KEY = os.getenv("API_KEY")
openai.api_key = API_KEY

# Define a list to store the conversation history
conversation_history = []


def generate_response(history):
    # Combine the conversation history into a single string
    # Use the last 5 messages as context
    prompt = "\n".join(history[-5:])

    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        engine=MODEL_ENGINE,
        prompt=prompt,
        max_tokens=int(MAX_TOKENS),
        temperature=float(TEMPERATURE),
        top_p=float(TOP_P),
        frequency_penalty=float(FREQUENCY_PENALTY),
        presence_penalty=float(PRESENCE_PENALTY),
    )

    # Extract the response
    message = response.choices[0].text.lstrip(
        "?!").strip().replace("\n", "<br>").replace("\"", "\'")

    return message


@app.route('/', methods=['GET', 'POST'])
def main():
    form = InputPromptForm()
    checkAPI = True
    response = ""
    prompt = ""
    error = ""

    if request.method == "POST":
        prompt = request.form.get("prompt")
        newAPI = request.form.get("newAPI")

        if (prompt and prompt.strip(" ") != ""):

            # get chatbot response
            try:
                # Add the user's message to the conversation history
                conversation_history.append(prompt)

                # Generate a response
                response = generate_response(conversation_history)

                # Add the bot's response to the conversation history
                conversation_history.append(response)
            except Exception as e:
                print("Error:", e)
                if "Incorrect API key provided" in str(e):
                    print("key:", os.getenv("API_KEY"))
                    response = "Incorrect API key provided"
                    checkAPI = False
                else:
                    error = e

            # checkAPI = False
            response = Markup(response)

            print("GPT:", response)

        if (newAPI):
            API_KEY = newAPI
            openai.api_key = API_KEY

            dotenv_file = find_dotenv()
            set_key(dotenv_file, "API_KEY", API_KEY)

            print("newAPI:", newAPI, "END")

    return render_template('index.html', form=form, message=response, checkAPI=checkAPI, error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, threaded=True, debug=True)
