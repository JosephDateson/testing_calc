HTML_HEADER_TEXT = "<!DOCTYPE html>" \
                   "<html lang='en' class='no-js'>" \
                   "   <head>" \
                   "      <script></script>" \
                   "      <style>td.formatted_square_hide{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}td.formatted_square_show{white-space:normal;overflow:hidden;text-overflow:ellipsis;}a.on_green{color:blue;text-decoration:underline;}a.on_green:hover {	color: #7c8d87;text-decoration: underline;}table.fixed { table-layout:fixed; word-break:break-all;}	</style>" \
                   "      <meta charset='UTF-8' />" \
                   "      <meta http-equiv='X-UA-Compatible' content='IE=edge,chrome=1'>" \
                   "      <meta name='viewport' content='width=device-width, initial-scale=1.0'>" \
                   "      <title>Multi-Dimensional Equilibrium Calculator - Result</title>" \
                   "      <meta name='description' content='Sticky Table Headers Revisited: Creating functional and flexible sticky table headers' />" \
                   "      <meta name='keywords' content='Sticky Table Headers Revisited' />" \
                   "      <meta name='author' content='Codrops' />" \
                   "      <link rel='shortcut icon' href='../favicon.ico'>" \
                   "      <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'>" \
                   "      <style> article,aside,details,figcaption,figure,footer,header,hgroup,main,nav,section,summary{display:block;}audio,canvas,video{display:inline-block;}audio:not([controls]){display:none;height:0;}[hidden]{display:none;}html{font-family:sans-serif;-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%;}body{margin:0;}a:focus{outline:thin dotted;}a:active,a:hover{outline:0;}h1{font-size:2em;margin:0.67em 0;}abbr[title]{border-bottom:1px dotted;}b,strong{font-weight:bold;}dfn{font-style:italic;}hr{-moz-box-sizing:content-box;box-sizing:content-box;height:0;}mark{background:#ff0;color:#000;}code,kbd,pre,samp{font-family:monospace,serif;font-size:1em;}pre{white-space:pre-wrap;}q{quotes:'\201C' '\201D' '\2018' '\2019';}small{font-size:80%;}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline;}sup{top:-0.5em;}sub{bottom:-0.25em;}img{border:0;}svg:not(:root){overflow:hidden;}figure{margin:0;}fieldset{border:1px solid #c0c0c0;margin:0 2px;padding:0.35em 0.625em 0.75em;}legend{border:0;padding:0;}button,input,select,textarea{font-family:inherit;font-size:100%;margin:0;}button,input{line-height:normal;}button,select{text-transform:none;}button,html input[type='button'],input[type='reset'],input[type='submit']{-webkit-appearance:button;cursor:pointer;}button[disabled],html input[disabled]{cursor:default;}input[type='checkbox'],input[type='radio']{box-sizing:border-box;padding:0;}input[type='search']{-webkit-appearance:textfield;-moz-box-sizing:content-box;-webkit-box-sizing:content-box;box-sizing:content-box;}input[type='search']::-webkit-search-cancel-button,input[type='search']::-webkit-search-decoration{-webkit-appearance:none;}button::-moz-focus-inner,input::-moz-focus-inner{border:0;padding:0;}textarea{overflow:auto;vertical-align:top;}table{border-collapse:collapse;border-spacing:0;} </style>" \
                   "      <style> @import url(http://fonts.googleapis.com/css?family=Lato:300,400,700); @font-face { font-family: 'codropsicons'; src:url('../fonts/codropsicons/codropsicons.eot'); src:url('../fonts/codropsicons/codropsicons.eot?#iefix') format('embedded-opentype'), url('../fonts/codropsicons/codropsicons.woff') format('woff'), url('../fonts/codropsicons/codropsicons.ttf') format('truetype'), url('../fonts/codropsicons/codropsicons.svg#codropsicons') format('svg'); font-weight: normal; font-style: normal; } *, *:after, *:before { -webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box; } body { font-family: 'Lato', Arial, sans-serif; color: #7c8d87; background: #f8f8f8; } a { color: #31bc86; text-decoration: none; } a:hover, a:focus { color: #7c8d87; } .container > header { margin: 0 auto; padding: 2em; text-align: center; background: rgba(0,0,0,0.01); } .container > header h1 { font-size: 2.625em; line-height: 1.3; margin: 0; font-weight: 300; } .container > header span { display: block; font-size: 60%; opacity: 0.7; padding: 0 0 0.6em 0.1em; } /* To Navigation Style */ .codrops-top { background: #fff; background: rgba(255, 255, 255, 0.6); text-transform: uppercase; width: 100%; font-size: 0.69em; line-height: 2.2; } .codrops-top a { text-decoration: none; padding: 0 1em; letter-spacing: 0.1em; display: inline-block; } .codrops-top a:hover { background: rgba(255,255,255,0.95); } .codrops-top span.right { float: right; } .codrops-top span.right a { float: left; display: block; } .codrops-icon:before { font-family: 'codropsicons'; margin: 0 4px; speak: none; font-style: normal; font-weight: normal; font-variant: normal; text-transform: none; line-height: 1; -webkit-font-smoothing: antialiased; } .codrops-icon-drop:before { content: '\e001'; } .codrops-icon-prev:before { content: '\e004'; } /* Demo Buttons Style */ .codrops-demos { padding-top: 1em; font-size: 0.8em; } .codrops-demos a { display: inline-block; margin: 0.5em; padding: 0.7em 1.1em; outline: none; border: 2px solid #31bc86; text-decoration: none; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; } .codrops-demos a:hover, .codrops-demos a.current-demo, .codrops-demos a.current-demo:hover { border-color: #7c8d87; color: #7c8d87; } .related { text-align: center; font-size: 1.5em; padding-bottom: 3em; } @media screen and (max-width: 25em) { .codrops-icon span { display: none; } } </style>" \
                   "      <style> /* Component styles */ @font-face { font-family: 'Blokk'; src: url('../fonts/blokk/BLOKKRegular.eot'); src: url('../fonts/blokk/BLOKKRegular.eot?#iefix') format('embedded-opentype'), url('../fonts/blokk/BLOKKRegular.woff') format('woff'), url('../fonts/blokk/BLOKKRegular.svg#BLOKKRegular') format('svg'); font-weight: normal; font-style: normal; } .component { line-height: 1.5em; margin: 0 auto; padding: 2em 0 3em; width: 90%; max-width: 1000px; overflow: hidden; } .component .filler { font-family: 'Blokk', Arial, sans-serif; color: #d3d3d3; } table { border-collapse: collapse; margin-bottom: 3em; width: 100%; background: #fff; } td, th { padding: 0.75em 1.5em; text-align: left; } td.err { background-color: #e992b9; color: #fff; font-size: 0.75em; text-align: center; line-height: 1; } th { background-color: #31bc86; font-weight: bold; color: #fff; white-space: nowrap; } tbody th { background-color: #2ea879; } tbody tr:nth-child(2n-1) { background-color: #f5f5f5; transition: all .125s ease-in-out; } tbody tr:hover { background-color: rgba(129,208,177,.3); } /* For appearance */ .sticky-wrap { overflow-x: auto; overflow-y: hidden; position: relative; margin: 3em 0; width: 100%; } .sticky-wrap .sticky-thead, .sticky-wrap .sticky-col, .sticky-wrap .sticky-intersect { opacity: 0; position: absolute; top: 0; left: 0; transition: all .125s ease-in-out; z-index: 50; width: auto; /* Prevent table from stretching to full size */ } .sticky-wrap .sticky-thead { box-shadow: 0 0.25em 0.1em -0.1em rgba(0,0,0,.125); z-index: 100; width: 100%; /* Force stretch */ } .sticky-wrap .sticky-intersect { opacity: 1; z-index: 150; } .sticky-wrap .sticky-intersect th { background-color: #666; color: #eee; } .sticky-wrap td, .sticky-wrap th { box-sizing: border-box; } /* Not needed for sticky header/column functionality */ td.user-name { text-transform: capitalize; } .sticky-wrap.overflow-y { overflow-y: auto; max-height: 50vh; } </style>" \
                   "      <!--[if IE]> <script src='http://html5shiv.googlecode.com/svn/trunk/html5.js'></script> <![endif]-->" \
                   "  </head>" \
                   "   <body>" \
                   "      <div class='container'>" \
                   "      <!-- Top Navigation -->" \
                   "      <header>" \
                   "         <h1>Multi-Dimensional Equilibrium Calculator - <em>Result</em> <span>#date#</span></h1>" \
                   "         <nav class='codrops-demos'> <a onclick='save();' href='#'>Downalod current page</a> <a class='current-demo' href='#' onclick='download_csv(\"result.csv\",\"a\")'>Download Excel version</a> </nav>" \
                   "      </header>" \
                   "      <div class='component'>" \
                   "      <div class='panel panel-default'>" \
                   "         <div class='panel-heading'>" \
                   "            <a data-toggle='collapse' href='#collapse1'>" \
                   "               <h4>How to read the tables?</h4>" \
                   "            </a>" \
                   "         </div>" \
                   "         <div class='panel-collapse collapse in' id='collapse1'>" \
                   "            <div class='panel-body'>" \
                   "               <b>The top table</b> presents the multi-dimensional partition into cells of all strategies. <br><b>The second table</b> presents the score of each cell's best response against a uniform distribution on the chosen cell from the first table.<br><b> A cell's result will appear in the second table by clicking on it.</b> <br><br> <b><u>Conventions &amp; Notations</u> </b><br><br>" \
                   "               <table>" \
                   "                  <tbody>" \
                   "                     <tr>" \
                   "                        <td>(1,2)*</td>" \
                   "                        <td> A star superscript on a strategy denotes a best response againt the cell itself. </td>" \
                   "                     </tr>" \
                   "                     <tr>" \
                   "                        <td><font color='red'>(1,2)</font></td>" \
                   "                        <td> A cell colored red denotes a multi-dimensional equilibrium.</td>" \
                   "                     </tr>" \
                   "                     <tr>" \
                   "                        <td><font color='red'><u>(1,2)</u></font></td>" \
                   "                        <td> A cell colored red and underlined denotes a gloabl equilibrium.</td>" \
                   "                     </tr>" \
                   "                     <tr>" \
                   "                        <td><font color='blue'>Best Response: 4<br>    Score: 1.5</font></td>" \
                   "                        <td> <b>In the second table, </b>a cell colored blue denotes the chosen cell. <br>'Best response' is the cell's best response against the chosen cell, and 'Score' is its score against the chosen cell. </td>" \
                   "                     </tr>" \
                   "                  </tbody>" \
                   "               </table>" \
                   "            </div>" \
                   "         </div>" \
                   "      </div>" \
                   "      "
HTML_END_TEXT = "</div>" \
                "</div>" \
                "<!-- /container -->" \
                "   <script>" \
                "       function myFunction(show) {" \
                "           if (show ==1){" \
                "               var cur_class_name='formatted_square_hide';" \
                "               var new_class_name='formatted_square_show';" \
                "               document.getElementById('show_hide_strategies').setAttribute('onclick','return myFunction(0);');" \
                "               document.getElementById('show_hide_strategies').innerHTML='(click to hide all strategies)';" \
                "           }else{" \
                "               var cur_class_name='formatted_square_show';" \
                "               var new_class_name='formatted_square_hide';" \
                "               document.getElementById('show_hide_strategies').setAttribute('onclick','return myFunction(1);');" \
                "               document.getElementById('show_hide_strategies').innerHTML='(click to show all strategies)';" \
                "           }" \
                "           while (document.getElementsByClassName(cur_class_name).length){" \
                "               document.getElementsByClassName(cur_class_name)[0].className = new_class_name;" \
                "           }" \
                "       }" \
                "   </script> " \
                "   <script src='http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js'></script> " \
                "   <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery-throttle-debounce/1.1/jquery.ba-throttle-debounce.min.js'></script> " \
                "   <script> " \
                "       $(function(){ " \
                "           $('table').each(function() { " \
                "               if($(this).find('thead').length > 0 && $(this).find('th').length > 0) " \
                "                   { // Clone <thead> var $w = $(window), $t = $(this), $thead = $t.find('thead').clone(), $col = $t.find('thead, tbody').clone(); " \
                "                     // Add class, remove margins, reset width and wrap table $t .addClass('sticky-enabled') .css({ margin: 0, width: '100%' }).wrap('<div class='sticky-wrap' />'); " \
                "               if($t.hasClass('overflow-y')) " \
                "                   $t.removeClass('overflow-y').parent().addClass('overflow-y'); " \
                "               // Create new sticky table head (basic) $t.after('<table class='sticky-thead' />'); " \
                "               // If <tbody> contains <th>, then we create sticky column and intersect (advanced) " \
                "                  if($t.find('tbody th').length > 0) { " \
                "                   $t.after('<table class='sticky-col' /><table class='sticky-intersect' />'); " \
                "           } // Create shorthand for things " \
                "           var $stickyHead = $(this).siblings('.sticky-thead'), $stickyCol = $(this).siblings('.sticky-col'), $stickyInsct = $(this).siblings('.sticky-intersect'), $stickyWrap = $(this).parent('.sticky-wrap'); " \
                "           $stickyHead.append($thead); " \
                "           $stickyCol .append($col) .find('thead th:gt(0)').remove() .end() .find('tbody td').remove(); " \
                "           $stickyInsct.html('<thead><tr><th>'+$t.find('thead th:first-child').html()+'</th></tr></thead>'); " \
                "           // Set widths var setWidths = function () { " \
                "               $t .find('thead th').each(function (i) { $stickyHead.find('th').eq(i).width($(this).width()); }) .end() .find('tr').each(function (i) { $stickyCol.find('tr').eq(i).height($(this).height()); }); " \
                "           // Set width of sticky table head $stickyHead.width($t.width()); " \
                "           // Set width of sticky table col $stickyCol.find('th').add($stickyInsct.find('th')).width($t.find('thead th').width()) }, repositionStickyHead = function () { // Return value of calculated allowance var allowance = calcAllowance(); " \
                "           // Check if wrapper parent is overflowing along the y-axis if($t.height() > $stickyWrap.height()) { // If it is overflowing (advanced layout) " \
                "           // Position sticky header based on wrapper scrollTop() if($stickyWrap.scrollTop() > 0) { " \
                "           // When top of wrapping parent is out of view $stickyHead.add($stickyInsct).css({ opacity: 1, top: $stickyWrap.scrollTop() }); } else { " \
                "           // When top of wrapping parent is in view $stickyHead.add($stickyInsct).css({ opacity: 0, top: 0 }); } } else { " \
                "           // If it is not overflowing (basic layout) " \
                "           // Position sticky header based on viewport scrollTop if($w.scrollTop() > $t.offset().top && $w.scrollTop() < $t.offset().top + $t.outerHeight() - allowance) { " \
                "           // When top of viewport is in the table itself $stickyHead.add($stickyInsct).css({ opacity: 1, top: $w.scrollTop() - $t.offset().top }); } else { " \
                "           // When top of viewport is above or below table $stickyHead.add($stickyInsct).css({ opacity: 0, top: 0 }); } } }, repositionStickyCol = function () { " \
                "           if($stickyWrap.scrollLeft() > 0) { " \
                "           // When left of wrapping parent is out of view $stickyCol.add($stickyInsct).css({ opacity: 1, left: $stickyWrap.scrollLeft() }); } else { " \
                "           // When left of wrapping parent is in view $stickyCol .css({ opacity: 0 }) .add($stickyInsct).css({ left: 0 }); } }, calcAllowance = function () { " \
                "           var a = 0; " \
                "           // Calculate allowance $t.find('tbody tr:lt(3)').each(function () { a += $(this).height(); }); " \
                "           // Set fail safe limit (last three row might be too tall) // Set arbitrary limit at 0.25 of viewport height, or you can use an arbitrary pixel value if(a > $w.height()*0.25) { a = $w.height()*0.25; } " \
                "           // Add the height of sticky header a += $stickyHead.height(); return a; }; setWidths(); $t.parent('.sticky-wrap').scroll($.throttle(250, function() { repositionStickyHead(); repositionStickyCol(); })); $w .load(setWidths) .resize($.debounce(250, function () { setWidths(); repositionStickyHead(); " \
                "           repositionStickyCol(); })) .scroll($.throttle(250, repositionStickyHead)); } }); });" \
                "   </script>" \
                "   <script> " \
                "       function download_csv(filename, text) {" \
                "           text='<csv_content_placeholder>';" \
                "           var element = document.createElement('a');" \
                "           element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));" \
                "           element.setAttribute('download', filename);  " \
                "           element.style.display = 'none';  " \
                "           document.body.appendChild(element);  " \
                "           element.click();  " \
            "               document.body.removeChild(element);" \
                "       }" \
                "   </script>" \
                "   <script>" \
                "       function save() {" \
                "           var html = document.documentElement.outerHTML;	" \
            "               var save_name = 'result';var temp_save_element = document.createElement('a');	" \
                "           temp_save_element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(html));	" \
                "           temp_save_element.setAttribute('download', save_name+'.html');	" \
                "           temp_save_element.style.display = 'none';	" \
                "           document.body.appendChild(temp_save_element);	" \
                "           temp_save_element.click();	" \
                "           document.body.removeChild(temp_save_element);" \
                "       }" \
                "   </script> " \
                "  </body> " \
                "</html>"
