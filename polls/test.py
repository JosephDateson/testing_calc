import logging,re

def exclude_self_index_from_cond(home_made_func):
    '''Prevent the case of s[i]>s[1] being checked for s[1]. i.e. s[1]>s[1]'''
    indices = re.findall(r'\[\w+\]', home_made_func, re.M | re.I)
    has_digit = False
    has_alpha = False
    alpha  = "qazwsxedcrfvtgbyhnujmiklop"
    digits = "0123456789"
    for index in indices:
        if index[1] in alpha:
            has_alpha = True
        if index[1] in digits:
            has_digit = True
    if has_alpha and has_digit:
        # print "in exclude_self_index_from_cond, with="+str(home_made_func)
        cond = re.findall(r',.*\)', home_made_func, re.M | re.I)
        cond = cond[0][1:-1]
        new_cond = "("+cond+" or "+str(indices[0])+"=="+str(indices[1])+")"
        # print "cond="+str(home_made_func.replace(cond,new_cond))
        home_made_func = home_made_func.replace(cond,new_cond)
    return home_made_func

def generate_quantifier_vector(quantifier, type='exists'):
    '''Receive an exist condition and generate a boolean vector based on it's condition
        Type can be either exists or for_each'''
    exp_in_paranth = re.findall(r'' + type + '\((.*?\))\)', quantifier, re.M | re.I)
    if exp_in_paranth == []:
        # print "empty"
        exp_in_paranth = re.findall(r'' + type + '\((.*?)\)', quantifier, re.M | re.I)
    exp_in_paranth = exp_in_paranth[0].split(",")

    vecs = re.findall(r'(.)\[.\]', exp_in_paranth[-1], re.M | re.I)
    condition_vec_exp = "1 " if (type in ['exists','percell'] ) else "not(0 "

    if type=="percellcost":
        condition_vec_exp = "1 " if (type == 'percellcost') else "not(0 "
        condition_vec_exp += "in ["+exp_in_paranth[-1]+" if True else 0 "
    elif type == "count":
        exp_after_paranth = quantifier.split(")")[len(quantifier.split(")"))-1]
        condition_vec_exp = "sum([1 if " + exp_in_paranth[-1] + " else 0 "
    else:
        condition_vec_exp += "in [1 if " + exp_in_paranth[-1] + " else 0 "
    for i in range(len(exp_in_paranth) - 1):
        condition_vec_exp += "for " + exp_in_paranth[i] + " in range(len(" + vecs[i] + ")) "
    condition_vec_exp += "]"
    if type in ['foreach',"count"] :
        condition_vec_exp += ")"
    if type == "count":
        condition_vec_exp += exp_after_paranth
    condition_vec = condition_vec_exp[condition_vec_exp.index('['):]
    return (condition_vec_exp,condition_vec)


def decode_conditions(conditions):
    # Convert proprietary functions in already excel parsed conditions into pyton syntax
    # logging.debug(decode_conditions.__name__ + ":before " + decode_conditions.__name__ + ":" + "conds=" + str(conditions))
    for i in range(len(conditions)):
        conditions[i] = conditions[i].replace('("s")', '(s)')
        conditions[i] = conditions[i].replace('("r")', '(r)')
        for quantifier in ['exists', 'foreach','percell','countcells','increasing','decreasing','percellcost','cell']:
            exists = re.findall(r'\"(' + quantifier + '\(.*?\))\"', conditions[i], re.M | re.I)
            if quantifier == 'countcells':
                exists = re.findall(r'(countcells\(.*?\)=\d+)', conditions[i], re.M | re.I)
            for j in range(len(exists)):
                exists_with_indices = list(exists)
                exists_with_indices_vec=list(exists)
                entries = re.findall(r'(._.)', exists[j], re.M | re.I)
                for k in range(len(entries)):
                    exists_with_indices[j] = exists_with_indices[j].replace(entries[k],
                                                                            (entries[k].replace("_", "[") + "]"))

                if not (">" in exists_with_indices[j]) and not ("<" in exists_with_indices[j]):
                    exists_with_indices[j] = exists_with_indices[j].replace("=", "==")
                exists_with_indices[j]= exclude_self_index_from_cond(exists_with_indices[j])
                if quantifier == 'countcells':
                    #Non-vectorial home made functions
                    exists_with_indices[j] = exists_with_indices[j].replace('countcells', 's.count')
                    if len(re.findall(r'(\(\d+\))', exists[j], re.M | re.I)) == 0:
                        for equal in re.findall(r'([^<>=]=)[^<>=]',exists_with_indices[j],re.M | re.I):
                            exists_with_indices[j] = exists_with_indices[j].replace(equal,equal+"=")
                        exists_with_indices[j], exists_with_indices_vec[j] = generate_quantifier_vector(exists_with_indices[j], "count")

                    conditions[i] = conditions[i].replace('\"' + exists[j] + '\"', exists_with_indices[j])
                elif quantifier=='cell':
                    exists_with_indices[j] = exists_with_indices[j].replace('cell', '')
                    conditions[i] = conditions[i].replace('\"' + exists[j] + '\"', exists_with_indices[j])
                elif quantifier=='increasing' or quantifier=='decreasing':
                    exists_with_indices[j] = exists_with_indices[j].replace(quantifier+'()', 'not_strictly_'+quantifier+'(s)')
                    conditions[i] = conditions[i].replace('\"' + exists[j] + '\"', exists_with_indices[j])
                else:
                    exists_with_indices[j],exists_with_indices_vec[j] = generate_quantifier_vector(exists_with_indices[j], quantifier)
                    conditions[i] = conditions[i].replace('\"' + exists[j] + '\"', exists_with_indices[j])
                    if quantifier=='percell':
                        # print "percell"
                        # print "before conditions[i]="+str( conditions[i])
                        full_cond_percell = ' if ' + exists_with_indices[j]
                        conditions[i] = re.sub(r'(\d+)' + re.escape(full_cond_percell),
                                     r'\1*' + 'sum('+exists_with_indices_vec[j] +')'+full_cond_percell, conditions[i])
                    elif quantifier=='percellcost':
                        # print "percellcost"
                        # print "before conditions[i]=" + str(conditions[i])
                        # print "before exists_with_indices[j]="+str(exists_with_indices[j])
                        full_cond_percell = exists_with_indices[j]
                        conditions[i] = re.sub(r'' + re.escape(full_cond_percell),
                                               r'sum(' + exists_with_indices_vec[j] + ')',
                                               conditions[i])

                # print "after conditions[i]="+str( conditions[i])
    # logging.debug(decode_conditions.__name__ + ":after  " + decode_conditions.__name__ + ":" + "conds=" + str(conditions))
    return conditions

# foreach = ['("S" if "foreach(i,s_i>=r_i)" else ("L" if "foreach(i,s_i<=s_1)" else "M"))']
countcells = ['("1" if "countcells(i,s_i>r_i)=2" else ("2" if "countcells(0)=1" else "3"))']
print(decode_conditions(countcells))
# quant = 's.count(i,s[i]>r[i])=2'
# quant = 'foreach(i,(s[i]>=s[1] or [i]==[1]))'
# print(generate_quantifier_vector(quant,'count'))
old_str = "countcells(i,si>=T/2+1)=countcells(i,si>0)"
def replace_variables_definitions_in_condition(old_str,variables_definitions):
    new_str = old_str
    for variables_definition in variables_definitions:
        new_str = re.sub(r"\b" + variables_definition + r"\b", variables_definitions[variables_definition], new_str)

def replace_variables_definitions(value_with_variable, variables_definitions):
    for variables_definition in variables_definitions:
        value_with_variable = value_with_variable.replace(variables_definition,
                                                          variables_definitions[variables_definition])
    return value_with_variable