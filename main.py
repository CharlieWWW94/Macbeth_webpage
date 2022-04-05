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
import quote_manipulator

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


@app.route("/quick_learn/<target_quotation>", methods=["GET", "POST"])
def quick_learn(target_quotation, attempt_tally=1):

    if request.method == "POST":
        # this is all submitted info minus the target quotation
        quick_request_info = request.values.to_dict()
        new_tally = quick_request_info['attempt_tally']

        # This is the complete quotation to verify answer again. Type: list
        qf_dict_list = [ast.literal_eval(target_quotation)]

        # This is the quotation with Xs in it to replace with the submission
        qf_to_complete = ast.literal_eval(quick_request_info['old_target'])

        gap_to_fill = qf_to_complete['quotations'][0]['quotation'].index('X')
        qf_to_complete['quotations'][0]['quotation'][gap_to_fill] = quick_request_info[str("gap")]

        if qf_to_complete['quotations'][0] == qf_dict_list:
            pass
        quick_quotation_new = quote_manipulator.create_gaps(qf_dict_list, difficulty='easy')

        return render_template("quick_learn.html", quotation=quick_quotation_new, attempt_tally=int(new_tally),
                               original_quotation=qf_dict_list)

    quick_quotation_list = [ast.literal_eval(target_quotation)]
    quick_quotation = quote_manipulator.create_gaps(quick_quotation_list, difficulty='easy')

    return render_template("quick_learn.html", quotation=quick_quotation, attempt_tally=attempt_tally,
                           original_quotation=quick_quotation_list)


@app.route("/select_difficulty")
def select_difficulty():
    return render_template("select_difficulty.html")


@app.route("/learn_quotations/<difficulty>", methods=["GET", "POST"])
def learn_quotations(difficulty):
    quotations_to_learn = session.get('quotations', None)
    print(f"quoations to learn: {quotations_to_learn}")
    quotations_to_complete = quote_manipulator.create_gaps(quotations_to_learn, difficulty=difficulty)

    # This section of code processes the result

    if request.method == 'POST':
        request_info = request.values.to_dict()
        print(request_info)
        quotations_from_page = ast.literal_eval(request_info['quotations'])
        print(quotations_from_page)

        index = 0
        for entry in quotations_from_page['quotations']:
            print(entry)
            # index = quotations_from_page['quotations'].index(entry)
            for num in range(0, entry['quotation'].count('X')):
                gap_to_fill = entry['quotation'].index('X')
                entry['quotation'][gap_to_fill] = request_info[str(index)]
                index += 1

        return redirect(url_for("quiz_results", submitted_answers=quotations_from_page["quotations"],
                                quotations_to_learn=quotations_to_learn, difficulty=difficulty))

    return render_template("learn_quotations.html", difficulty=difficulty, quotations=quotations_to_complete, space=" ")


@app.route("/quiz_results/<submitted_answers>/<quotations_to_learn>/<difficulty>", methods=["GET", "POST"])
def quiz_results(submitted_answers, quotations_to_learn, difficulty):
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

    return render_template("quiz_results.html", answers=submitted_answers_list, to_learn=quotations_to_learn,
                           difficulty=difficulty)


if __name__ == "__main__":
    app.run(debug=True)
