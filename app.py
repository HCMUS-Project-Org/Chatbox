import os

try:
    import openai
    from flask import Flask, render_template, request, Markup
    from dotenv import load_dotenv, set_key, find_dotenv
    from flask_bootstrap import Bootstrap
    from form.InputPromptForm import InputPromptForm
except:
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
FREQUENCY_PENALTY = os.getenv("FREQUENCY_PENALTY")
PRESENCE_PENALTY = os.getenv("PRESENCE_PENALTY")

app = Flask(__name__)

Bootstrap(app)
# sk-4FpBCSHWvehW6OwbA5sfT3BlbkFJMo4fJRyIS5baZrhN0Y
app.config['SECRET_KEY'] = SECRET_KEY
openai.api_key = API_KEY


print("key:", API_KEY)


def call_openai(prompt):
    # Generate text with the GPT-3 model
    response = openai.Completion.create(
        engine=MODEL_ENGINE,
        prompt=prompt,
        max_tokens=int(MAX_TOKENS),
        temperature=float(TEMPERATURE),
        frequency_penalty=float(FREQUENCY_PENALTY),
        presence_penalty=float(PRESENCE_PENALTY),
        # stop=["\"\"\""]
    )
    print("response:", response)

    message = response.choices[0].text.lstrip(
        "?!").strip().replace("\n", "<br>").replace("\"", "\'")

    return message


@app.route('/', methods=['GET', 'POST'])
def main():
    form = InputPromptForm()
    checkAPI = True
    message = ""
    prompt = ""
    error = ""

    if request.method == "POST":
        prompt = request.form.get("prompt")
        newAPI = request.form.get("newAPI")

        if (prompt and prompt.strip(" ") != ""):

            # get chatbot response
            try:
                message = call_openai(prompt)

            except Exception as e:
                print("Error:", e)
                if "Incorrect API key provided" in str(e):
                    print("key:", os.getenv("API_KEY"))
                    message = "Incorrect API key provided"
                    checkAPI = False
                else:
                    error = e

            # checkAPI = False
            message = Markup(message)

            print("message:", message)

        if (newAPI):
            API_KEY = newAPI
            openai.api_key = API_KEY

            dotenv_file = find_dotenv()
            set_key(dotenv_file, "API_KEY", API_KEY)

            print("newAPI:", newAPI, "END")

    return render_template('index.html', form=form, message=message, checkAPI=checkAPI, error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, threaded=True, debug=True)
