import openai
import os
from flask import Flask, render_template, request, Markup
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap
from form.InputPromptForm import InputPromptForm


load_dotenv()  # take environment variables from .env.

SECRET_KEY = os.getenv("SECRET_KEY")
API_KEY = os.getenv("API_KEY")
PORT = os.getenv("PORT")

app = Flask(__name__)

Bootstrap(app)

app.config['SECRET_KEY'] = SECRET_KEY
openai.api_key = "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"


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
    message = ""
    prompt = ""

    if request.method == "POST":
        prompt = request.form.get("prompt")

        if (prompt.strip(" ") != ""):
            print("-------------")
            print("prompt:", prompt, "END")

            # get chatbot response
            message = call_openai(prompt).replace("\n", "<br>")
            # message = "one<br>two<br>three"
            message = Markup(message)

            print("message:", message)

    return render_template('index.html', form=form, message=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, threaded=True, debug=True)
