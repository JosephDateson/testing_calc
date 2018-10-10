import pandas as pd
from src.pycel.excelcompiler import *

def not_strictly_increasing(L):
    return (all(x <= y for x, y in zip(L, L[1:])) and any(x < y for x, y in zip(L, L[1:])))
# }

# deprecated
# {
def not_strictly_decreasing(L):
    return (all(x >= y for x, y in zip(L, L[1:])) and any(x > y for x, y in zip(L, L[1:])))
# }

# deprecated
# {
#     def encode_conditions(conditions):
#         # Replaces proprietary expressions with strings in order to parse excel expressions
#         for i in range(len(conditions)):
#             conditions[i] = conditions[i].replace("(s)", '("s")')
#             conditions[i] = conditions[i].replace("(r)", '("r")')
#             exists = re.findall(r'(exists\(.*?\))', conditions[i], re.M | re.I)
#             for j in range(len(exists)):
#                 conditions[i] = conditions[i].replace(exists[j], '\"' + exists[j] + '\"')
#             for_each = re.findall(r'(foreach\(.*?\)),', conditions[i], re.M | re.I)
#             for j in range(len(for_each)):
#                 conditions[i] = conditions[i].replace(for_each[j], '\"' + for_each[j] + '\"')
#             percell = re.findall(r'(percell\(.*?\)),', conditions[i], re.M | re.I)
#             for j in range(len(percell)):
#                 conditions[i] = conditions[i].replace(percell[j], '\"' + percell[j] + '\"')
#             countcells = list(set(re.findall(r'(countcells\(.*?\))', conditions[i], re.M | re.I)))
#             for j in range(len(countcells)):
#                 conditions[i] = conditions[i].replace(countcells[j], '\"' + countcells[j] + '\"')
#             increasing = re.findall(r'(increasing\(\))', conditions[i], re.M | re.I)
#             for j in range(len(increasing)):
#                 conditions[i] = conditions[i].replace(increasing[j], '\"' + increasing[j] + '\"')
#             decreasing = re.findall(r'(decreasing\(\))', conditions[i], re.M | re.I)
#             for j in range(len(decreasing)):
#                 conditions[i] = conditions[i].replace(decreasing[j], '\"' + decreasing[j] + '\"')
#             percellcost = re.findall(r'(percellcost\(.*?\)),', conditions[i], re.M | re.I)
#             for j in range(len(percellcost)):
#                 conditions[i] = conditions[i].replace(percellcost[j], '\"' + percellcost[j] + '\"')
#             cell = re.findall(r'(cell\(.*?\)),', conditions[i], re.M | re.I)
#             for j in range(len(cell)):
#                 conditions[i] = conditions[i].replace(cell[j], '\"' + cell[j] + '\"')
#             sum = re.findall(r'(SUM\(.*?\))', conditions[i], re.M | re.I)
#         return conditions
#
#     def generate_quantifier_vector(quantifier, type='exists'):
#         '''Receive an exist condition and generate a boolean vector based on it's condition
#             Type can be either exists or for_each'''
#         exp_in_paranth = re.findall(r'' + type + '\((.*?\))\)', quantifier, re.M | re.I)
#         digits = re.findall(r'\((\d+)\)', quantifier, re.M | re.I)
#         if exp_in_paranth == []:
#             exp_in_paranth = re.findall(r'' + type + '\((.*?)\)', quantifier, re.M | re.I)
#         if len(exp_in_paranth) == 0:
#             return quantifier,quantifier
#         exp_in_paranth = exp_in_paranth[0].split(",")
#         for digit in digits:
#             if digit in exp_in_paranth:
#                 exp_in_paranth.remove(digit)
#         if len(exp_in_paranth) == 0:
#             return quantifier,quantifier
#         vecs = re.findall(r'(.)\[.\]', exp_in_paranth[-1], re.M | re.I)
#         condition_vec_exp = "1 " if (type in ['exists','percell'] ) else "not(0 "
#         if type=="percellcost":
#             condition_vec_exp = "1 " if (type == 'percellcost') else "not(0 "
#             condition_vec_exp += "in ["+exp_in_paranth[-1]+" if True else 0 "
#         elif type == "count":
#             exp_after_paranth = quantifier.split(")")[len(quantifier.split(")")) - 1]
#             condition_vec_exp = "sum([1 if " + exp_in_paranth[-1] + " else 0 "
#         else:
#             condition_vec_exp += "in [1 if " + exp_in_paranth[-1] + " else 0 "
#         for i in range(len(exp_in_paranth) - 1):
#             condition_vec_exp += "for " + exp_in_paranth[i] + " in range(len(" + vecs[i] + ")) "
#         condition_vec_exp += "]"
#         if type in ['foreach',"count"] :
#             condition_vec_exp += ")"
#         if type == "count":
#             condition_vec_exp += exp_after_paranth
#             for equal in re.findall(r'([^<>=]=)[^<>=]', condition_vec_exp, re.M | re.I):
#                 condition_vec_exp = condition_vec_exp.replace(equal,"==")
#         condition_vec = condition_vec_exp[condition_vec_exp.index('['):]
#         return (condition_vec_exp,condition_vec)
#
#     def decode_conditions(conditions,debug=False):
#         # Convert proprietary functions in already excel parsed conditions into pyton syntax
#         for i in range(len(conditions)):
#             conditions[i] = conditions[i].replace('("s")', '(s)')
#             conditions[i] = conditions[i].replace('("r")', '(r)')
#             for quantifier in ['exists', 'foreach','percell','countcells','increasing','decreasing','percellcost','cell']:
#                 # Find all appearances of the quantifiers in the given condition
#                 exists = re.findall(r'\"(' + quantifier + '\(.*?\))\"', conditions[i], re.M | re.I)
#                 if quantifier == 'countcells':
#                     exists = re.findall(r'(countcells\(.*?\)[<>=][<>=]*\d+)', conditions[i], re.M | re.I)
#                 for j in range(len(exists)):
#
#                     exists_with_indices = list(exists)
#                     exists_with_indices_vec=list(exists)
#
#                     # Replace _ with [] for each s_i and r_i
#                     entries = re.findall(r'(._.)', exists[j], re.M | re.I)
#                     for k in range(len(entries)):
#                         exists_with_indices[j] = exists_with_indices[j].replace(entries[k],
#                                                                                 (entries[k].replace("_", "[") + "]"))
#                     # Replace = with ==
#                     if not (">" in exists_with_indices[j]) and not ("<" in exists_with_indices[j]):
#                         exists_with_indices[j] = exists_with_indices[j].replace("=", "==")
#
#                     exists_with_indices[j]= exclude_self_index_from_cond(exists_with_indices[j])
#
#                     if quantifier == 'countcells':
#                         if debug:
#                             logging.debug("decode_conditions: Starting to process countcells")
#                             logging.debug("decode_conditions: exists_with_indices[j] = "+str(exists_with_indices[j]))
#
#                         # for equal in re.findall(r'([^<>=]=)[^<>=]', exists_with_indices[j], re.M | re.I):
#                         #     exists_with_indices[j] = exists_with_indices[j].replace(equal, equal+"=")
#                         if debug:
#                             logging.debug("decode_conditions: Switching = for ==: exists_with_indices[j] = " + str(exists_with_indices[j]))
#
#                         #Non-vectorial home made functions
#                         exists_with_indices[j] = exists_with_indices[j].replace('countcells', 's.count')
#                         if debug:
#                             logging.debug("decode_conditions: Switching countcells for s.count: exists_with_indices[j] = " + str(exists_with_indices[j]))
#                         if len(re.findall(r'(\(\d+\))', exists_with_indices[j], re.M | re.I)) != len(re.findall(r'(count)', exists_with_indices[j], re.M | re.I)):
#                             all_factors = re.findall(r"([^\*|\/|\+|\-\**]+)",exists_with_indices[j])
#                             for factor in all_factors:
#                                 new_factor, exists_with_indices_vec[j] = generate_quantifier_vector(
#                                     factor, "count")
#                                 exists_with_indices[j] = exists_with_indices[j].replace(factor,new_factor)
#                         if debug:
#                             logging.debug("decode_conditions: Switch count with list comprehension: exists_with_indices[j] = " + str(exists_with_indices[j]))
#                         conditions[i] = conditions[i].replace('\"' + exists[j] + '\"', exists_with_indices[j])
#                         if debug:
#                             logging.debug("decode_conditions: Final condition result: conditions[i] = " + str(conditions[i]))
#                     elif quantifier=='cell':
#                         exists_with_indices[j] = exists_with_indices[j].replace('cell', '')
#                         conditions[i] = conditions[i].replace('\"' + exists[j] + '\"', exists_with_indices[j])
#                     elif quantifier=='increasing' or quantifier=='decreasing':
#                         exists_with_indices[j] = exists_with_indices[j].replace(quantifier+'()', 'not_strictly_'+quantifier+'(s)')
#                         conditions[i] = conditions[i].replace('\"' + exists[j] + '\"', exists_with_indices[j])
#                     else:
#                         exists_with_indices[j],exists_with_indices_vec[j] = generate_quantifier_vector(exists_with_indices[j], quantifier)
#                         conditions[i] = conditions[i].replace('\"' + exists[j] + '\"', exists_with_indices[j])
#                         if quantifier=='percell':
#                             full_cond_percell = ' if ' + exists_with_indices[j]
#                             conditions[i] = re.sub(r'(\d+)' + re.escape(full_cond_percell),
#                                          r'\1*' + 'sum('+exists_with_indices_vec[j] +')'+full_cond_percell, conditions[i])
#                         elif quantifier=='percellcost':
#                             full_cond_percell = exists_with_indices[j]
#                             conditions[i] = re.sub(r'' + re.escape(full_cond_percell),
#                                                    r'sum(' + exists_with_indices_vec[j] + ')',
#                                                    conditions[i])
#         return conditions
#
#     def exclude_self_index_from_cond(home_made_func):
#         '''Prevent the case of s[i]>s[1] being checked for s[1]. i.e. s[1]>s[1]'''
#         indices = re.findall(r'\[\w+\]', home_made_func, re.M | re.I)
#         has_digit = False
#         has_alpha = False
#         alpha  = "qazwsxedcrfvtgbyhnujmiklop"
#         digits = "0123456789"
#         for index in indices:
#             if index[1] in alpha:
#                 has_alpha = True
#             if index[1] in digits:
#                 has_digit = True
#         if has_alpha and has_digit:
#             cond = re.findall(r',.*\)', home_made_func, re.M | re.I)
#             cond = cond[0][1:-1]
#             new_cond = "("+cond+" or "+str(indices[0])+"=="+str(indices[1])+")"
#             home_made_func = home_made_func.replace(cond,new_cond)
#         return home_made_func
#
# }
#
# deprecated
# {
#     def parse_conditions(conds,debug=False):
#         conds = parseConditions.encode_conditions(conds)
#         if debug:
#             logging.debug("parse_conditions - after encoding: dimensions_columns_conds = " + str(conds))
#         python_inputs = []
#         for i in conds:
#             e = shunting_yard(i);
#             G, root = build_ast(e)
#             python_inputs += [root.emit(G, context=None)]
#         if debug:
#             return parseConditions.decode_conditions(python_inputs,True)
#         else:
#             return parseConditions.decode_conditions(python_inputs)
# }
def create_dimensions_matrix(dimensions_rows_categories_names, dimensions_columns_categories_names):
    dimensions_matrix = {row_name: dict() for row_name in dimensions_rows_categories_names}
    for row_name in dimensions_matrix:
        for col_name in dimensions_columns_categories_names:
            dimensions_matrix[row_name][col_name] = dict()
    return dimensions_matrix

def classify_strategies_to_dimensions(strategies, dimensions_matrix, dimensions_rows_conds,
                                      dimensions_columns_conds):
    row = ""
    col = ""
    for t in strategies:
        s = tuple(t)
        exec "row =" + dimensions_rows_conds[0]
        exec "col =" + dimensions_columns_conds[0]
        dimensions_matrix[row][col][s] = dict()
    return dimensions_matrix