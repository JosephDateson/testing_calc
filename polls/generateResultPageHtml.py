import pandas as pd
import htmlResultFile
import time
htmlHeaderTextWithDate = htmlResultFile.HTML_HEADER_TEXT.replace("#date#", time.strftime("%H:%M %d/%m/%y"))
TABLES = []
def create_cell(strategy, row, col, dimensions_matrix):
    strategy_cont = strategy
    if len(strategy) == 1:
        strategy_cont = strategy[0]
    strategy_str =  str(strategy_cont)
    if dimensions_matrix[row][col][strategy]["is_best_response"]:
        strategy_str = strategy_str + "*"
    return strategy_str + ", "


def create_result_html_table(dimensions_matrix, dimensions_rows_categories_names, dimensions_columns_categories_names):
    def create_strategy_table(strategy):
        table_content = '<table id="scores" class="table table-bordered fixed"><thead><tr><th class="col-xs-3 ">Cells\' best strategy\'s score <br> against<i><b id="chosen_cell">chosen cell</b></i></th>'
        for col3 in dimensions_columns_categories_names:
            table_content += "<th>" + col3 + "</th>"
        table_content += "</tr></thead>"
        for row3 in dimensions_rows_categories_names:
            table_content += "<tr><th>" + row3 + "</th>"
            for col3 in dimensions_columns_categories_names:
                if dimensions_matrix[row3][col3]['best_response'] != ():
                    best_response_name = dimensions_matrix[row][col][strategy][row3][col3]['best_response']
                    if (best_response_name == tuple()):
                        best_response_printable_name = ""
                    else:
                        best_response_printable_name = best_response_name if len(best_response_name) > 1 else \
                        best_response_name[0]
                    strategies = str(round(dimensions_matrix[row][col][strategy][row3][col3]['best_response_payment'],2))
                else:
                    strategies = ""
                    best_response_name=""
                    best_response_printable_name=""
                table_content += "<td class='formatted_square_hide'>Best Response:" + str(best_response_printable_name) + "<br> Score=" + str(strategies) + "</td>"
            table_content += "</tr>"
        return table_content
    html_string = '<table class="table table-bordered fixed"><thead><tr><th class="col-xs-3">Partitions of <br>strategies into cells<br><a id="show_hide_strategies" class="on_green" onclick="return myFunction(1);">(click to show all strategies)</a> </th>'
    for col in dimensions_columns_categories_names:
        html_string += "<th>"+col+"</th>"
    html_string += "</tr></thead>"
    global TABLES
    for i in range(len(dimensions_rows_categories_names)):
        row = dimensions_rows_categories_names[i]
        html_string += "<tr><th>"+row+"</th>"
        for j in range(len(dimensions_columns_categories_names)):
            col = dimensions_columns_categories_names[j]
            strategies = ""
            is_MD_eq = False
            is_Global_eq = False
            strategy_for_link = 0
            if (dimensions_matrix[row][col]['best_response'] != ()):
                strategies+=create_cell(dimensions_matrix[row][col]['best_response'], row, col, dimensions_matrix)
                strategy_for_link = dimensions_matrix[row][col]['best_response']
                TABLES+=[(dimensions_matrix[row][col]['best_response'] if len(dimensions_matrix[row][col]['best_response']) > 1 else dimensions_matrix[row][col]['best_response'][0], create_strategy_table(dimensions_matrix[row][col]['best_response']))]
            for strategy in dimensions_matrix[row][col]:
                if strategy != "best_response"  and strategy!=dimensions_matrix[row][col]['best_response']:
                    strategy_for_link = strategy
                    strategies+=create_cell(strategy, row, col, dimensions_matrix)
                    # TABLES += [(strategy if len(strategy) > 1 else strategy[0], create_strategy_table(strategy))]
                    # TABLES+= [(strategy,create_strategy_table())]
                    if dimensions_matrix[row][col][strategy]["is_MD_eq"]:
					    is_MD_eq = True
                    if dimensions_matrix[row][col][strategy]["is_Global_eq"]:
					    is_Global_eq = True
            strategies=strategies[::-1].replace(",","",1)[::-1]
            if is_MD_eq:
                strategies = '<font color="red">'+strategies+'</font>'
            if is_Global_eq:
                strategies = '<font color="red"><u>'+strategies+'</u></font>'
            html_string +="<td class='formatted_square_hide'>" + ' <a onclick="cell_name=document.getElementById(\'chosen_cell\');cell_name.innerHTML=\'('+row+','+col+')\';all_extra_data' + str(i) + str(j) + "_" + str(
            in_house_hash(str(strategy_for_link))) + '()" >' +  strategies   + '</a>'+ "</td>"
        html_string += "</tr>"
    html_string += "</table>"
    #Adding info for each strategy
    top_table = html_string
    html_string += '<table class="table table-bordered fixed" id="scores"><thead><tr><th class="col-xs-3">Cells\' best strategy\'s score <br>against <font color="blue"><b id="chosen_cell">chosen cell</b></font></th>'
    for col in dimensions_columns_categories_names:
        html_string += "<th>"+col+"</th>"
    html_string += "</tr></thead>"
    for row in dimensions_rows_categories_names:
        html_string += "<tr><th>"+row+"</th>"
        # table_content += "<tr><th>"+row+"</th>"
        for col in dimensions_columns_categories_names:
            strategies = ""
            html_string += "<td class='formatted_square_hide'>" + strategies + "</td>"
        html_string += "</tr>"
    for i in range(len(dimensions_rows_categories_names)):
        row = dimensions_rows_categories_names[i]
        for j in range(len(dimensions_columns_categories_names)):
            col = dimensions_columns_categories_names[j]
            # for strategy in dimensions_matrix[row][col]:
            for strategy in dimensions_matrix[row][col]:
                if strategy != "best_response":
                    html_string += generate_script_for_strategy(dimensions_matrix,row,col,strategy,dimensions_rows_categories_names,dimensions_columns_categories_names,i,j)

    def create_csv():
        with open(r'tmp.csv', 'w') as f:
            f.write("This is an exact copy of the top table in the result window\n")
            for df in (pd.read_html(top_table)):
                df.to_csv(f, index=False,header=False)
        with open(r'tmp.csv', 'a') as f:
            f.write("\nThese are exact copies of all the possible bottom tables in the result window. Each table has a strategy name above it and the rest is as if this strategy was chosen in the result window.\n")
            for (strategy,table) in TABLES:
                for df in (pd.read_html(table)):
                    f.write("\n\n\"" + str(strategy) + "\"\n")
                    df.to_csv(f, index=False,header=False)
        with open(r'tmp.csv', 'r') as f:
            csv_content = f.read().replace('\n','\\n').replace('"','\\"').replace("'","\\\\\\\'")
        return csv_content
    html_string= htmlHeaderTextWithDate + html_string;
    html_string += htmlResultFile.HTML_END_TEXT.replace("<csv_content_placeholder>",create_csv())

        # html_string+= str(pd.read_html(html_string))

    return html_string
def generate_script_for_strategy(dimensions_matrix,row,col,strategy,dimensions_rows_categories_names,dimensions_columns_categories_names,row_index,col_index):
    #Generate a table for each strategy containing lost_to's and payments
    html_string = '<script>function all_extra_data' + str(row_index) + str(col_index) +"_"+str(in_house_hash(str(strategy)))+ '() {'

    for i in range(len(dimensions_rows_categories_names)):
        row2 = dimensions_rows_categories_names[i]
        for j in range(len(dimensions_columns_categories_names)):
            col2 = dimensions_columns_categories_names[j]
            html_string+='var x'+str(row_index)+str(col_index)+str(i)+str(j)+' = document.getElementById("scores").rows['+str(i+1)+'].cells;'
            if (dimensions_matrix[row2][col2]['best_response'] != ()):
                best_response_name = dimensions_matrix[row][col][dimensions_matrix[row][col]['best_response']][row2][col2]['best_response']
                if (best_response_name==tuple()):
                    best_response_printable_name=""
                else:
                    best_response_printable_name = best_response_name if len(best_response_name) > 1 else best_response_name[0]
                cell_content = 'Best Response: '+str(best_response_printable_name)+'<br>Score: '+str(round(dimensions_matrix[row][col][dimensions_matrix[row][col]['best_response']][row2][col2]['best_response_payment'],2))
                if row==row2 and col==col2:
                    cell_content = "<font color='blue'>"+cell_content+"</font>"
                html_string+='x'+str(row_index)+str(col_index)+str(i)+str(j)+'['+str(j+1)+'].innerHTML = "'+cell_content+'";'
    html_string += '}</script>'
    return html_string
def in_house_hash(string):
    binary_rep = ''.join(format(ord(x), 'b') for x in string)
    return str(int(binary_rep,2))
