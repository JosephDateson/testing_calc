
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