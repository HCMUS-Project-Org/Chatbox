import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap

load_dotenv()  # take environment variables from .env.

API_KEY = os.getenv("API_KEY")
PORT = os.getenv("PORT")

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, threaded=True, debug=True)
