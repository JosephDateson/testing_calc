import re
def exclude_self_index_from_cond(home_made_func):
    '''
    :param home_made_func: A func of the form foreach(i,si<=s1)
    :return: Prevent the case of s[i]>s[1] being checked for s[1]. i.e. s[1]>s[1]
    '''
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
        cond = re.findall(r',.*\)', home_made_func, re.M | re.I)
        cond = cond[0][1:-1]
        new_cond = "("+cond+" or "+str(indices[0])+"=="+str(indices[1])+")"
        home_made_func = home_made_func.replace(cond,new_cond)
    return home_made_func
def test_exclude_self_index_from_cond():
    foreach = "foreach(i,si<=s1)"
    exclude_self_index_from_cond(foreach)
if __name__ == '__main__':
    test_exclude_self_index_from_cond()