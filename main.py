import copy
import json
from flask import Flask, render_template, request, jsonify, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
import os
import api_communicator
import random
import ast

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
        session['quotations'] = test['quotations']
        return display_results(test)

    return render_template("index.html", form=form)


@app.route("/search_results")
def display_results(results):
    return render_template("search_results.html", results=results)

@app.route("/select_difficulty")
def select_difficulty():
    return render_template("select_difficulty.html")


@app.route("/learn_quotations", methods=["GET", "POST"])
def learn_quotations():
    quotations_to_learn = session.get('quotations', None)

    for quotation in quotations_to_learn:
        quotation_as_list = quotation['quotation'].split()
        quotation['quotation'] = quotation_as_list

    quotations_to_edit = copy.deepcopy(quotations_to_learn)
    quotations_to_complete = {'quotations': []}

    for quotation in quotations_to_edit:
        to_remove = random.randint(0, int(len(quotation['quotation']) - 1))
        quotation_to_complete = quotation
        quotation_to_complete['quotation'][to_remove] = 'X'
        quotations_to_complete['quotations'].append(quotation_to_complete)

    if request.method == 'POST':
        request_info = request.values.to_dict()
        print(request_info)
        quotations_from_page = ast.literal_eval(request_info['quotations'])


        for entry in quotations_from_page['quotations']:
            index = quotations_from_page['quotations'].index(entry)
            gap_to_fill = entry['quotation'].index('X')
            entry['quotation'][gap_to_fill] = request_info[str(index)]

        print(quotations_from_page['quotations'])
        print(quotations_to_learn)

        if quotations_from_page['quotations'] == quotations_to_learn:
            print('Woohoo!')

            #The below code will be used for a quick fire game for a single quotation, this will be a separate option though.

        #if quotations_from_page['quotations'] == quotations_to_learn:
         #   print('Woohoo!')
          #  coaching_message = random.choice(['You got it! Keep going!', 'Amazing! Keep it up', "You're smashing it bro!", "My Guy!", "I see you shining..."])
          #  return render_template("learn_quotations.html", quotations=quotations_to_complete, space=" ", coaching_message=coaching_message, result="Correct")
        #else:
         #   coaching_message = random.choice(["missed it, but keep going!", "We miss 100% of the shots we never take", "fuck the haters, keep grinding"])
          #  return render_template("learn_quotations.html", quotations=quotations_to_complete, space= " ", coaching_message=coaching_message, result="Incorrect")

    return render_template("learn_quotations.html", quotations=quotations_to_complete, space=" ")

if __name__ == "__main__":
    app.run(debug=True)
