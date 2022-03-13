from flask import Flask, render_template, request, jsonify, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
import os
import api_communicator
import random
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap(app)


class SearchForm(FlaskForm):
    theme = SelectField('Theme', choices=['All', 'Ambition', 'Bravery', 'Witchcraft', 'Equivocation'])
    character = SelectField('Character', choices=['All', 'Macbeth', 'Lady Macbeth', 'First Witch', 'Captain'])
    act = SelectField('Act', choices=['All', 1, 2])
    scene = SelectField('Scene', choices=['All', 1, 2, 3, 4, 5])
    submit = SubmitField('Submit')


@app.route("/", methods=["GET", "POST"])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        list_search_params = list(form.data.items())
        test = api_communicator.search(list_search_params)
        print(test)
        session['quotations'] = test['quotations']
        return display_results(test)

    return render_template("index.html", form=form)


@app.route("/search_results")
def display_results(results):
    return render_template("search_results.html", results=results)


@app.route("/learn_quotations", methods=["GET"])
def learn_quotations():
    quotations_to_learn = session.get('quotations', None)
    for quotation in quotations_to_learn:
        quotation_as_list = quotation['quotation'].split()
        quotation['quotation'] = quotation_as_list

    quotations_to_complete = {'quotations': []}
    for quotation in quotations_to_learn:
        to_remove = random.randint(0, int(len(quotation['quotation']) - 1))
        quotation_to_complete = quotation
        quotation_to_complete['quotation'][to_remove] = 'X'
        print(quotation_to_complete)
        quotations_to_complete['quotations'].append(quotation_to_complete)
    print(quotations_to_complete)

    return render_template("learn_quotations.html", quotations=quotations_to_complete)


if __name__ == "__main__":
    app.run(debug=True)
