
def calc_payments(dimensions_matrix, payment_conds):
    for row in dimensions_matrix:
        for col in dimensions_matrix[row]:
            for strategy in dimensions_matrix[row][col]:
                for row2 in dimensions_matrix:
                    dimensions_matrix[row][col][strategy][row2] = dict()
                    for col2 in dimensions_matrix[row2]:
                        dimensions_matrix[row][col][strategy][row2][col2] = dict()
                        for strategy2 in dimensions_matrix[row2][col2]:
                            dimensions_matrix[row][col][strategy][row2][col2][strategy2] = dict()
                            s = strategy
                            r = strategy2
                            payment = [0 for i in range(len(payment_conds))]
                            for k in range(len(payment_conds)):
                                exec "payment["+str(k)+"]=" + payment_conds[k]
                            final_payment = sum(payment)
                            dimensions_matrix[row][col][strategy][row2][col2][strategy2]["val"] = final_payment
    for row in dimensions_matrix:
        for col in dimensions_matrix[row]:
            for strategy in dimensions_matrix[row][col]:
                for row2 in dimensions_matrix[row][col][strategy]:
                    for col2 in dimensions_matrix[row][col][strategy][row2]:
                        cell_size = len(dimensions_matrix[row][col][strategy][row2][col2])
                        pyments_in_cell = [
                            eval(str(dimensions_matrix[row][col][strategy][row2][col2][strategy2]["val"])) for
                            strategy2
                            in dimensions_matrix[row][col][strategy][row2][col2]]
                        uni_payment = sum([(1 / float(cell_size)) * payment for payment in pyments_in_cell])
                        dimensions_matrix[row][col][strategy][row2][col2]["uniform_payment"] = uni_payment
    # dimensions_matrix_copy = dict(dimensions_matrix)
    # for row in dimensions_matrix:
    #     for col in dimensions_matrix[row]:
    #         strategy = dimensions_matrix[row][col].keys()[0]
    #         for row2 in dimensions_matrix[row][col][strategy]:
    #             for col2 in dimensions_matrix[row][col][strategy][row2]:
    #                 if row==row2 and col==col2:
    #                     # a=1
    #                     dimensions_matrix_copy[row][col]["uniform_payment"]= dimensions_matrix[row][col][strategy][row2][col2]["uniform_payment"]
    # dimensions_matrix = dict(dimensions_matrix_copy)
    for row in dimensions_matrix:
        for col in dimensions_matrix[row]:
            best_payment = -1000000
            best_response=tuple()
            for strategy in dimensions_matrix[row][col]:
                dimensions_matrix[row][col][strategy]["is_best_response"] = False
                if dimensions_matrix[row][col][strategy][row][col]["uniform_payment"]>=best_payment:
                    best_response = strategy
                    best_payment = dimensions_matrix[row][col][strategy][row][col]["uniform_payment"]
            for strategy in dimensions_matrix[row][col]:
                if dimensions_matrix[row][col][strategy][row][col]["uniform_payment"]>=best_payment:
                    dimensions_matrix[row][col][strategy]["is_best_response"] = True
            if best_response !=tuple():
                dimensions_matrix[row][col][best_response]["is_best_response"] = True
            dimensions_matrix[row][col]["best_response"] = best_response
    #Add to each cell's best response, the pthers cells' best response to it and its score
    for row in dimensions_matrix:
        for col in dimensions_matrix[row]:
            for row2 in dimensions_matrix:
                for col2 in dimensions_matrix[row2]:
                    best_response = tuple()
                    best_payment = -float("inf")
                    for strategy in dimensions_matrix[row2][col2]:
                        if strategy != "best_response" and dimensions_matrix[row2][col2][strategy][row][col]["uniform_payment"] >= best_payment:
                            best_response = strategy
                            best_payment = dimensions_matrix[row2][col2][strategy][row][col]["uniform_payment"]
                    if (dimensions_matrix[row][col]["best_response"]!=tuple()):
                        dimensions_matrix[row][col][dimensions_matrix[row][col]["best_response"]][row2][col2]["best_response"] = best_response
                        dimensions_matrix[row][col][dimensions_matrix[row][col]["best_response"]][row2][col2][
                        "best_response_payment"] = best_payment
    return dimensions_matrix

def calc_MD_eq(dimensions_matrix, dimensions_ordered_row, dimensions_ordered_col):
    for row in dimensions_matrix:
        for col in dimensions_matrix[row]:
            best_response = dimensions_matrix[row][col]["best_response"]
            is_MD_eq = True
            lost_to = ""
            row_index = dimensions_ordered_row.index(row)
            if not(best_response==tuple()):
                for col2 in dimensions_matrix[row]:
                    for strategy in dimensions_matrix[dimensions_ordered_row[row_index]][col2]:
                        if strategy != "best_response" and col2 != col:
                            a= dimensions_matrix[row][col][best_response][row][col]["uniform_payment"]
                            if dimensions_matrix[row][col][best_response][row][col]["uniform_payment"] < \
                                    dimensions_matrix[dimensions_ordered_row[row_index ]][col2][strategy][row][col]["uniform_payment"]:
                                is_MD_eq = False
                                lost_to = "row="+str(dimensions_ordered_row[row_index])+",column="+str(col2)+",strategy="+str(strategy)
                col_index = dimensions_ordered_col.index(col)
                for row2 in dimensions_matrix:
                    for strategy in dimensions_matrix[row2][dimensions_ordered_col[col_index]]:
                        if strategy != "best_response" and row2 != row:
                            a= dimensions_matrix[row][col][best_response][row][col]["uniform_payment"]
                            if dimensions_matrix[row][col][best_response][row][col]["uniform_payment"] < \
                                    dimensions_matrix[row2][dimensions_ordered_col[col_index]][strategy][row][col][
                                        "uniform_payment"]:
                                is_MD_eq = False
                                lost_to = "row=" + str(row2) + ",column=" + str(
                                    dimensions_ordered_col[col_index]) + ",strategy=" + str(strategy)
                # if row_index != 0:
                #
                #     for strategy in dimensions_matrix[dimensions_ordered_row[row_index - 1]][col]:
                #         if strategy != "best_response":
                #             a= dimensions_matrix[row][col][best_response][row][col]["uniform_payment"]
                #             if dimensions_matrix[row][col][best_response][row][col]["uniform_payment"] < \
                #                     dimensions_matrix[dimensions_ordered_row[row_index - 1]][col][strategy][row][col]["uniform_payment"]:
                #                 is_MD_eq = False
                #                 lost_to = "row="+str(dimensions_ordered_row[row_index - 1])+",column="+str(col)+",strategy="+str(strategy)
                # if row_index != len(dimensions_ordered_row) - 1:
                #     for strategy in dimensions_matrix[dimensions_ordered_row[row_index + 1]][col]:
                #         if strategy != "best_response":
                #             if dimensions_matrix[row][col][best_response][row][col]["uniform_payment"] < \
                #                     dimensions_matrix[dimensions_ordered_row[row_index + 1]][col][strategy][row][col]["uniform_payment"]:
                #                 is_MD_eq = False
                #                 lost_to = "row="+str(dimensions_ordered_row[row_index + 1])+",column="+str(col)+",strategy="+str(strategy)
                # col_index = dimensions_ordered_col.index(col)
                # if col_index != 0:
                #     for strategy in dimensions_matrix[row][dimensions_ordered_col[col_index - 1]]:
                #         if strategy != "best_response":
                #             if dimensions_matrix[row][col][best_response][row][col]["uniform_payment"] < \
                #                     dimensions_matrix[row][dimensions_ordered_col[col_index - 1]][strategy][row][col]["uniform_payment"]:
                #                 is_MD_eq = False
                #                 lost_to = "row="+str(row)+",column="+str(dimensions_ordered_col[col_index - 1])+",strategy="+str(strategy)
                # if col_index != len(dimensions_ordered_col) - 1:
                #     for strategy in dimensions_matrix[row][dimensions_ordered_col[col_index + 1]]:
                #         if strategy != "best_response":
                #             if dimensions_matrix[row][col][best_response][row][col]["uniform_payment"] < \
                #                     dimensions_matrix[row][dimensions_ordered_col[col_index + 1]][strategy][row][col]["uniform_payment"]:
                #                 is_MD_eq = False
                #                 lost_to = "row="+str(row)+",column="+str(dimensions_ordered_col[col_index + 1])+",strategy="+str(strategy)
            else:
                is_MD_eq = False
                lost_to = "no one, empty cell"
            for strategy in dimensions_matrix[row][col]:
                if strategy != "best_response":
                    if is_MD_eq:
                        dimensions_matrix[row][col][strategy]["is_MD_eq"] = True
                        dimensions_matrix[row][col][strategy]["lost_to_MD_eq"] = lost_to
                    else:
                        dimensions_matrix[row][col][strategy]["is_MD_eq"] = False
                        dimensions_matrix[row][col][strategy]["lost_to_MD_eq"] = lost_to

    return dimensions_matrix

def calc_Global_eq(dimensions_matrix):
    for row in dimensions_matrix:
        for col in dimensions_matrix[row]:
            best_response = dimensions_matrix[row][col]["best_response"]
            lost_to = ""
            is_Global_eq = False
            if best_response != tuple():
                if dimensions_matrix[row][col][best_response]["is_MD_eq"]:
                    is_Global_eq = True
                    for row2 in dimensions_matrix:
                        for col2 in dimensions_matrix[row]:
                            for strategy in dimensions_matrix[row2][col2]:
                                if strategy != "best_response":
                                    if dimensions_matrix[row][col][best_response][row][col]["uniform_payment"] < \
                                            dimensions_matrix[row2][col2][strategy][row][col]["uniform_payment"]:
                                        lost_to = "row=" + str(row2) + ",column=" + str(col2)+",strategy="+str(strategy)
                                        is_Global_eq = False
            for strategy in dimensions_matrix[row][col]:
                if strategy != "best_response":
                    if is_Global_eq:
                        dimensions_matrix[row][col][strategy]["is_Global_eq"] = True
                        dimensions_matrix[row][col][strategy]["lost_to_Global_eq"] = lost_to
                    else:
                        dimensions_matrix[row][col][strategy]["is_Global_eq"] = False
                        dimensions_matrix[row][col][strategy]["lost_to_Global_eq"] = lost_to
    return dimensions_matrix
