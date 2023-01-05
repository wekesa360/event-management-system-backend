def get_model_choices(choices):
    """
    takes model choices and convert to a list of choices
    """
    choices_value_list = []
    for i in range(len(choices)):
        choices_value_list.append(choices[i][0])
    return choices_value_list