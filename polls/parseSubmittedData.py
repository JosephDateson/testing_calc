import re
import itertools
import parseConditions

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
    return dimensions_rows_conds_dict, dimensions_columns_conds_dict, strategies_constraints, payment_conds_dict, payment_conds, dimensions_rows_conds, dimensions_columns_conds

def generate_all_strategies_combinations(n,full_set):
    # Generate all combinations of size n from the set full_set
    full_set_list = []
    full_set_str = "[" + full_set + "]"
    exec "full_set_list="+full_set_str
    return set(itertools.combinations(full_set_list, n))

def generate_all_strategies_product(n,full_set):
    # Generate all tuples of size n from the set full_set
    full_set_list = []
    full_set_str = "[" + full_set + "]"
    exec "full_set_list="+full_set_str
    return list(itertools.product(full_set_list,repeat=n))

def convert_to_excel_conds(constraints):
    #Convert constraint condition to an excel condition
    converted_constraints = []
    for constraint in constraints:
        converted_constraints += ["=IF("+constraints[constraint]+",1,0)"]
    return converted_constraints

def is_satisfying_constraints(strategy,constraints):
    #Returns 0 if a given strategy doesn't satisfy all constraints, and 1 otherwise
    s = tuple(strategy)
    satisfied = False
    for constraint in constraints:
        exec "satisfied="+constraint
        if not(satisfied):
            return False
    return True

def filter_strategies_by_constraints(strategies, constraints):
    filtered_strategies = []
    for strategy in strategies:
        if is_satisfying_constraints(strategy,constraints):
            filtered_strategies+=[strategy]
    return filtered_strategies

def strategies_filter(strategies, constraints):
    constraints = parseConditions.parse_conditions(constraints)
    filtered_strategies = filter_strategies_by_constraints(strategies, constraints)
    return filtered_strategies

def parse_generator(submitted_data, variables_definitions, strategies_constraints):
    strategies_vectors = []
    dimensions_rows_categories_names = []
    dimensions_columns_categories_names = []

    strategies_full_set = ""
    if submitted_data["strategies_vector_single"] != '':
        tuples = re.findall("\(.+?\)", str(submitted_data["strategies_vector_single"]))
        new_single_vector = str(submitted_data["strategies_vector_single"])
        for tup in tuples:
            new_single_vector = new_single_vector.replace(tup, "")
        new_single_vector = new_single_vector.split(",")
        final_single_vector = []
        for item in new_single_vector:
            if item != '':
                final_single_vector += [item]
        final_single_vector += tuples
        for strategy in final_single_vector:
            strategy_with_variable = replace_variables_definitions(strategy, variables_definitions)
            strategies_vectors += [[eval(str(strategy_with_variable))]]
        strategies_vectors = [list(strategy[0]) if type(strategy[0]) == tuple else strategy for strategy in
                              strategies_vectors]
    elif submitted_data["strategies_upper_bound"] != '' and submitted_data["strategies_lower_bound"] != '':
        strategies_vectors = str([i for i in range(
            int(replace_variables_definitions(submitted_data["strategies_lower_bound"], variables_definitions)), int(
                replace_variables_definitions(submitted_data["strategies_upper_bound"],
                                              variables_definitions)) + 1)]).replace("[", "").replace("]", "").replace(
            " ", "")
    else:
        strategies_vectors_str = dict()
        strategies_vectors = []
        for datum in submitted_data:
            if ("vector" in datum) and not ("length" in datum):
                strategies_vectors_str[datum] = submitted_data[datum]
                if str(strategies_vectors_str[datum]) != '':
                    strategies_vectors += [[eval(str(strategies_vectors_str[datum]))]]
        strategies_vectors = [list(strategy[0]) if type(strategy[0]) == tuple else strategy for strategy in
                              strategies_vectors]
    for i in range(1, 11):
        field_name = "dimensions_row_category_name_" + str(i)
        if str(submitted_data[field_name]) != '':
            dimensions_rows_categories_names += [str(submitted_data[field_name])]
    dimensions_rows_categories_names = replace_variables_definitions_in_condition(dimensions_rows_categories_names,
                                                                                  variables_definitions)

    for i in range(1, 11):
        field_name = "dimensions_column_category_name_" + str(i)
        if str(submitted_data[field_name]) != '':
            dimensions_columns_categories_names += [str(submitted_data[field_name])]
    dimensions_columns_categories_names = replace_variables_definitions_in_condition(
        dimensions_columns_categories_names,
        variables_definitions)
    strategies_vector_length = 0
    strategies_full_set = ""
    for datum in submitted_data:
        if ("strategies_vector_length" in datum):
            if str(submitted_data[datum]) != '':
                strategies_vector_length = int(
                    replace_variables_definitions(submitted_data[datum], variables_definitions))
        if ("strategies_full_set" in datum):
            if str(submitted_data[datum]) != '':
                strategies_full_set = replace_variables_definitions(submitted_data[datum], variables_definitions)

    if (strategies_vector_length != 0):
        if strategies_full_set == "":
            strategies_full_set = replace_variables_definitions(strategies_vectors, variables_definitions)
        if "ignore permutations" in strategies_constraints:
            del strategies_constraints["ignore permutations"]
            all_strategies_generated = generate_all_strategies_combinations(strategies_vector_length,
                                                                            strategies_full_set)
        else:
            all_strategies_generated = generate_all_strategies_product(strategies_vector_length, strategies_full_set)
        strategies_constraints = convert_to_excel_conds(strategies_constraints)
        strategies_vectors = strategies_filter(all_strategies_generated, strategies_constraints)

    return strategies_vectors, dimensions_rows_categories_names, dimensions_columns_categories_names