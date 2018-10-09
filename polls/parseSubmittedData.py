import re

# functions for variable definition
def replace_variables_definitions(value_with_variable ,variables_definitions):
    for variables_definition in variables_definitions:
        value_with_variable = value_with_variable.replace(variables_definition, variables_definitions[variables_definition])
    return value_with_variable

def replace_variables_definitions_in_condition(old_str_list, variables_definitions):
    for i in range(len(old_str_list)):
        new_str = old_str_list[i]
        for variables_definition in variables_definitions:
            new_str = re.sub(r"\b" + variables_definition + r"\b", variables_definitions[variables_definition],
                             new_str)
        old_str_list[i] = new_str
    return old_str_list

def parse_variables_definition(submitted_data):
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

def parse_conditions(submitted_data, variables_definitions):

    dimensions_rows_conds_dict = dict()
    dimensions_columns_conds_dict = dict()
    strategies_constraints = dict()
    payment_conds_dict = dict()
    payment_conds = []
    dimensions_rows_conds = []
    dimensions_columns_conds = []

    conditions = []
    for datum in submitted_data:
        if ("dimension" in datum) and ("row" in datum) and ("cond" in datum):
            if str(submitted_data[datum]) == 'else':
                last = str("\"" + submitted_data[datum.replace('cond', 'name').replace('if', 'category')] + "\"")
            elif str(submitted_data[datum]) != '':
                conditions += [str("IF(" + submitted_data[datum] + ",\"" + submitted_data[
                    datum.replace('cond', 'name').replace('if', 'category')] + "\",<next_condition>)")]

    for i in range(1, len(conditions)):
        conditions[i] = conditions[i].replace("<next_condition>", conditions[i - 1])
    dimensions_rows_conds_dict['dimensions_row_if_cond_1'] = "=" + conditions[len(conditions) - 1].replace(
        "<next_condition>", last)
    strategies_symbols = re.findall("[-,=><(](s[0-9a-z]+?|r[0-9a-z]+?)",
                                    dimensions_rows_conds_dict['dimensions_row_if_cond_1'])
    for symbol in strategies_symbols:
        dimensions_rows_conds_dict['dimensions_row_if_cond_1'] = dimensions_rows_conds_dict[
            'dimensions_row_if_cond_1'].replace(symbol, symbol[0] + "_" + symbol[1:])

    conditions = []
    for datum in submitted_data:
        if ("dimension" in datum) and ("column" in datum) and ("cond" in datum):
            if str(submitted_data[datum]) == 'else':
                last = str("\"" + submitted_data[datum.replace('cond', 'name').replace('if', 'category')] + "\"")
            elif str(submitted_data[datum]) != '':
                conditions += [str("IF(" + submitted_data[datum] + ",\"" + submitted_data[
                    datum.replace('cond', 'name').replace('if', 'category')] + "\",<next_condition>)")]

    for i in range(1, len(conditions)):
        conditions[i] = conditions[i].replace("<next_condition>", conditions[i - 1])
    dimensions_columns_conds_dict['dimensions_column_if_cond_1'] = "=" + conditions[len(conditions) - 1].replace(
        "<next_condition>", last)
    strategies_symbols = re.findall("[-,=><(](s[0-9a-z]+?|r[0-9a-z]+?)",
                                    dimensions_columns_conds_dict['dimensions_column_if_cond_1'])
    for symbol in strategies_symbols:
        dimensions_columns_conds_dict['dimensions_column_if_cond_1'] = dimensions_columns_conds_dict[
            'dimensions_column_if_cond_1'].replace(symbol, symbol[0] + "_" + symbol[1:])

    for datum in submitted_data:
        if str(submitted_data[datum]) != '':
            if "constraint" in datum:
                strategies_constraints[datum] = str(submitted_data[datum])
            if ("payment" in datum) and ("cond" in datum):
                payment_conds_dict[datum] = str(
                    "=IF(" + submitted_data[datum] + "," + submitted_data[datum.replace('cond', 'res')] + ",0)")

    for cond in payment_conds_dict:
        if payment_conds_dict[cond] != '':
            payment_conds += [payment_conds_dict[cond]]

    payment_conds_temp = []
    for cond in payment_conds:
        strategies_symbols = re.findall("[-,=><(](s[0-9a-z]+?|r[0-9a-z]+?)", cond)
        for symbol in strategies_symbols:
            cond = cond.replace(symbol, symbol[0] + "_" + symbol[1:])
        payment_conds_temp += [cond]
    payment_conds = payment_conds_temp
    payment_conds = replace_variables_definitions_in_condition(payment_conds, variables_definitions)

    for cond in dimensions_rows_conds_dict:
        if dimensions_rows_conds_dict[cond] != '':
            dimensions_rows_conds += [dimensions_rows_conds_dict[cond]]

    dimensions_rows_conds_temp = []
    for cond in dimensions_rows_conds:
        strategies_symbols = re.findall("[-,=><(](s[0-9a-z]+?|r[0-9a-z]+?)", cond)
        for symbol in strategies_symbols:
            cond = cond.replace(symbol, symbol[0] + "_" + symbol[1:])
        dimensions_rows_conds_temp += [cond]
    dimensions_rows_conds = dimensions_rows_conds_temp
    dimensions_rows_conds = replace_variables_definitions_in_condition(dimensions_rows_conds, variables_definitions)

    for cond in dimensions_columns_conds_dict:
        if dimensions_columns_conds_dict[cond] != '':
            dimensions_columns_conds += [dimensions_columns_conds_dict[cond]]

    dimensions_columns_conds_temp = []
    for cond in dimensions_columns_conds:
        strategies_symbols = re.findall("[-,=><(](s[0-9a-z]+?|r[0-9a-z]+?)", cond)
        for symbol in strategies_symbols:
            cond = cond.replace(symbol, symbol[0] + "_" + symbol[1:])
        dimensions_columns_conds_temp += [cond]
    dimensions_columns_conds = dimensions_columns_conds_temp
    dimensions_columns_conds = replace_variables_definitions_in_condition(dimensions_columns_conds,
                                                                          variables_definitions)