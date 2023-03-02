import openai
import os
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

print("from .env:", SECRET_KEY, PORT, API_KEY, MODEL_ENGINE,
      MAX_TOKENS, TEMPERATURE, FREQUENCY_PENALTY, PRESENCE_PENALTY)
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
                # message = "\n\n#include <stdio.h>\n\nint main(void)\n{\n    printf(\"Hello, World!\\n\");\n    return 0;\n}".replace(
                #     "\n", "<br>").replace("\"", "\`")
                # message = "one<br>two<br>three"
                # message = "![alt text](https: // upload.wikimedia.org/wikipedia/commons/thumb/9/97/The_Earth_seen_from_Apollo_17.jpg/220px-The_Earth_seen_from_Apollo_17.jpg)"
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


# "\n\n<!DOCTYPE html>\n<html>\n<head>\n    <title>Web Commercial</title>\n    <style>\n        body {\n            background-color: #eee;\n            font-family: sans-serif;\n            font-size: 1.2em;\n        }\n\n        .commercial {\n            margin: auto;\n            width: 900px;\n            padding: 20px; \n            background-color: #fff; \n            border-radius: 5px; \n        }\n\n        h1 {\n            font-size: 2.5em; \n            font-weight: bold; \n            color: #444; \n        }\n\n        p {\n            margin: 10px 0; \n        }\n\n        .product-image {\n            float: left; \n            margin-right: 20px; \n        }\n\n        .product-description {\n            float: left; \n            width: 600px; \n        }\n\n        .product-price {\n            font-size: 1.5em; \n            font-weight: bold; \n            color: #009900; \n        }\n\n    </style>\n</head>\n<body>\n\n    <div class=\"commercial\">\n\n        <h1>Introducing the all new Product X!</h1>\n\n        <div class=\"product\">\n\n            <div class=\"product-image\">\n                <img src=\"product_x.jpg\" alt=\"Product X\" />  \n            </div>\n\n            <div class=\"product-description\">\n\n                <p>Product X is the latest innovation in technology that you won't want to miss out on! With features like...</p>\n\n                <ul>\n                    <li>Feature 1</li> \n                    <li>Feature 2</li> \n                    <li>Feature 3</li> \n                </ul>\n\n                <p class=\"product-price\">Only $99.99!</p>\n\n                <p><a href=\"#\">Order now!</a></p>\n\n            </div>\n\n        </div> <!-- end product -->\n\n    </div><!-- end commercial -->    \n    \n</body>  \n</html>"
