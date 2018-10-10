from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.shortcuts import render_to_response, render

from src.pycel.excelcompiler import *
import logging, sys, time

import htmlResultFile
import parseConditions
import parseSubmittedData
import generateResultPageHtml
import dimensionsClassifier
import equilibriaCalculator


htmlHeaderTextWithDate = htmlResultFile.HTML_HEADER_TEXT.replace("#date#", time.strftime("%H:%M %d/%m/%y"))
DEBUG=True

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# Used by other files:
# Used bu urls.py
def empty_url(request):
    print "aaaa"
    context = {
        'latest_question_list': 'Hello',
    }
    return render(request,"index.html")

def full_calc(strategies_vector, dimensions_rows_conds, dimensions_columns_conds, dimensions_rows_categories_names,
              dimensions_columns_categories_names, dimensions_ordered_row, dimensions_ordered_col, payment_conds):

    # Parsing conditions
    dimensions_rows_conds = parseConditions.parse_conditions(dimensions_rows_conds)
    dimensions_columns_conds = parseConditions.parse_conditions(dimensions_columns_conds,True)
    logging.debug("full_calc - after parsing: dimensions_columns_conds = " + str(dimensions_columns_conds))
    payment_conds = parseConditions.parse_conditions(payment_conds)

    # Classifying to dimensions
    dimensions_matrix = dimensionsClassifier.create_dimensions_matrix(dimensions_rows_categories_names,
                                                 dimensions_columns_categories_names)
    dimensions_matrix = dimensionsClassifier.classify_strategies_to_dimensions(strategies_vector, dimensions_matrix,
                                                          dimensions_rows_conds,
                                                          dimensions_columns_conds)

    # Calculating equilibria
    dimensions_matrix = equilibriaCalculator.calc_payments(dimensions_matrix, payment_conds)
    dimensions_matrix = equilibriaCalculator.calc_MD_eq(dimensions_matrix, dimensions_ordered_row, dimensions_ordered_col)
    dimensions_matrix = equilibriaCalculator.calc_Global_eq(dimensions_matrix)
    return dimensions_matrix

class NameForm(forms.Form):
    var_name_1 = forms.CharField(max_length=1000, required=False)
    var_name_2 = forms.CharField(max_length=1000, required=False)
    var_name_3 = forms.CharField(max_length=1000, required=False)
    var_name_4 = forms.CharField(max_length=1000, required=False)
    var_name_5 = forms.CharField(max_length=1000, required=False)
    var_name_6 = forms.CharField(max_length=1000, required=False)
    var_name_7 = forms.CharField(max_length=1000, required=False)
    var_name_8 = forms.CharField(max_length=1000, required=False)
    var_name_9 = forms.CharField(max_length=1000, required=False)
    var_name_10 = forms.CharField(max_length=1000, required=False)

    var_val_1 = forms.CharField(max_length=1000, required=False)
    var_val_2 = forms.CharField(max_length=1000, required=False)
    var_val_3 = forms.CharField(max_length=1000, required=False)
    var_val_4 = forms.CharField(max_length=1000, required=False)
    var_val_5 = forms.CharField(max_length=1000, required=False)
    var_val_6 = forms.CharField(max_length=1000, required=False)
    var_val_7 = forms.CharField(max_length=1000, required=False)
    var_val_8 = forms.CharField(max_length=1000, required=False)
    var_val_9 = forms.CharField(max_length=1000, required=False)
    var_val_10 = forms.CharField(max_length=1000, required=False)

    strategies_vector_length = forms.CharField(max_length=1000, required=False)
    strategies_full_set = forms.CharField(max_length=1000, required=False)

    strategies_super_set = forms.CharField(max_length=1000, required=False)
    strategies_lower_bound = forms.CharField(max_length=1000, required=False)
    strategies_constraint_1 = forms.CharField(max_length=1000, required=False)
    strategies_constraint_2 = forms.CharField(max_length=1000, required=False)
    strategies_constraint_3 = forms.CharField(max_length=1000, required=False)
    strategies_constraint_4 = forms.CharField(max_length=1000, required=False)
    strategies_constraint_5 = forms.CharField(max_length=1000, required=False)
    strategies_constraint_6 = forms.CharField(max_length=1000, required=False)
    strategies_constraint_7 = forms.CharField(max_length=1000, required=False)
    strategies_constraint_8 = forms.CharField(max_length=1000, required=False)
    strategies_constraint_9 = forms.CharField(max_length=1000, required=False)
    strategies_constraint_10 = forms.CharField(max_length=1000, required=False)

    payment_if_cond_1 = forms.CharField(max_length=1000, required=False)
    payment_if_true_1 = forms.CharField(max_length=1000, required=False)
    payment_if_false_1 = forms.CharField(max_length=1000, required=False)
    payment_if_cond_2 = forms.CharField(max_length=1000, required=False)
    payment_if_true_2 = forms.CharField(max_length=1000, required=False)
    payment_if_false_2 = forms.CharField(max_length=1000, required=False)
    payment_if_cond_3 = forms.CharField(max_length=1000, required=False)
    payment_if_true_3 = forms.CharField(max_length=1000, required=False)
    payment_if_false_3 = forms.CharField(max_length=1000, required=False)
    payment_if_cond_4 = forms.CharField(max_length=1000, required=False)
    payment_if_true_4 = forms.CharField(max_length=1000, required=False)
    payment_if_false_4 = forms.CharField(max_length=1000, required=False)
    payment_if_cond_5 = forms.CharField(max_length=1000, required=False)
    payment_if_true_5 = forms.CharField(max_length=1000, required=False)
    payment_if_false_5 = forms.CharField(max_length=1000, required=False)
    payment_if_cond_6 = forms.CharField(max_length=1000, required=False)
    payment_if_true_6 = forms.CharField(max_length=1000, required=False)
    payment_if_false_6 = forms.CharField(max_length=1000, required=False)
    payment_if_cond_7 = forms.CharField(max_length=1000, required=False)
    payment_if_true_7 = forms.CharField(max_length=1000, required=False)
    payment_if_false_7 = forms.CharField(max_length=1000, required=False)
    payment_if_cond_8 = forms.CharField(max_length=1000, required=False)
    payment_if_true_8 = forms.CharField(max_length=1000, required=False)
    payment_if_false_8 = forms.CharField(max_length=1000, required=False)
    payment_if_cond_9 = forms.CharField(max_length=1000, required=False)
    payment_if_true_9 = forms.CharField(max_length=1000, required=False)
    payment_if_false_9 = forms.CharField(max_length=1000, required=False)
    payment_if_cond_10 = forms.CharField(max_length=1000, required=False)
    payment_if_true_10 = forms.CharField(max_length=1000, required=False)
    payment_if_false_10 = forms.CharField(max_length=1000, required=False)

    payment_if_res_1 = forms.CharField(max_length=1000, required=False)
    payment_if_res_2 = forms.CharField(max_length=1000, required=False)
    payment_if_res_3 = forms.CharField(max_length=1000, required=False)
    payment_if_res_4 = forms.CharField(max_length=1000, required=False)
    payment_if_res_5 = forms.CharField(max_length=1000, required=False)
    payment_if_res_6 = forms.CharField(max_length=1000, required=False)
    payment_if_res_7 = forms.CharField(max_length=1000, required=False)
    payment_if_res_8 = forms.CharField(max_length=1000, required=False)
    payment_if_res_9 = forms.CharField(max_length=1000, required=False)
    payment_if_res_10 = forms.CharField(max_length=1000, required=False)



    dimensions_row_category_name_1 = forms.CharField(max_length=1000, required=False)
    dimensions_row_category_name_2 = forms.CharField(max_length=1000, required=False)
    dimensions_row_category_name_3 = forms.CharField(max_length=1000, required=False)
    dimensions_row_category_name_4 = forms.CharField(max_length=1000, required=False)
    dimensions_row_category_name_5 = forms.CharField(max_length=1000, required=False)
    dimensions_row_category_name_6 = forms.CharField(max_length=1000, required=False)
    dimensions_row_category_name_7 = forms.CharField(max_length=1000, required=False)
    dimensions_row_category_name_8 = forms.CharField(max_length=1000, required=False)
    dimensions_row_category_name_9 = forms.CharField(max_length=1000, required=False)
    dimensions_row_category_name_10 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_cond_1 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_true_1 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_false_1 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_cond_2 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_true_2 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_false_2 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_cond_3 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_true_3 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_false_3 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_cond_4 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_true_4 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_false_4 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_cond_5 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_true_5 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_false_5 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_cond_6 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_true_6 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_false_6 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_cond_7 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_true_7 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_false_7 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_cond_8 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_true_8 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_false_8 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_cond_9 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_true_9 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_false_9 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_cond_10 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_true_10 = forms.CharField(max_length=1000, required=False)
    dimensions_row_if_false_10 = forms.CharField(max_length=1000, required=False)

    dimensions_column_category_name_1 = forms.CharField(max_length=1000, required=False)
    dimensions_column_category_name_2 = forms.CharField(max_length=1000, required=False)
    dimensions_column_category_name_3 = forms.CharField(max_length=1000, required=False)
    dimensions_column_category_name_4 = forms.CharField(max_length=1000, required=False)
    dimensions_column_category_name_5 = forms.CharField(max_length=1000, required=False)
    dimensions_column_category_name_6 = forms.CharField(max_length=1000, required=False)
    dimensions_column_category_name_7 = forms.CharField(max_length=1000, required=False)
    dimensions_column_category_name_8 = forms.CharField(max_length=1000, required=False)
    dimensions_column_category_name_9 = forms.CharField(max_length=1000, required=False)
    dimensions_column_category_name_10 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_cond_1 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_true_1 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_false_1 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_cond_2 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_true_2 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_false_2 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_cond_3 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_true_3 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_false_3 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_cond_4 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_true_4 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_false_4 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_cond_5 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_true_5 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_false_5 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_cond_6 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_true_6 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_false_6 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_cond_7 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_true_7 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_false_7 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_cond_8 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_true_8 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_false_8 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_cond_9 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_true_9 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_false_9 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_cond_10 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_true_10 = forms.CharField(max_length=1000, required=False)
    dimensions_column_if_false_10 = forms.CharField(max_length=1000, required=False)

    strategies_vector_1 = forms.CharField(max_length=1000, required=False)
    strategies_vector_2 = forms.CharField(max_length=1000, required=False)
    strategies_vector_3 = forms.CharField(max_length=1000, required=False)
    strategies_vector_4 = forms.CharField(max_length=1000, required=False)
    strategies_vector_5 = forms.CharField(max_length=1000, required=False)
    strategies_vector_6 = forms.CharField(max_length=1000, required=False)
    strategies_vector_7 = forms.CharField(max_length=1000, required=False)
    strategies_vector_8 = forms.CharField(max_length=1000, required=False)
    strategies_vector_9 = forms.CharField(max_length=1000, required=False)
    strategies_vector_10 = forms.CharField(max_length=1000, required=False)
    strategies_vector_11 = forms.CharField(max_length=1000, required=False)
    strategies_vector_12 = forms.CharField(max_length=1000, required=False)
    strategies_vector_13 = forms.CharField(max_length=1000, required=False)
    strategies_vector_14 = forms.CharField(max_length=1000, required=False)
    strategies_vector_15 = forms.CharField(max_length=1000, required=False)
    strategies_vector_16 = forms.CharField(max_length=1000, required=False)
    strategies_vector_17 = forms.CharField(max_length=1000, required=False)
    strategies_vector_18 = forms.CharField(max_length=1000, required=False)
    strategies_vector_19 = forms.CharField(max_length=1000, required=False)
    strategies_vector_20 = forms.CharField(max_length=1000, required=False)
    strategies_vector_21 = forms.CharField(max_length=1000, required=False)
    strategies_vector_22 = forms.CharField(max_length=1000, required=False)
    strategies_vector_23 = forms.CharField(max_length=1000, required=False)
    strategies_vector_24 = forms.CharField(max_length=1000, required=False)
    strategies_vector_25 = forms.CharField(max_length=1000, required=False)
    strategies_vector_26 = forms.CharField(max_length=1000, required=False)
    strategies_vector_27 = forms.CharField(max_length=1000, required=False)
    strategies_vector_28 = forms.CharField(max_length=1000, required=False)
    strategies_vector_29 = forms.CharField(max_length=1000, required=False)
    strategies_vector_30 = forms.CharField(max_length=1000, required=False)
    strategies_vector_single = forms.CharField(max_length=1000, required=False)

    strategies_upper_bound = forms.CharField(max_length=1000, required=False)
    strategies_lower_bound = forms.CharField(max_length=1000, required=False)

@csrf_exempt
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # Read the form's content
        form = NameForm(request.POST)
        if form.is_valid():
            try:
                variables_names, variables_definitions, variables_values = \
                    parseSubmittedData.parse_variables_definition(form.cleaned_data)
            except:
                return HttpResponse("Variables were not inserted properly. Please type them once again.")

            try:
                dimensions_rows_conds_dict, dimensions_columns_conds_dict, strategies_constraints, \
                payment_conds_dict, payment_conds, dimensions_rows_conds, dimensions_columns_conds = \
                    parseSubmittedData.parse_conditions(form.cleaned_data, variables_definitions)
            except:
                return HttpResponse("Dimensions data were not inserted properly. Please type them once again.")

            logging.debug("Preprocessing: dimensions_columns_conds = " + str(dimensions_columns_conds))

            try:
                strategies_vectors, dimensions_rows_categories_names, dimensions_columns_categories_names = \
                    parseSubmittedData.parse_generator(form.cleaned_data, variables_definitions, strategies_constraints)
            except:
                return HttpResponse("Generator data were not inserted properly. Please type them once again.")
            # **********************************************************************************************************

            # Run the Calc
            try:
                dimensions_matrix=full_calc(strategies_vectors, dimensions_rows_conds, dimensions_columns_conds,
                                            dimensions_rows_categories_names, dimensions_columns_categories_names,
                                            dimensions_rows_categories_names, dimensions_columns_categories_names, payment_conds)
            except Exception as err:
                return HttpResponse("An error occurred while calculating the equilibrium: {0}. Please contact us.".format(err))

            # Generate the result page
            try:
                result_html_page = \
                    generateResultPageHtml.create_result_html_table(dimensions_matrix, dimensions_rows_categories_names, dimensions_columns_categories_names)
            except:
                return HttpResponse("An error occurred while generating the result page. Please contact us." )

            return HttpResponse(result_html_page)
        else:
            return HttpResponse("Bug")

    # return render(request, 'name.html', {'form': form})
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)



