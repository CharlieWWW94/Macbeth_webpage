import copy
import json
from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
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

    # This section of code creates the gap-fill exercises

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

    # This section of code processes the result

    if request.method == 'POST':
        request_info = request.values.to_dict()
        quotations_from_page = ast.literal_eval(request_info['quotations'])

        for entry in quotations_from_page['quotations']:
            index = quotations_from_page['quotations'].index(entry)
            gap_to_fill = entry['quotation'].index('X')
            entry['quotation'][gap_to_fill] = request_info[str(index)]



        return redirect(url_for("quiz_results", submitted_answers=quotations_from_page["quotations"], quotations_to_learn=quotations_to_learn))


        #At this point let's redirect to a results page. Be sure to pass in both quotations from page and quotations to learn.


        #if quotations_from_page['quotations'] == quotations_to_learn:
         #   print('Woohoo!')

            # The below code will be used for a quick fire game for a single quotation, this will be a separate option though.

        # if quotations_from_page['quotations'] == quotations_to_learn:
        #   print('Woohoo!')
        #  coaching_message = random.choice(['You got it! Keep going!', 'Amazing! Keep it up', "You're smashing it bro!", "My Guy!", "I see you shining..."])
        #  return render_template("learn_quotations.html", quotations=quotations_to_complete, space=" ", coaching_message=coaching_message, result="Correct")
        # else:
        #   coaching_message = random.choice(["missed it, but keep going!", "We miss 100% of the shots we never take", "fuck the haters, keep grinding"])
        #  return render_template("learn_quotations.html", quotations=quotations_to_complete, space= " ", coaching_message=coaching_message, result="Incorrect")

    return render_template("learn_quotations.html", quotations=quotations_to_complete, space=" ")


@app.route("/quiz_results/<submitted_answers>/<quotations_to_learn>", methods=["GET", "POST"])
def quiz_results(submitted_answers, quotations_to_learn):

    submitted_answers_list = ast.literal_eval(submitted_answers)
    quotations_to_learn_list = ast.literal_eval(quotations_to_learn)
    print(type(submitted_answers_list))

    if type(submitted_answers_list) != list:
        submitted_answers_list = [submitted_answers_list]
        quotations_to_learn_list = [quotations_to_learn_list]
        print(submitted_answers_list)

    for entry in submitted_answers_list:
        entry_index = submitted_answers_list.index(entry)
        if entry == quotations_to_learn_list[entry_index]:
            entry['quotation'] = " ".join(entry['quotation'])
            entry['correct'] = 1
            print(entry)
        else:
            entry['correct'] = 0
            entry_location = submitted_answers_list.index(entry)
            entry['correct_answer'] = " ".join(quotations_to_learn_list[entry_location]['quotation'])
            entry['quotation'] = " ".join(entry['quotation'])

    return render_template("quiz_results.html", answers=submitted_answers_list, to_learn=quotations_to_learn)





if __name__ == "__main__":
    app.run(debug=True)
