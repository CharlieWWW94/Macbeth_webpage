from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap(app)


class SearchForm(FlaskForm):
    theme = SelectField('Theme', choices=['Ambition', 'Witchcraft', 'Equivocation'])
    character = SelectField('Character', choices=['Macbeth', 'Lady Macbeth', 'First Witch'])
    act = SelectField('Act', choices=[1, 2])
    scene = SelectField('Scene', choices=[1, 2, 3, 4, 5])
    submit = SubmitField('Submit')


@app.route("/", methods=["GET", "POST"])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        list_search_params = list(form.data.items())
        print(list_search_params)

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
