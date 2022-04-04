import copy
import random


def create_gaps(quotations_to_learn, difficulty):
    for quotation in quotations_to_learn:
        quotation_as_list = quotation['quotation'].split()
        quotation['quotation'] = quotation_as_list

    quotations_to_edit = copy.deepcopy(quotations_to_learn)
    quotations_for_completion = {'quotations': []}

    if difficulty == 'easy':
        for quotation in quotations_to_edit:
            to_remove = random.randint(0, int(len(quotation['quotation']) - 1))
            quotation_to_complete = quotation
            quotation_to_complete['quotation'][to_remove] = 'X'
            quotations_for_completion['quotations'].append(quotation_to_complete)

    elif difficulty == 'medium':

        for quotation in quotations_to_edit:
            for num in range(0, len(quotation) // 2):
                to_remove = random.randint(0, int(len(quotation['quotation']) - 1))
                quotation_to_complete = quotation
                quotation_to_complete['quotation'][to_remove] = 'X'
            quotations_for_completion['quotations'].append(quotation_to_complete)

    elif difficulty == 'hard':

        for quotation in quotations_to_edit:
            for num in range(0, len(quotation) - 2):
                to_remove = random.randint(0, int(len(quotation['quotation']) - 1))
                quotation_to_complete = quotation
                quotation_to_complete['quotation'][to_remove] = 'X'
            quotations_for_completion['quotations'].append(quotation_to_complete)

    return quotations_for_completion

def verify_answers(answers):
    pass