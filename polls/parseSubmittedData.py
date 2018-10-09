

def parse_variables_definition(submitted_data):
    # Process variables definitions from the form
    '''
    :param submitted_data: The submitted data from the form
    :return: the parsed (variables_names, variables_definitions, variables_values)
    '''
    variables_definitions = dict()
    variables_names = dict()
    variables_values = dict()
    for datum in submitted_data:
        if ("var_name" in datum):
            if str(submitted_data[datum]) != '':
                variables_names[datum.split("_")[2]] = str(submitted_data[datum])
        if ("var_val" in datum):
            if str(submitted_data[datum]) != '':
                variables_values[datum.split("_")[2]] = str(submitted_data[datum])
    for index in variables_names:
        variables_definitions[variables_names[index]] = variables_values[index]
    return variables_names, variables_definitions, variables_values