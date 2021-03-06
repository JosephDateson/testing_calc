from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django import forms
import re
import itertools
import src.pycel
from src.pycel.excelcompiler import *
# from pycel.excelwrapper import ExcelOpxWrapper as ExcelWrapperImpl
# import pycel.excellib
# from pycel.excellib import *
# from pycel.excelutil import *
# from math import *
# from networkx.classes.digraph import DiGraph
# from networkx.drawing.nx_pydot import write_dot
# from networkx.drawing.nx_pylab import draw, draw_circular
# from networkx.readwrite.gexf import write_gexf
# from pycel.tokenizer import ExcelParser, f_token, shunting_yard
# import cPickle
import logging, sys, time
import pandas as pd
import html5lib
# import networkx as nx



DEBUG=True
TABLES = []
HTML_HEADER_TEXT="<!DOCTYPE html>  <html lang='en' class='no-js'> <head><script></script> <style>td.formatted_square_hide{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}td.formatted_square_show{white-space:normal;overflow:hidden;text-overflow:ellipsis;}a.on_green{color:blue;text-decoration:underline;}a.on_green:hover {	color: #7c8d87;text-decoration: underline;}table.fixed { table-layout:fixed; word-break:break-all;}	</style> <meta charset='UTF-8' /> <meta http-equiv='X-UA-Compatible' content='IE=edge,chrome=1'> <meta name='viewport' content='width=device-width, initial-scale=1.0'> <title>Multi-Dimensional Equilibrium Calculator - Result</title> <meta name='description' content='Sticky Table Headers Revisited: Creating functional and flexible sticky table headers' /> <meta name='keywords' content='Sticky Table Headers Revisited' /> <meta name='author' content='Codrops' /> <link rel='shortcut icon' href='../favicon.ico'> <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'> <style> article,aside,details,figcaption,figure,footer,header,hgroup,main,nav,section,summary{display:block;}audio,canvas,video{display:inline-block;}audio:not([controls]){display:none;height:0;}[hidden]{display:none;}html{font-family:sans-serif;-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%;}body{margin:0;}a:focus{outline:thin dotted;}a:active,a:hover{outline:0;}h1{font-size:2em;margin:0.67em 0;}abbr[title]{border-bottom:1px dotted;}b,strong{font-weight:bold;}dfn{font-style:italic;}hr{-moz-box-sizing:content-box;box-sizing:content-box;height:0;}mark{background:#ff0;color:#000;}code,kbd,pre,samp{font-family:monospace,serif;font-size:1em;}pre{white-space:pre-wrap;}q{quotes:'\201C' '\201D' '\2018' '\2019';}small{font-size:80%;}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline;}sup{top:-0.5em;}sub{bottom:-0.25em;}img{border:0;}svg:not(:root){overflow:hidden;}figure{margin:0;}fieldset{border:1px solid #c0c0c0;margin:0 2px;padding:0.35em 0.625em 0.75em;}legend{border:0;padding:0;}button,input,select,textarea{font-family:inherit;font-size:100%;margin:0;}button,input{line-height:normal;}button,select{text-transform:none;}button,html input[type='button'],input[type='reset'],input[type='submit']{-webkit-appearance:button;cursor:pointer;}button[disabled],html input[disabled]{cursor:default;}input[type='checkbox'],input[type='radio']{box-sizing:border-box;padding:0;}input[type='search']{-webkit-appearance:textfield;-moz-box-sizing:content-box;-webkit-box-sizing:content-box;box-sizing:content-box;}input[type='search']::-webkit-search-cancel-button,input[type='search']::-webkit-search-decoration{-webkit-appearance:none;}button::-moz-focus-inner,input::-moz-focus-inner{border:0;padding:0;}textarea{overflow:auto;vertical-align:top;}table{border-collapse:collapse;border-spacing:0;} </style> <style> @import url(http://fonts.googleapis.com/css?family=Lato:300,400,700); @font-face { font-family: 'codropsicons'; src:url('../fonts/codropsicons/codropsicons.eot'); src:url('../fonts/codropsicons/codropsicons.eot?#iefix') format('embedded-opentype'), url('../fonts/codropsicons/codropsicons.woff') format('woff'), url('../fonts/codropsicons/codropsicons.ttf') format('truetype'), url('../fonts/codropsicons/codropsicons.svg#codropsicons') format('svg'); font-weight: normal; font-style: normal; } *, *:after, *:before { -webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box; } body { font-family: 'Lato', Arial, sans-serif; color: #7c8d87; background: #f8f8f8; } a { color: #31bc86; text-decoration: none; } a:hover, a:focus { color: #7c8d87; } .container > header { margin: 0 auto; padding: 2em; text-align: center; background: rgba(0,0,0,0.01); } .container > header h1 { font-size: 2.625em; line-height: 1.3; margin: 0; font-weight: 300; } .container > header span { display: block; font-size: 60%; opacity: 0.7; padding: 0 0 0.6em 0.1em; } /* To Navigation Style */ .codrops-top { background: #fff; background: rgba(255, 255, 255, 0.6); text-transform: uppercase; width: 100%; font-size: 0.69em; line-height: 2.2; } .codrops-top a { text-decoration: none; padding: 0 1em; letter-spacing: 0.1em; display: inline-block; } .codrops-top a:hover { background: rgba(255,255,255,0.95); } .codrops-top span.right { float: right; } .codrops-top span.right a { float: left; display: block; } .codrops-icon:before { font-family: 'codropsicons'; margin: 0 4px; speak: none; font-style: normal; font-weight: normal; font-variant: normal; text-transform: none; line-height: 1; -webkit-font-smoothing: antialiased; } .codrops-icon-drop:before { content: '\e001'; } .codrops-icon-prev:before { content: '\e004'; } /* Demo Buttons Style */ .codrops-demos { padding-top: 1em; font-size: 0.8em; } .codrops-demos a { display: inline-block; margin: 0.5em; padding: 0.7em 1.1em; outline: none; border: 2px solid #31bc86; text-decoration: none; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; } .codrops-demos a:hover, .codrops-demos a.current-demo, .codrops-demos a.current-demo:hover { border-color: #7c8d87; color: #7c8d87; } .related { text-align: center; font-size: 1.5em; padding-bottom: 3em; } @media screen and (max-width: 25em) { .codrops-icon span { display: none; } } </style> <style> /* Component styles */ @font-face { font-family: 'Blokk'; src: url('../fonts/blokk/BLOKKRegular.eot'); src: url('../fonts/blokk/BLOKKRegular.eot?#iefix') format('embedded-opentype'), url('../fonts/blokk/BLOKKRegular.woff') format('woff'), url('../fonts/blokk/BLOKKRegular.svg#BLOKKRegular') format('svg'); font-weight: normal; font-style: normal; } .component { line-height: 1.5em; margin: 0 auto; padding: 2em 0 3em; width: 90%; max-width: 1000px; overflow: hidden; } .component .filler { font-family: 'Blokk', Arial, sans-serif; color: #d3d3d3; } table { border-collapse: collapse; margin-bottom: 3em; width: 100%; background: #fff; } td, th { padding: 0.75em 1.5em; text-align: left; } td.err { background-color: #e992b9; color: #fff; font-size: 0.75em; text-align: center; line-height: 1; } th { background-color: #31bc86; font-weight: bold; color: #fff; white-space: nowrap; } tbody th { background-color: #2ea879; } tbody tr:nth-child(2n-1) { background-color: #f5f5f5; transition: all .125s ease-in-out; } tbody tr:hover { background-color: rgba(129,208,177,.3); } /* For appearance */ .sticky-wrap { overflow-x: auto; overflow-y: hidden; position: relative; margin: 3em 0; width: 100%; } .sticky-wrap .sticky-thead, .sticky-wrap .sticky-col, .sticky-wrap .sticky-intersect { opacity: 0; position: absolute; top: 0; left: 0; transition: all .125s ease-in-out; z-index: 50; width: auto; /* Prevent table from stretching to full size */ } .sticky-wrap .sticky-thead { box-shadow: 0 0.25em 0.1em -0.1em rgba(0,0,0,.125); z-index: 100; width: 100%; /* Force stretch */ } .sticky-wrap .sticky-intersect { opacity: 1; z-index: 150; } .sticky-wrap .sticky-intersect th { background-color: #666; color: #eee; } .sticky-wrap td, .sticky-wrap th { box-sizing: border-box; } /* Not needed for sticky header/column functionality */ td.user-name { text-transform: capitalize; } .sticky-wrap.overflow-y { overflow-y: auto; max-height: 50vh; } </style> <!--[if IE]> <script src='http://html5shiv.googlecode.com/svn/trunk/html5.js'></script> <![endif]--> </head> <body> <div class='container'> <!-- Top Navigation --> <header> <h1>Multi-Dimensional Equilibrium Calculator - <em>Result</em> <span>#date#</span></h1> <nav class='codrops-demos'> <a onclick='save();' href='#'>Downalod current page</a> <a class='current-demo' href='#' onclick='download_csv(\"result.csv\",\"a\")'>Download Excel version</a> </nav> </header> <div class='component'> <div class='panel panel-default'> <div class='panel-heading'> <a data-toggle='collapse' href='#collapse1'> <h4>How to read the tables?</h4> </a> </div> <div class='panel-collapse collapse in' id='collapse1'> <div class='panel-body'> <b>The top table</b> presents the multi-dimensional partition into cells of all strategies. <br><b>The second table</b> presents the score of each cell's best response against a uniform distribution on the chosen cell from the first table.<br><b> A cell's result will appear in the second table by clicking on it.</b> <br><br> <b><u>Conventions &amp; Notations</u> </b><br><br><table><tbody><tr><td>(1,2)*</td><td> A star superscript on a strategy denotes a best response againt the cell itself. </td></tr><tr><td><font color='red'>(1,2)</font></td><td> A cell colored red denotes a multi-dimensional equilibrium.</td></tr> <tr><td><font color='red'><u>(1,2)</u></font></td><td> A cell colored red and underlined denotes a gloabl equilibrium.</td></tr><tr><td><font color='blue'>Best Response: 4<br>    Score: 1.5</font></td><td> <b>In the second table, </b>a cell colored blue denotes the chosen cell. <br>'Best response' is the cell's best response against the chosen cell, and 'Score' is its score against the chosen cell. </td></tr></tbody> </table> </div> </div> </div>"
HTML_END_TEXT="</div> </div><!-- /container --><script>function myFunction(show) {if (show ==1){var cur_class_name='formatted_square_hide';var new_class_name='formatted_square_show';document.getElementById('show_hide_strategies').setAttribute('onclick','return myFunction(0);');document.getElementById('show_hide_strategies').innerHTML='(click to hide all strategies)';}else{var cur_class_name='formatted_square_show';var new_class_name='formatted_square_hide';document.getElementById('show_hide_strategies').setAttribute('onclick','return myFunction(1);');document.getElementById('show_hide_strategies').innerHTML='(click to show all strategies)';}while (document.getElementsByClassName(cur_class_name).length){document.getElementsByClassName(cur_class_name)[0].className = new_class_name;}}</script> <script src='http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js'></script> <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery-throttle-debounce/1.1/jquery.ba-throttle-debounce.min.js'></script> <script> $(function(){ $('table').each(function() { if($(this).find('thead').length > 0 && $(this).find('th').length > 0) { // Clone <thead> var $w = $(window), $t = $(this), $thead = $t.find('thead').clone(), $col = $t.find('thead, tbody').clone(); // Add class, remove margins, reset width and wrap table $t .addClass('sticky-enabled') .css({ margin: 0, width: '100%' }).wrap('<div class='sticky-wrap' />'); if($t.hasClass('overflow-y')) $t.removeClass('overflow-y').parent().addClass('overflow-y'); // Create new sticky table head (basic) $t.after('<table class='sticky-thead' />'); // If <tbody> contains <th>, then we create sticky column and intersect (advanced) if($t.find('tbody th').length > 0) { $t.after('<table class='sticky-col' /><table class='sticky-intersect' />'); } // Create shorthand for things var $stickyHead = $(this).siblings('.sticky-thead'), $stickyCol = $(this).siblings('.sticky-col'), $stickyInsct = $(this).siblings('.sticky-intersect'), $stickyWrap = $(this).parent('.sticky-wrap'); $stickyHead.append($thead); $stickyCol .append($col) .find('thead th:gt(0)').remove() .end() .find('tbody td').remove(); $stickyInsct.html('<thead><tr><th>'+$t.find('thead th:first-child').html()+'</th></tr></thead>'); // Set widths var setWidths = function () { $t .find('thead th').each(function (i) { $stickyHead.find('th').eq(i).width($(this).width()); }) .end() .find('tr').each(function (i) { $stickyCol.find('tr').eq(i).height($(this).height()); }); // Set width of sticky table head $stickyHead.width($t.width()); // Set width of sticky table col $stickyCol.find('th').add($stickyInsct.find('th')).width($t.find('thead th').width()) }, repositionStickyHead = function () { // Return value of calculated allowance var allowance = calcAllowance(); // Check if wrapper parent is overflowing along the y-axis if($t.height() > $stickyWrap.height()) { // If it is overflowing (advanced layout) // Position sticky header based on wrapper scrollTop() if($stickyWrap.scrollTop() > 0) { // When top of wrapping parent is out of view $stickyHead.add($stickyInsct).css({ opacity: 1, top: $stickyWrap.scrollTop() }); } else { // When top of wrapping parent is in view $stickyHead.add($stickyInsct).css({ opacity: 0, top: 0 }); } } else { // If it is not overflowing (basic layout) // Position sticky header based on viewport scrollTop if($w.scrollTop() > $t.offset().top && $w.scrollTop() < $t.offset().top + $t.outerHeight() - allowance) { // When top of viewport is in the table itself $stickyHead.add($stickyInsct).css({ opacity: 1, top: $w.scrollTop() - $t.offset().top }); } else { // When top of viewport is above or below table $stickyHead.add($stickyInsct).css({ opacity: 0, top: 0 }); } } }, repositionStickyCol = function () { if($stickyWrap.scrollLeft() > 0) { // When left of wrapping parent is out of view $stickyCol.add($stickyInsct).css({ opacity: 1, left: $stickyWrap.scrollLeft() }); } else { // When left of wrapping parent is in view $stickyCol .css({ opacity: 0 }) .add($stickyInsct).css({ left: 0 }); } }, calcAllowance = function () { var a = 0; // Calculate allowance $t.find('tbody tr:lt(3)').each(function () { a += $(this).height(); }); // Set fail safe limit (last three row might be too tall) // Set arbitrary limit at 0.25 of viewport height, or you can use an arbitrary pixel value if(a > $w.height()*0.25) { a = $w.height()*0.25; } // Add the height of sticky header a += $stickyHead.height(); return a; }; setWidths(); $t.parent('.sticky-wrap').scroll($.throttle(250, function() { repositionStickyHead(); repositionStickyCol(); })); $w .load(setWidths) .resize($.debounce(250, function () { setWidths(); repositionStickyHead(); repositionStickyCol(); })) .scroll($.throttle(250, repositionStickyHead)); } }); });</script><script> function download_csv(filename, text) {text='<csv_content_placeholder>';var element = document.createElement('a');element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));element.setAttribute('download', filename);  element.style.display = 'none';  document.body.appendChild(element);  element.click();  document.body.removeChild(element);}</script><script>function save() {var html = document.documentElement.outerHTML;	var save_name = 'result';var temp_save_element = document.createElement('a');	temp_save_element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(html));	temp_save_element.setAttribute('download', save_name+'.html');	temp_save_element.style.display = 'none';	document.body.appendChild(temp_save_element);	temp_save_element.click();	document.body.removeChild(temp_save_element);}</script> </body> </html>"

HTML_HEADER_TEXT = HTML_HEADER_TEXT.replace("#date#",time.strftime("%H:%M %d/%m/%y"))

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.template import loader
def empty_url(request):
    print "aaaa"
    context = {
        'latest_question_list': 'Hello',
    }
    return render(request,"index.html")
def not_strictly_increasing(L):
    return (all(x <= y for x, y in zip(L, L[1:])) and any(x < y for x, y in zip(L, L[1:])))

def not_strictly_decreasing(L):
    return (all(x >= y for x, y in zip(L, L[1:])) and any(x > y for x, y in zip(L, L[1:])))


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

def generate_quantifier_vector(quantifier, type='exists'):
    '''Receive an exist condition and generate a boolean vector based on it's condition
        Type can be either exists or for_each'''
    exp_in_paranth = re.findall(r'' + type + '\((.*?\))\)', quantifier, re.M | re.I)
    digits = re.findall(r'\((\d+)\)', quantifier, re.M | re.I)
    if exp_in_paranth == []:
        exp_in_paranth = re.findall(r'' + type + '\((.*?)\)', quantifier, re.M | re.I)
    if len(exp_in_paranth) == 0:
        return quantifier,quantifier
    exp_in_paranth = exp_in_paranth[0].split(",")
    for digit in digits:
        if digit in exp_in_paranth:
            exp_in_paranth.remove(digit)
    if len(exp_in_paranth) == 0:
        return quantifier,quantifier
    vecs = re.findall(r'(.)\[.\]', exp_in_paranth[-1], re.M | re.I)
    condition_vec_exp = "1 " if (type in ['exists','percell'] ) else "not(0 "
    if type=="percellcost":
        condition_vec_exp = "1 " if (type == 'percellcost') else "not(0 "
        condition_vec_exp += "in ["+exp_in_paranth[-1]+" if True else 0 "
    elif type == "count":
        exp_after_paranth = quantifier.split(")")[len(quantifier.split(")")) - 1]
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
        for equal in re.findall(r'([^<>=]=)[^<>=]', condition_vec_exp, re.M | re.I):
            condition_vec_exp = condition_vec_exp.replace(equal,"==")
    condition_vec = condition_vec_exp[condition_vec_exp.index('['):]
    return (condition_vec_exp,condition_vec)

def decode_conditions(conditions,debug=False):
    # Convert proprietary functions in already excel parsed conditions into pyton syntax
    for i in range(len(conditions)):
        conditions[i] = conditions[i].replace('("s")', '(s)')
        conditions[i] = conditions[i].replace('("r")', '(r)')
        for quantifier in ['exists', 'foreach','percell','countcells','increasing','decreasing','percellcost','cell']:
            # Find all appearances of the quantifiers in the given condition
            exists = re.findall(r'\"(' + quantifier + '\(.*?\))\"', conditions[i], re.M | re.I)
            if quantifier == 'countcells':
                exists = re.findall(r'(countcells\(.*?\)[<>=][<>=]*\d+)', conditions[i], re.M | re.I)
            for j in range(len(exists)):

                exists_with_indices = list(exists)
                exists_with_indices_vec=list(exists)

                # Replace _ with [] for each s_i and r_i
                entries = re.findall(r'(._.)', exists[j], re.M | re.I)
                for k in range(len(entries)):
                    exists_with_indices[j] = exists_with_indices[j].replace(entries[k],
                                                                            (entries[k].replace("_", "[") + "]"))
                # Replace = with ==
                if not (">" in exists_with_indices[j]) and not ("<" in exists_with_indices[j]):
                    exists_with_indices[j] = exists_with_indices[j].replace("=", "==")

                exists_with_indices[j]= exclude_self_index_from_cond(exists_with_indices[j])

                if quantifier == 'countcells':
                    if debug:
                        logging.debug("decode_conditions: Starting to process countcells")
                        logging.debug("decode_conditions: exists_with_indices[j] = "+str(exists_with_indices[j]))

                    after
                    parsing
                    if debug:
                        logging.debug("decode_conditions: Switching = for ==: exists_with_indices[j] = " + str(exists_with_indices[j]))

                    #Non-vectorial home made functions
                    exists_with_indices[j] = exists_with_indices[j].replace('countcells', 's.count')
                    if debug:
                        logging.debug("decode_conditions: Switching countcells for s.count: exists_with_indices[j] = " + str(exists_with_indices[j]))
                    if len(re.findall(r'(\(\d+\))', exists_with_indices[j], re.M | re.I)) != len(re.findall(r'(count)', exists_with_indices[j], re.M | re.I)):
                        all_factors = re.findall(r"([^\*|\/|\+|\-\**]+)",exists_with_indices[j])
                        for factor in all_factors:
                            new_factor, exists_with_indices_vec[j] = generate_quantifier_vector(
                                factor, "count")
                            exists_with_indices[j] = exists_with_indices[j].replace(factor,new_factor)
                    if debug:
                        logging.debug("decode_conditions: Switch count with list comprehension: exists_with_indices[j] = " + str(exists_with_indices[j]))
                    conditions[i] = conditions[i].replace('\"' + exists[j] + '\"', exists_with_indices[j])
                    if debug:
                        logging.debug("decode_conditions: Final condition result: conditions[i] = " + str(conditions[i]))
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
                        full_cond_percell = ' if ' + exists_with_indices[j]
                        conditions[i] = re.sub(r'(\d+)' + re.escape(full_cond_percell),
                                     r'\1*' + 'sum('+exists_with_indices_vec[j] +')'+full_cond_percell, conditions[i])
                    elif quantifier=='percellcost':
                        full_cond_percell = exists_with_indices[j]
                        conditions[i] = re.sub(r'' + re.escape(full_cond_percell),
                                               r'sum(' + exists_with_indices_vec[j] + ')',
                                               conditions[i])
    return conditions

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
        cond = re.findall(r',.*\)', home_made_func, re.M | re.I)
        cond = cond[0][1:-1]
        new_cond = "("+cond+" or "+str(indices[0])+"=="+str(indices[1])+")"
        home_made_func = home_made_func.replace(cond,new_cond)
    return home_made_func

def parse_conditions(conds,debug=False):
    conds = encode_conditions(conds)
    if debug:
        logging.debug("parse_conditions - after encoding: dimensions_columns_conds = " + str(conds))
    python_inputs = []
    for i in conds:
        e = shunting_yard(i);
        G, root = build_ast(e)
        python_inputs += [root.emit(G, context=None)]
    if debug:
        return decode_conditions(python_inputs,True)
    else:
        return decode_conditions(python_inputs)

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

def create_dimensions_matrix(dimensions_rows_categories_names, dimensions_columns_categories_names):
    dimensions_matrix = {row_name: dict() for row_name in dimensions_rows_categories_names}
    for row_name in dimensions_matrix:
        for col_name in dimensions_columns_categories_names:
            dimensions_matrix[row_name][col_name] = dict()
    return dimensions_matrix

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

def full_calc(strategies_vector, dimensions_rows_conds, dimensions_columns_conds, dimensions_rows_categories_names,
              dimensions_columns_categories_names, dimensions_ordered_row, dimensions_ordered_col, payment_conds):

    dimensions_rows_conds = parse_conditions(dimensions_rows_conds)
    dimensions_columns_conds = parse_conditions(dimensions_columns_conds,True)
    logging.debug("full_calc - after parsing: dimensions_columns_conds = " + str(dimensions_columns_conds))
    payment_conds = parse_conditions(payment_conds)
    dimensions_matrix = create_dimensions_matrix(dimensions_rows_categories_names,
                                                 dimensions_columns_categories_names)
    dimensions_matrix = classify_strategies_to_dimensions(strategies_vector, dimensions_matrix,
                                                          dimensions_rows_conds,
                                                          dimensions_columns_conds)
    dimensions_matrix = calc_payments(dimensions_matrix, payment_conds)
    dimensions_matrix = calc_MD_eq(dimensions_matrix, dimensions_ordered_row, dimensions_ordered_col)
    dimensions_matrix = calc_Global_eq(dimensions_matrix)
    return dimensions_matrix


def create_html_table(dimensions_matrix,dimensions_rows_categories_names,dimensions_columns_categories_names):
    def create_cell(strategy):
        strategy_cont = strategy
        if len(strategy) == 1:
            strategy_cont = strategy[0]
        strategy_str =  str(strategy_cont)
        if dimensions_matrix[row][col][strategy]["is_best_response"]:
            strategy_str = strategy_str + "*"
        return strategy_str + ", "
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
            if (dimensions_matrix[row][col]['best_response'] != ()):
                strategies+=create_cell(dimensions_matrix[row][col]['best_response'])
                strategy_for_link = dimensions_matrix[row][col]['best_response']
                TABLES+=[(dimensions_matrix[row][col]['best_response'] if len(dimensions_matrix[row][col]['best_response']) > 1 else dimensions_matrix[row][col]['best_response'][0], create_strategy_table(dimensions_matrix[row][col]['best_response']))]
            for strategy in dimensions_matrix[row][col]:
                if strategy != "best_response"  and strategy!=dimensions_matrix[row][col]['best_response']:
                    strategy_for_link = strategy
                    strategies+=create_cell(strategy)
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
    html_string=HTML_HEADER_TEXT+html_string;
    html_string += HTML_END_TEXT.replace("<csv_content_placeholder>",create_csv())

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


def convert_nested_ifs_to_strings(nested_if):
    #Converts all #<num> to \"#num\", for the excel unwrapper
    hastags = re.findall(r'(\#\d+)', nested_if, re.M | re.I)
    for hashtag in hastags:
        nested_if = nested_if.replace(hashtag,"\""+hashtag+"\"")
    return nested_if
# def read_costraints(excel_constraints):
#     python_constraints = [0 for i in range(len(excel_constraints))]
#     for i in range(len(excel_constraints)):
#         e = shunting_yard(excel_constraints[i])
#         G, root = build_ast(e)
#         python_constraints[i] = root.emit(G, context=None)
#     return python_constraints
# a
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
def strategies_filter(strategies,constraints):
    constraints = parse_conditions(constraints)
    filtered_strategies = filter_strategies_by_constraints(strategies, constraints)
    return filtered_strategies
@csrf_exempt
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # Read the form's content
        form = NameForm(request.POST)
        if form.is_valid():
            # Declaring all variables
            variables_definitions = dict()
            variables_names = dict()
            variables_values = dict()
            strategies_constraints = dict()
            payment_conds_dict = dict()
            payment_conds = []
            dimensions_rows_conds_dict = dict()
            dimensions_rows_conds = []
            dimensions_columns_conds_dict = dict()
            dimensions_columns_conds = []
            strategies_vectors = []
            dimensions_rows_categories_names = []
            dimensions_columns_categories_names = []
            all_strategies_generated = []

            # **********************************************************************************************************
            # functions for variable definition
            def replace_variables_definitions(value_with_variable,variables_definitions):
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

            # Process variables definitions from the form
            for datum in form.cleaned_data:
                if ("var_name" in datum):
                    if str(form.cleaned_data[datum]) != '':
                        variables_names[datum.split("_")[2]] = str(form.cleaned_data[datum])
                if ("var_val" in datum):
                    if str(form.cleaned_data[datum]) != '':
                        variables_values[datum.split("_")[2]] = str(form.cleaned_data[datum])
            for index in variables_names:
                variables_definitions[variables_names[index]] = variables_values[index]
            # **********************************************************************************************************

            # **********************************************************************************************************
            # Process conditions
            conditions = []
            for datum in form.cleaned_data:
                if ("dimension" in datum) and ("row" in datum) and ("cond" in datum):
                    if str(form.cleaned_data[datum]) == 'else':
                        last = str("\""+form.cleaned_data[datum.replace('cond', 'name').replace('if', 'category')]+"\"")
                    elif str(form.cleaned_data[datum]) != '':
                        conditions += [str("IF(" + form.cleaned_data[datum] + ",\"" + form.cleaned_data[
                                datum.replace('cond', 'name').replace('if', 'category')] + "\",<next_condition>)")]

            for i in range(1,len(conditions)):
                conditions[i] = conditions[i].replace("<next_condition>",conditions[i-1])
            dimensions_rows_conds_dict['dimensions_row_if_cond_1'] = "="+conditions[len(conditions)-1].replace("<next_condition>", last)
            strategies_symbols = re.findall("[-,=><(](s[0-9a-z]+?|r[0-9a-z]+?)", dimensions_rows_conds_dict['dimensions_row_if_cond_1'])
            for symbol in strategies_symbols:
                dimensions_rows_conds_dict['dimensions_row_if_cond_1'] = dimensions_rows_conds_dict['dimensions_row_if_cond_1'].replace(symbol,symbol[0]+"_"+symbol[1:])

            conditions = []
            for datum in form.cleaned_data:
                if ("dimension" in datum) and ("column" in datum) and ("cond" in datum):
                    if str(form.cleaned_data[datum]) == 'else':
                        last = str("\"" + form.cleaned_data[datum.replace('cond', 'name').replace('if', 'category')] + "\"")
                    elif str(form.cleaned_data[datum]) != '':
                        conditions += [str("IF(" + form.cleaned_data[datum] + ",\"" + form.cleaned_data[
                            datum.replace('cond', 'name').replace('if', 'category')] + "\",<next_condition>)")]

            for i in range(1, len(conditions)):
                conditions[i] = conditions[i].replace("<next_condition>", conditions[i - 1])
            dimensions_columns_conds_dict['dimensions_column_if_cond_1'] = "=" + conditions[len(conditions) - 1].replace("<next_condition>", last)
            strategies_symbols = re.findall("[-,=><(](s[0-9a-z]+?|r[0-9a-z]+?)",dimensions_columns_conds_dict['dimensions_column_if_cond_1'])
            for symbol in strategies_symbols:
                dimensions_columns_conds_dict['dimensions_column_if_cond_1'] = dimensions_columns_conds_dict['dimensions_column_if_cond_1'].replace(symbol, symbol[0] + "_" + symbol[1:])

            for datum in form.cleaned_data:
                if str(form.cleaned_data[datum]) != '':
                    if "constraint" in datum:
                        strategies_constraints[datum] = str(form.cleaned_data[datum])
                    if ("payment" in datum) and ("cond" in datum):
                        payment_conds_dict[datum] =  str("=IF(" + form.cleaned_data[datum] + "," + form.cleaned_data[datum.replace('cond','res')] + ",0)")

            for cond in payment_conds_dict:
                if payment_conds_dict[cond]!='':
                    payment_conds +=[payment_conds_dict[cond]]

            payment_conds_temp = []
            for cond in payment_conds:
                strategies_symbols = re.findall("[-,=><(](s[0-9a-z]+?|r[0-9a-z]+?)",cond)
                for symbol in strategies_symbols:
                    cond = cond.replace(symbol, symbol[0] + "_" + symbol[1:])
                payment_conds_temp += [cond]
            payment_conds = payment_conds_temp
            payment_conds = replace_variables_definitions_in_condition(payment_conds,variables_definitions)

            for cond in dimensions_rows_conds_dict:
                if dimensions_rows_conds_dict[cond]!='':
                    dimensions_rows_conds +=[dimensions_rows_conds_dict[cond]]

            dimensions_rows_conds_temp = []
            for cond in dimensions_rows_conds:
                strategies_symbols = re.findall("[-,=><(](s[0-9a-z]+?|r[0-9a-z]+?)", cond)
                for symbol in strategies_symbols:
                    cond = cond.replace(symbol, symbol[0] + "_" + symbol[1:])
                dimensions_rows_conds_temp += [cond]
            dimensions_rows_conds = dimensions_rows_conds_temp
            dimensions_rows_conds = replace_variables_definitions_in_condition(dimensions_rows_conds, variables_definitions)

            for cond in dimensions_columns_conds_dict:
                if dimensions_columns_conds_dict[cond]!='':
                    dimensions_columns_conds +=[dimensions_columns_conds_dict[cond]]

            dimensions_columns_conds_temp = []
            for cond in dimensions_columns_conds:
                strategies_symbols = re.findall("[-,=><(](s[0-9a-z]+?|r[0-9a-z]+?)", cond)
                for symbol in strategies_symbols:
                    cond = cond.replace(symbol, symbol[0] + "_" + symbol[1:])
                dimensions_columns_conds_temp += [cond]
            dimensions_columns_conds = dimensions_columns_conds_temp
            dimensions_columns_conds = replace_variables_definitions_in_condition(dimensions_columns_conds,
                                                                               variables_definitions)
            logging.debug("Preprocessing: dimensions_columns_conds = " + str(dimensions_columns_conds))
            # **********************************************************************************************************

            # **********************************************************************************************************
            # Process generator fields
            strategies_full_set = ""
            if form.cleaned_data["strategies_vector_single"] != '':
                tuples = re.findall("\(.+?\)", str(form.cleaned_data["strategies_vector_single"]))
                new_single_vector = str(form.cleaned_data["strategies_vector_single"])
                for tup in tuples:
                    new_single_vector = new_single_vector.replace(tup,"")
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
            elif form.cleaned_data["strategies_upper_bound"]!='' and form.cleaned_data["strategies_lower_bound"]!='':
                strategies_vectors = str([i for i in range(int(replace_variables_definitions(form.cleaned_data["strategies_lower_bound"], variables_definitions)),int(replace_variables_definitions(form.cleaned_data["strategies_upper_bound"], variables_definitions))+1)]).replace("[","").replace("]","").replace(" ","")
            else:
                strategies_vectors_str = dict()
                strategies_vectors = []
                for datum in form.cleaned_data:
                    if ("vector" in datum) and not ("length" in datum):
                        strategies_vectors_str[datum] = form.cleaned_data[datum]
                        if str(strategies_vectors_str[datum]) != '':
                            strategies_vectors+= [[eval(str(strategies_vectors_str[datum]))]]
                strategies_vectors = [list(strategy[0]) if type(strategy[0]) == tuple else strategy for strategy in
                                      strategies_vectors]
            for i in range(1,11):
                field_name = "dimensions_row_category_name_"+str(i)
                if str(form.cleaned_data[field_name]) != '':
                    dimensions_rows_categories_names+=[str(form.cleaned_data[field_name])]
            dimensions_rows_categories_names = replace_variables_definitions_in_condition(dimensions_rows_categories_names,
                                                                               variables_definitions)

            for i in range(1, 11):
                field_name = "dimensions_column_category_name_" + str(i)
                if str(form.cleaned_data[field_name]) != '':
                    dimensions_columns_categories_names += [str(form.cleaned_data[field_name])]
            dimensions_columns_categories_names = replace_variables_definitions_in_condition(dimensions_columns_categories_names,
                                                                               variables_definitions)
            strategies_vector_length = 0
            strategies_full_set = ""
            for datum in form.cleaned_data:
                if ("strategies_vector_length" in datum):
                    if str(form.cleaned_data[datum]) != '':
                        strategies_vector_length = int(replace_variables_definitions(form.cleaned_data[datum], variables_definitions))
                if ("strategies_full_set" in datum):
                    if str(form.cleaned_data[datum]) != '':
                        strategies_full_set = replace_variables_definitions(form.cleaned_data[datum], variables_definitions)

            if (strategies_vector_length != 0):
                if strategies_full_set == "":
                    strategies_full_set = replace_variables_definitions(strategies_vectors, variables_definitions)
                if "ignore permutations" in strategies_constraints:
                    del strategies_constraints["ignore permutations"]
                    all_strategies_generated = generate_all_strategies_combinations(strategies_vector_length, strategies_full_set)
                else:
                    all_strategies_generated = generate_all_strategies_product(strategies_vector_length, strategies_full_set)
                strategies_constraints=convert_to_excel_conds(strategies_constraints)
                strategies_vectors = strategies_filter(all_strategies_generated,strategies_constraints)
            # **********************************************************************************************************

            # **********************************************************************************************************
            # Run the Calc
            dimensions_matrix=full_calc(strategies_vectors, dimensions_rows_conds, dimensions_columns_conds,dimensions_rows_categories_names,dimensions_columns_categories_names,dimensions_rows_categories_names,dimensions_columns_categories_names,payment_conds)
            return HttpResponse(create_html_table(dimensions_matrix,dimensions_rows_categories_names,dimensions_columns_categories_names))
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



