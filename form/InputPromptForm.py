from flask_wtf import FlaskForm
from wtforms import (StringField)


class InputPromptForm(FlaskForm):
    prompt = StringField("Prompt",  render_kw={"placeholder": "Prompt"})
    newAPI = StringField("OpenAI API Key",  render_kw={
                         "placeholder": "OpenAI API Key"})
