import re
def encode_conditions(conditions):
    # Replaces proprietary expressions with strings in order to parse excel expressions
    for i in range(len(conditions)):
        conditions[i] = conditions[i].replace("(s)", '("s")')
        conditions[i] = conditions[i].replace("(r)", '("r")')
        exists = re.findall(r'(exists\(.*?\))', conditions[i], re.M | re.I)
        for j in range(len(exists)):
            conditions[i] = conditions[i].replace(exists[j], '\"' + exists[j] + '\"')
        for_each = re.findall(r'(foreach\(.*?\)),', conditions[i], re.M | re.I)
        for j in range(len(for_each)):
            conditions[i] = conditions[i].replace(for_each[j], '\"' + for_each[j] + '\"')
        percell = re.findall(r'(percell\(.*?\)),', conditions[i], re.M | re.I)
        for j in range(len(percell)):
            conditions[i] = conditions[i].replace(percell[j], '\"' + percell[j] + '\"')
        countcells = list(set(re.findall(r'(countcells\(.*?\))', conditions[i], re.M | re.I)))
        for j in range(len(countcells)):
            conditions[i] = conditions[i].replace(countcells[j], '\"' + countcells[j] + '\"')
        increasing = re.findall(r'(increasing\(\))', conditions[i], re.M | re.I)
        for j in range(len(increasing)):
            conditions[i] = conditions[i].replace(increasing[j], '\"' + increasing[j] + '\"')
        decreasing = re.findall(r'(decreasing\(\))', conditions[i], re.M | re.I)
        for j in range(len(decreasing)):
            conditions[i] = conditions[i].replace(decreasing[j], '\"' + decreasing[j] + '\"')
        percellcost = re.findall(r'(percellcost\(.*?\)),', conditions[i], re.M | re.I)
        for j in range(len(percellcost)):
            conditions[i] = conditions[i].replace(percellcost[j], '\"' + percellcost[j] + '\"')
        cell = re.findall(r'(cell\(.*?\)),', conditions[i], re.M | re.I)
        for j in range(len(cell)):
            conditions[i] = conditions[i].replace(cell[j], '\"' + cell[j] + '\"')
        sum = re.findall(r'(SUM\(.*?\))', conditions[i], re.M | re.I)
    return conditions
conditions = ['=IF(countcells(0)+countcells(1)=1,"2",IF(countcells(0)+countcells(1)=2,"1","3"))'] # ['=IF(countcells(i,s_i<=4/2)=countcells(i,s_i>0),"L",IF(countcells(i,s_i>=4/2+1)=countcells(i,s_i>0),"H","mix"))']
print(encode_conditions(conditions))