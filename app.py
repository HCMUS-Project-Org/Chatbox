import openai
import os
from flask import Flask, render_template, request, Markup
from dotenv import load_dotenv, set_key, find_dotenv
from flask_bootstrap import Bootstrap
from form.InputPromptForm import InputPromptForm


load_dotenv()  # take environment variables from .env.

SECRET_KEY = os.getenv("SECRET_KEY")
API_KEY = os.getenv("API_KEY")
PORT = os.getenv("PORT")


app = Flask(__name__)

Bootstrap(app)
# sk-4FpBCSHWvehW6OwbA5sfT3BlbkFJMo4fJRyIS5baZrhN0Y
app.config['SECRET_KEY'] = SECRET_KEY
openai.api_key = API_KEY

print("key:", API_KEY)


def call_openai(prompt):
    # Set up the GPT-3 model
    model_engine = "text-davinci-002"

    # Generate text with the GPT-3 model
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text.strip()

    return message


@app.route('/', methods=['GET', 'POST'])
def main():
    form = InputPromptForm()
    checkAPI = True
    message = ""
    prompt = ""

    if request.method == "POST":
        prompt = request.form.get("prompt")
        newAPI = request.form.get("newAPI")

        if (prompt and prompt.strip(" ") != ""):

            # get chatbot response
            try:
                message = call_openai(prompt).replace("\n", "<br>")
            except Exception as e:
                print("Error:", e)
                if "Incorrect API key provided" in str(e):
                    print("key:", os.getenv("API_KEY"))
                    message = "Incorrect API key provided"
                    checkAPI = False

            # message = "one<br>two<br>three"
            # checkAPI = False
            message = Markup(message)

            print("message:", message)

        if (newAPI):
            API_KEY = newAPI
            openai.api_key = API_KEY

            dotenv_file = find_dotenv()
            set_key(dotenv_file, "API_KEY", API_KEY)

            print("newAPI:", newAPI, "END")

    return render_template('index.html', form=form, message=message, checkAPI=checkAPI)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, threaded=True, debug=True)
