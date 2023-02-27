from flask_wtf import FlaskForm
from wtforms import (StringField)


class InputPromptForm(FlaskForm):
    prompt = StringField("Name",  render_kw={"placeholder": "Prompt"})
