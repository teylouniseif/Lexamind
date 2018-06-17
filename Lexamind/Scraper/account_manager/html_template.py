#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  30 21:57:00 2018
@author: Saif Kurdi-Teylouni
"""
import jsonpickle, re

class Template(object):

    emailStart="\r\n" \
    			"<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\r\n" \
    			"<html xmlns=\"http://www.w3.org/1999/xhtml\">\r\n" \
    			"\r\n" \
    			"<body style=\"min-width: 100%;-webkit-text-size-adjust: 100%;-ms-text-size-adjust: 100%;margin: 0;padding: 0;-moz-box-sizing: border-box;-webkit-box-sizing: border-box;box-sizing: border-box;width: 100% !important;\">\r\n" \
    			"  <!-- <style> -->\r\n" \
    			"  <table class=\"body\" data-made-with-foundation style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse;width: 100%;border-spacing: 0;padding: 0;vertical-align: top;text-align: left;\">\r\n" \
    			"    <tr style=\"padding: 0;vertical-align: top;text-align: left;\">\r\n" \
    			"      <td class=\"float-center\" id=\"no-border\" align=\"center\" valign=\"top\" style=\"border-bottom: 0;border-collapse: collapse !important;word-wrap: break-word;-webkit-hyphens: auto;-moz-hyphens: auto;hyphens: auto;padding: 0;vertical-align: top;text-align: left;\">\r\n" \
    			"        <center style=\"width: 100%;min-width: 580px;\">\r\n" \
    			"\r\n" \
    			"            <div class=\"newsletter\" style=\"margin: 5%;\">\r\n" \
    			"                <div class=\"title\">\r\n"

    emailEnd=" </table></div>\r\n"\
    			"              \r\n"\
    			"              </center></td></tr></table>\r\n"\
    			"                \r\n"\
    			"          \r\n"\
    			"        \r\n"\
    			"      \r\n"\
    			"    \r\n"\
    			"  \r\n"\
    			"</body>\r\n"\
    			"</html>\r\n"\
    			""

    rowfont= """   </div>\r\n
              <table style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse;width: 100%;border-spacing: 0;padding: 0;vertical-align: top;text-align: left;\">\r\n
                <tr class=\"column-titles\" style=\"padding: 0;vertical-align: top;text-align: left;font-family: 'Josefin Sans', sans-serif;\">\r\n
                  <th class=\"even\" style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse;font-family: 'Tahoma', sans-serif;padding: 10px;\"><span style=\"background-color: rgba(255,242,0,1);\">Projet de loi</span></th>\r\n
                  <th style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse;font-family: 'Tahoma', sans-serif;padding: 10px;\"><span style=\"background-color: rgba(255,242,0,1);\">Loi amendée</span></th> \r\n
                  <th class=\"even\" style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse;font-family: 'Tahoma', sans-serif;padding: 10px;\"><span style=\"background-color: rgba(255,242,0,1);\">Statut</span></th>\r\n
                  <th style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse;font-family: 'Tahoma', sans-serif;padding: 10px;\"><span style=\"background-color: rgba(255,242,0,1);\">Date</span></th>\r\n
                  <th class=\"even\" style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse;font-family: 'Tahoma', sans-serif;padding: 10px;\"><span style=\"background-color: rgba(255,242,0,1);\">Législature</span></th>\r\n
                  <th class=\"even\" style=\"border-bottom: 1px solid rgba(0,0,0,0.2);border-collapse: collapse;font-family: 'Tahoma', sans-serif;padding: 10px;\"><span style=\"background-color: rgba(255,242,0,1);\">Hyperlien</span></th>\r\n
                </tr>\r\n
               \r\n"""

    emailfont="<head>\r\n" \
    "  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\r\n" \
    "  <meta name=\"viewport\" content=\"width=device-width\">\r\n" \
    "  <title>Title</title>\r\n" \
    "  <style>\r\n" \
    "\r\n" \
    "span{\r\n" \
    "  background-color: rgba(255,242,0,1);\r\n" \
    "}\r\n" \
    "\r\n" \
    "#no-border{\r\n" \
    "  border-bottom: 0;\r\n" \
    "}\r\n" \
    "\r\n" \
    "#logo{\r\n" \
    "  width: 20%;\r\n" \
    "  margin: 50px;\r\n" \
    "}\r\n" \
    "\r\n" \
    ".newsletter{\r\n" \
    "  margin: 5%\r\n" \
    "}\r\n" \
    "table, th, td {\r\n" \
    "    border-bottom: 1px solid rgba(0,0,0,0.2);\r\n" \
    "    border-collapse: collapse;\r\n" \
    "}\r\n" \
    "\r\n" \
    "table {\r\n" \
    "  width:100%;\r\n" \
    "\r\n" \
    "}\r\n" \
    "h1 {\r\n" \
    "  font-family: 'Josefin Sans', sans-serif;\r\n" \
    "  font-size: 60px;\r\n" \
    "}\r\n" \
    ".column-titles{\r\n" \
    "  font-family: 'Josefin Sans', sans-serif;\r\n" \
    "  text-align: left;\r\n" \
    "}\r\n" \
    "\r\n" \
    ".column-titles th{\r\n" \
    "  font-family: 'Josefin Sans', sans-serif;\r\n" \
    "  padding: 10px;\r\n" \
    "}\r\n" \
    "\r\n" \
    ".data-row td {\r\n" \
    " padding: 10px;\r\n" \
    "  font-family: 'Roboto', sans-serif;\r\n" \
    "}\r\n" \
    "\r\n" \
    "/* .new{\r\n" \
    "  background-color: #B8E986;\r\n" \
    "}\r\n" \
    ".modified{\r\n" \
    "  background-color: #E9E386;\r\n" \
    "}\r\n" \
    ".annuled{\r\n" \
    "  background-color: #E9C286;\r\n" \
    "}\r\n" \
    ".dropped{\r\n" \
    "  background-color: #E9A186;\r\n" \
    "}\r\n" \
    "\r\n" \
    ".replaced{\r\n" \
    "  background-color: #E98986;\r\n" \
    "} */\r\n" \
    ".wrapper {\r\n" \
    "  width: 100%; }\r\n" \
    "\r\n" \
    "#outlook a {\r\n" \
    "  padding: 0; }\r\n" \
    "\r\n" \
    "body {\r\n" \
    "  width: 100% !important;\r\n" \
    "  min-width: 100%;\r\n" \
    "  -webkit-text-size-adjust: 100%;\r\n" \
    "  -ms-text-size-adjust: 100%;\r\n" \
    "  margin: 0;\r\n" \
    "  Margin: 0;\r\n" \
    "  padding: 0;\r\n" \
    "  -moz-box-sizing: border-box;\r\n" \
    "  -webkit-box-sizing: border-box;\r\n" \
    "  box-sizing: border-box; }\r\n" \
    "\r\n" \
    ".ExternalClass {\r\n" \
    "  width: 100%; }\r\n" \
    "  .ExternalClass,\r\n" \
    "  .ExternalClass p,\r\n" \
    "  .ExternalClass span,\r\n" \
    "  .ExternalClass font,\r\n" \
    "  .ExternalClass td,\r\n" \
    "  .ExternalClass div {\r\n" \
    "    line-height: 100%; }\r\n" \
    "\r\n" \
    "#backgroundTable {\r\n" \
    "  margin: 0;\r\n" \
    "  Margin: 0;\r\n" \
    "  padding: 0;\r\n" \
    "  width: 100% !important;\r\n" \
    "  line-height: 100% !important; }\r\n" \
    "\r\n" \
    "img {\r\n" \
    "  outline: none;\r\n" \
    "  text-decoration: none;\r\n" \
    "  -ms-interpolation-mode: bicubic;\r\n" \
    "  width: auto;\r\n" \
    "  max-width: 100%;\r\n" \
    "  clear: both;\r\n" \
    "  display: block; }\r\n" \
    "\r\n" \
    "center {\r\n" \
    "  width: 100%;\r\n" \
    "  min-width: 580px; }\r\n" \
    "\r\n" \
    "a img {\r\n" \
    "  border: none; }\r\n" \
    "\r\n" \
    "p {\r\n" \
    "  margin: 0 0 0 10px;\r\n" \
    "  Margin: 0 0 0 10px; }\r\n" \
    "\r\n" \
    "table {\r\n" \
    "  border-spacing: 0;\r\n" \
    "  border-collapse: collapse; }\r\n" \
    "\r\n" \
    "td {\r\n" \
    "  word-wrap: break-word;\r\n" \
    "  -webkit-hyphens: auto;\r\n" \
    "  -moz-hyphens: auto;\r\n" \
    "  hyphens: auto;\r\n" \
    "  border-collapse: collapse !important; }\r\n" \
    "\r\n" \
    "table, tr, td {\r\n" \
    "  padding: 0;\r\n" \
    "  vertical-align: top;\r\n" \
    "  text-align: left; }\r\n" \
    "\r\n" \
    "@media only screen {\r\n" \
    "  html {\r\n" \
    "    min-height: 100%;\r\n" \
    "    background: #f3f3f3; } }\r\n" \
    "\r\n" \
    "table.body {\r\n" \
    "  background: #f3f3f3;\r\n" \
    "  height: 100%;\r\n" \
    "  width: 100%; }\r\n" \
    "\r\n" \
    "table.container {\r\n" \
    "  background: #fefefe;\r\n" \
    "  width: 580px;\r\n" \
    "  margin: 0 auto;\r\n" \
    "  Margin: 0 auto;\r\n" \
    "  text-align: inherit; }\r\n" \
    "\r\n" \
    "table.row {\r\n" \
    "  padding: 0;\r\n" \
    "  width: 100%;\r\n" \
    "  position: relative; }\r\n" \
    "\r\n" \
    "table.spacer {\r\n" \
    "  width: 100%; }\r\n" \
    "  table.spacer td {\r\n" \
    "    mso-line-height-rule: exactly; }\r\n" \
    "\r\n" \
    "table.container table.row {\r\n" \
    "  display: table; }\r\n" \
    "\r\n" \
    "td.columns,\r\n" \
    "td.column,\r\n" \
    "th.columns,\r\n" \
    "th.column {\r\n" \
    "  margin: 0 auto;\r\n" \
    "  Margin: 0 auto;\r\n" \
    "  padding-left: 16px;\r\n" \
    "  padding-bottom: 16px; }\r\n" \
    "  td.columns .column,\r\n" \
    "  td.columns .columns,\r\n" \
    "  td.column .column,\r\n" \
    "  td.column .columns,\r\n" \
    "  th.columns .column,\r\n" \
    "  th.columns .columns,\r\n" \
    "  th.column .column,\r\n" \
    "  th.column .columns {\r\n" \
    "    padding-left: 0 !important;\r\n" \
    "    padding-right: 0 !important; }\r\n" \
    "    td.columns .column center,\r\n" \
    "    td.columns .columns center,\r\n" \
    "    td.column .column center,\r\n" \
    "    td.column .columns center,\r\n" \
    "    th.columns .column center,\r\n" \
    "    th.columns .columns center,\r\n" \
    "    th.column .column center,\r\n" \
    "    th.column .columns center {\r\n" \
    "      min-width: none !important; }\r\n" \
    "\r\n" \
    "td.columns.last,\r\n" \
    "td.column.last,\r\n" \
    "th.columns.last,\r\n" \
    "th.column.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    "td.columns table:not(.button),\r\n" \
    "td.column table:not(.button),\r\n" \
    "th.columns table:not(.button),\r\n" \
    "th.column table:not(.button) {\r\n" \
    "  width: 100%; }\r\n" \
    "\r\n" \
    "td.large-1,\r\n" \
    "th.large-1 {\r\n" \
    "  width: 32.33333px;\r\n" \
    "  padding-left: 8px;\r\n" \
    "  padding-right: 8px; }\r\n" \
    "\r\n" \
    "td.large-1.first,\r\n" \
    "th.large-1.first {\r\n" \
    "  padding-left: 16px; }\r\n" \
    "\r\n" \
    "td.large-1.last,\r\n" \
    "th.large-1.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    ".collapse > tbody > tr > td.large-1,\r\n" \
    ".collapse > tbody > tr > th.large-1 {\r\n" \
    "  padding-right: 0;\r\n" \
    "  padding-left: 0;\r\n" \
    "  width: 48.33333px; }\r\n" \
    "\r\n" \
    ".collapse td.large-1.first,\r\n" \
    ".collapse th.large-1.first,\r\n" \
    ".collapse td.large-1.last,\r\n" \
    ".collapse th.large-1.last {\r\n" \
    "  width: 56.33333px; }\r\n" \
    "\r\n" \
    "td.large-1 center,\r\n" \
    "th.large-1 center {\r\n" \
    "  min-width: 0.33333px; }\r\n" \
    "\r\n" \
    ".body .columns td.large-1,\r\n" \
    ".body .column td.large-1,\r\n" \
    ".body .columns th.large-1,\r\n" \
    ".body .column th.large-1 {\r\n" \
    "  width: 8.33333%; }\r\n" \
    "\r\n" \
    "td.large-2,\r\n" \
    "th.large-2 {\r\n" \
    "  width: 80.66667px;\r\n" \
    "  padding-left: 8px;\r\n" \
    "  padding-right: 8px; }\r\n" \
    "\r\n" \
    "td.large-2.first,\r\n" \
    "th.large-2.first {\r\n" \
    "  padding-left: 16px; }\r\n" \
    "\r\n" \
    "td.large-2.last,\r\n" \
    "th.large-2.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    ".collapse > tbody > tr > td.large-2,\r\n" \
    ".collapse > tbody > tr > th.large-2 {\r\n" \
    "  padding-right: 0;\r\n" \
    "  padding-left: 0;\r\n" \
    "  width: 96.66667px; }\r\n" \
    "\r\n" \
    ".collapse td.large-2.first,\r\n" \
    ".collapse th.large-2.first,\r\n" \
    ".collapse td.large-2.last,\r\n" \
    ".collapse th.large-2.last {\r\n" \
    "  width: 104.66667px; }\r\n" \
    "\r\n" \
    "td.large-2 center,\r\n" \
    "th.large-2 center {\r\n" \
    "  min-width: 48.66667px; }\r\n" \
    "\r\n" \
    ".body .columns td.large-2,\r\n" \
    ".body .column td.large-2,\r\n" \
    ".body .columns th.large-2,\r\n" \
    ".body .column th.large-2 {\r\n" \
    "  width: 16.66667%; }\r\n" \
    "\r\n" \
    "td.large-3,\r\n" \
    "th.large-3 {\r\n" \
    "  width: 129px;\r\n" \
    "  padding-left: 8px;\r\n" \
    "  padding-right: 8px; }\r\n" \
    "\r\n" \
    "td.large-3.first,\r\n" \
    "th.large-3.first {\r\n" \
    "  padding-left: 16px; }\r\n" \
    "\r\n" \
    "td.large-3.last,\r\n" \
    "th.large-3.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    ".collapse > tbody > tr > td.large-3,\r\n" \
    ".collapse > tbody > tr > th.large-3 {\r\n" \
    "  padding-right: 0;\r\n" \
    "  padding-left: 0;\r\n" \
    "  width: 145px; }\r\n" \
    "\r\n" \
    ".collapse td.large-3.first,\r\n" \
    ".collapse th.large-3.first,\r\n" \
    ".collapse td.large-3.last,\r\n" \
    ".collapse th.large-3.last {\r\n" \
    "  width: 153px; }\r\n" \
    "\r\n" \
    "td.large-3 center,\r\n" \
    "th.large-3 center {\r\n" \
    "  min-width: 97px; }\r\n" \
    "\r\n" \
    ".body .columns td.large-3,\r\n" \
    ".body .column td.large-3,\r\n" \
    ".body .columns th.large-3,\r\n" \
    ".body .column th.large-3 {\r\n" \
    "  width: 25%; }\r\n" \
    "\r\n" \
    "td.large-4,\r\n" \
    "th.large-4 {\r\n" \
    "  width: 177.33333px;\r\n" \
    "  padding-left: 8px;\r\n" \
    "  padding-right: 8px; }\r\n" \
    "\r\n" \
    "td.large-4.first,\r\n" \
    "th.large-4.first {\r\n" \
    "  padding-left: 16px; }\r\n" \
    "\r\n" \
    "td.large-4.last,\r\n" \
    "th.large-4.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    ".collapse > tbody > tr > td.large-4,\r\n" \
    ".collapse > tbody > tr > th.large-4 {\r\n" \
    "  padding-right: 0;\r\n" \
    "  padding-left: 0;\r\n" \
    "  width: 193.33333px; }\r\n" \
    "\r\n" \
    ".collapse td.large-4.first,\r\n" \
    ".collapse th.large-4.first,\r\n" \
    ".collapse td.large-4.last,\r\n" \
    ".collapse th.large-4.last {\r\n" \
    "  width: 201.33333px; }\r\n" \
    "\r\n" \
    "td.large-4 center,\r\n" \
    "th.large-4 center {\r\n" \
    "  min-width: 145.33333px; }\r\n" \
    "\r\n" \
    ".body .columns td.large-4,\r\n" \
    ".body .column td.large-4,\r\n" \
    ".body .columns th.large-4,\r\n" \
    ".body .column th.large-4 {\r\n" \
    "  width: 33.33333%; }\r\n" \
    "\r\n" \
    "td.large-5,\r\n" \
    "th.large-5 {\r\n" \
    "  width: 225.66667px;\r\n" \
    "  padding-left: 8px;\r\n" \
    "  padding-right: 8px; }\r\n" \
    "\r\n" \
    "td.large-5.first,\r\n" \
    "th.large-5.first {\r\n" \
    "  padding-left: 16px; }\r\n" \
    "\r\n" \
    "td.large-5.last,\r\n" \
    "th.large-5.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    ".collapse > tbody > tr > td.large-5,\r\n" \
    ".collapse > tbody > tr > th.large-5 {\r\n" \
    "  padding-right: 0;\r\n" \
    "  padding-left: 0;\r\n" \
    "  width: 241.66667px; }\r\n" \
    "\r\n" \
    ".collapse td.large-5.first,\r\n" \
    ".collapse th.large-5.first,\r\n" \
    ".collapse td.large-5.last,\r\n" \
    ".collapse th.large-5.last {\r\n" \
    "  width: 249.66667px; }\r\n" \
    "\r\n" \
    "td.large-5 center,\r\n" \
    "th.large-5 center {\r\n" \
    "  min-width: 193.66667px; }\r\n" \
    "\r\n" \
    ".body .columns td.large-5,\r\n" \
    ".body .column td.large-5,\r\n" \
    ".body .columns th.large-5,\r\n" \
    ".body .column th.large-5 {\r\n" \
    "  width: 41.66667%; }\r\n" \
    "\r\n" \
    "td.large-6,\r\n" \
    "th.large-6 {\r\n" \
    "  width: 274px;\r\n" \
    "  padding-left: 8px;\r\n" \
    "  padding-right: 8px; }\r\n" \
    "\r\n" \
    "td.large-6.first,\r\n" \
    "th.large-6.first {\r\n" \
    "  padding-left: 16px; }\r\n" \
    "\r\n" \
    "td.large-6.last,\r\n" \
    "th.large-6.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    ".collapse > tbody > tr > td.large-6,\r\n" \
    ".collapse > tbody > tr > th.large-6 {\r\n" \
    "  padding-right: 0;\r\n" \
    "  padding-left: 0;\r\n" \
    "  width: 290px; }\r\n" \
    "\r\n" \
    ".collapse td.large-6.first,\r\n" \
    ".collapse th.large-6.first,\r\n" \
    ".collapse td.large-6.last,\r\n" \
    ".collapse th.large-6.last {\r\n" \
    "  width: 298px; }\r\n" \
    "\r\n" \
    "td.large-6 center,\r\n" \
    "th.large-6 center {\r\n" \
    "  min-width: 242px; }\r\n" \
    "\r\n" \
    ".body .columns td.large-6,\r\n" \
    ".body .column td.large-6,\r\n" \
    ".body .columns th.large-6,\r\n" \
    ".body .column th.large-6 {\r\n" \
    "  width: 50%; }\r\n" \
    "\r\n" \
    "td.large-7,\r\n" \
    "th.large-7 {\r\n" \
    "  width: 322.33333px;\r\n" \
    "  padding-left: 8px;\r\n" \
    "  padding-right: 8px; }\r\n" \
    "\r\n" \
    "td.large-7.first,\r\n" \
    "th.large-7.first {\r\n" \
    "  padding-left: 16px; }\r\n" \
    "\r\n" \
    "td.large-7.last,\r\n" \
    "th.large-7.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    ".collapse > tbody > tr > td.large-7,\r\n" \
    ".collapse > tbody > tr > th.large-7 {\r\n" \
    "  padding-right: 0;\r\n" \
    "  padding-left: 0;\r\n" \
    "  width: 338.33333px; }\r\n" \
    "\r\n" \
    ".collapse td.large-7.first,\r\n" \
    ".collapse th.large-7.first,\r\n" \
    ".collapse td.large-7.last,\r\n" \
    ".collapse th.large-7.last {\r\n" \
    "  width: 346.33333px; }\r\n" \
    "\r\n" \
    "td.large-7 center,\r\n" \
    "th.large-7 center {\r\n" \
    "  min-width: 290.33333px; }\r\n" \
    "\r\n" \
    ".body .columns td.large-7,\r\n" \
    ".body .column td.large-7,\r\n" \
    ".body .columns th.large-7,\r\n" \
    ".body .column th.large-7 {\r\n" \
    "  width: 58.33333%; }\r\n" \
    "\r\n" \
    "td.large-8,\r\n" \
    "th.large-8 {\r\n" \
    "  width: 370.66667px;\r\n" \
    "  padding-left: 8px;\r\n" \
    "  padding-right: 8px; }\r\n" \
    "\r\n" \
    "td.large-8.first,\r\n" \
    "th.large-8.first {\r\n" \
    "  padding-left: 16px; }\r\n" \
    "\r\n" \
    "td.large-8.last,\r\n" \
    "th.large-8.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    ".collapse > tbody > tr > td.large-8,\r\n" \
    ".collapse > tbody > tr > th.large-8 {\r\n" \
    "  padding-right: 0;\r\n" \
    "  padding-left: 0;\r\n" \
    "  width: 386.66667px; }\r\n" \
    "\r\n" \
    ".collapse td.large-8.first,\r\n" \
    ".collapse th.large-8.first,\r\n" \
    ".collapse td.large-8.last,\r\n" \
    ".collapse th.large-8.last {\r\n" \
    "  width: 394.66667px; }\r\n" \
    "\r\n" \
    "td.large-8 center,\r\n" \
    "th.large-8 center {\r\n" \
    "  min-width: 338.66667px; }\r\n" \
    "\r\n" \
    ".body .columns td.large-8,\r\n" \
    ".body .column td.large-8,\r\n" \
    ".body .columns th.large-8,\r\n" \
    ".body .column th.large-8 {\r\n" \
    "  width: 66.66667%; }\r\n" \
    "\r\n" \
    "td.large-9,\r\n" \
    "th.large-9 {\r\n" \
    "  width: 419px;\r\n" \
    "  padding-left: 8px;\r\n" \
    "  padding-right: 8px; }\r\n" \
    "\r\n" \
    "td.large-9.first,\r\n" \
    "th.large-9.first {\r\n" \
    "  padding-left: 16px; }\r\n" \
    "\r\n" \
    "td.large-9.last,\r\n" \
    "th.large-9.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    ".collapse > tbody > tr > td.large-9,\r\n" \
    ".collapse > tbody > tr > th.large-9 {\r\n" \
    "  padding-right: 0;\r\n" \
    "  padding-left: 0;\r\n" \
    "  width: 435px; }\r\n" \
    "\r\n" \
    ".collapse td.large-9.first,\r\n" \
    ".collapse th.large-9.first,\r\n" \
    ".collapse td.large-9.last,\r\n" \
    ".collapse th.large-9.last {\r\n" \
    "  width: 443px; }\r\n" \
    "\r\n" \
    "td.large-9 center,\r\n" \
    "th.large-9 center {\r\n" \
    "  min-width: 387px; }\r\n" \
    "\r\n" \
    ".body .columns td.large-9,\r\n" \
    ".body .column td.large-9,\r\n" \
    ".body .columns th.large-9,\r\n" \
    ".body .column th.large-9 {\r\n" \
    "  width: 75%; }\r\n" \
    "\r\n" \
    "td.large-10,\r\n" \
    "th.large-10 {\r\n" \
    "  width: 467.33333px;\r\n" \
    "  padding-left: 8px;\r\n" \
    "  padding-right: 8px; }\r\n" \
    "\r\n" \
    "td.large-10.first,\r\n" \
    "th.large-10.first {\r\n" \
    "  padding-left: 16px; }\r\n" \
    "\r\n" \
    "td.large-10.last,\r\n" \
    "th.large-10.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    ".collapse > tbody > tr > td.large-10,\r\n" \
    ".collapse > tbody > tr > th.large-10 {\r\n" \
    "  padding-right: 0;\r\n" \
    "  padding-left: 0;\r\n" \
    "  width: 483.33333px; }\r\n" \
    "\r\n" \
    ".collapse td.large-10.first,\r\n" \
    ".collapse th.large-10.first,\r\n" \
    ".collapse td.large-10.last,\r\n" \
    ".collapse th.large-10.last {\r\n" \
    "  width: 491.33333px; }\r\n" \
    "\r\n" \
    "td.large-10 center,\r\n" \
    "th.large-10 center {\r\n" \
    "  min-width: 435.33333px; }\r\n" \
    "\r\n" \
    ".body .columns td.large-10,\r\n" \
    ".body .column td.large-10,\r\n" \
    ".body .columns th.large-10,\r\n" \
    ".body .column th.large-10 {\r\n" \
    "  width: 83.33333%; }\r\n" \
    "\r\n" \
    "td.large-11,\r\n" \
    "th.large-11 {\r\n" \
    "  width: 515.66667px;\r\n" \
    "  padding-left: 8px;\r\n" \
    "  padding-right: 8px; }\r\n" \
    "\r\n" \
    "td.large-11.first,\r\n" \
    "th.large-11.first {\r\n" \
    "  padding-left: 16px; }\r\n" \
    "\r\n" \
    "td.large-11.last,\r\n" \
    "th.large-11.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    ".collapse > tbody > tr > td.large-11,\r\n" \
    ".collapse > tbody > tr > th.large-11 {\r\n" \
    "  padding-right: 0;\r\n" \
    "  padding-left: 0;\r\n" \
    "  width: 531.66667px; }\r\n" \
    "\r\n" \
    ".collapse td.large-11.first,\r\n" \
    ".collapse th.large-11.first,\r\n" \
    ".collapse td.large-11.last,\r\n" \
    ".collapse th.large-11.last {\r\n" \
    "  width: 539.66667px; }\r\n" \
    "\r\n" \
    "td.large-11 center,\r\n" \
    "th.large-11 center {\r\n" \
    "  min-width: 483.66667px; }\r\n" \
    "\r\n" \
    ".body .columns td.large-11,\r\n" \
    ".body .column td.large-11,\r\n" \
    ".body .columns th.large-11,\r\n" \
    ".body .column th.large-11 {\r\n" \
    "  width: 91.66667%; }\r\n" \
    "\r\n" \
    "td.large-12,\r\n" \
    "th.large-12 {\r\n" \
    "  width: 564px;\r\n" \
    "  padding-left: 8px;\r\n" \
    "  padding-right: 8px; }\r\n" \
    "\r\n" \
    "td.large-12.first,\r\n" \
    "th.large-12.first {\r\n" \
    "  padding-left: 16px; }\r\n" \
    "\r\n" \
    "td.large-12.last,\r\n" \
    "th.large-12.last {\r\n" \
    "  padding-right: 16px; }\r\n" \
    "\r\n" \
    ".collapse > tbody > tr > td.large-12,\r\n" \
    ".collapse > tbody > tr > th.large-12 {\r\n" \
    "  padding-right: 0;\r\n" \
    "  padding-left: 0;\r\n" \
    "  width: 580px; }\r\n" \
    "\r\n" \
    ".collapse td.large-12.first,\r\n" \
    ".collapse th.large-12.first,\r\n" \
    ".collapse td.large-12.last,\r\n" \
    ".collapse th.large-12.last {\r\n" \
    "  width: 588px; }\r\n" \
    "\r\n" \
    "td.large-12 center,\r\n" \
    "th.large-12 center {\r\n" \
    "  min-width: 532px; }\r\n" \
    "\r\n" \
    ".body .columns td.large-12,\r\n" \
    ".body .column td.large-12,\r\n" \
    ".body .columns th.large-12,\r\n" \
    ".body .column th.large-12 {\r\n" \
    "  width: 100%; }\r\n" \
    "\r\n" \
    "td.large-offset-1,\r\n" \
    "td.large-offset-1.first,\r\n" \
    "td.large-offset-1.last,\r\n" \
    "th.large-offset-1,\r\n" \
    "th.large-offset-1.first,\r\n" \
    "th.large-offset-1.last {\r\n" \
    "  padding-left: 64.33333px; }\r\n" \
    "\r\n" \
    "td.large-offset-2,\r\n" \
    "td.large-offset-2.first,\r\n" \
    "td.large-offset-2.last,\r\n" \
    "th.large-offset-2,\r\n" \
    "th.large-offset-2.first,\r\n" \
    "th.large-offset-2.last {\r\n" \
    "  padding-left: 112.66667px; }\r\n" \
    "\r\n" \
    "td.large-offset-3,\r\n" \
    "td.large-offset-3.first,\r\n" \
    "td.large-offset-3.last,\r\n" \
    "th.large-offset-3,\r\n" \
    "th.large-offset-3.first,\r\n" \
    "th.large-offset-3.last {\r\n" \
    "  padding-left: 161px; }\r\n" \
    "\r\n" \
    "td.large-offset-4,\r\n" \
    "td.large-offset-4.first,\r\n" \
    "td.large-offset-4.last,\r\n" \
    "th.large-offset-4,\r\n" \
    "th.large-offset-4.first,\r\n" \
    "th.large-offset-4.last {\r\n" \
    "  padding-left: 209.33333px; }\r\n" \
    "\r\n" \
    "td.large-offset-5,\r\n" \
    "td.large-offset-5.first,\r\n" \
    "td.large-offset-5.last,\r\n" \
    "th.large-offset-5,\r\n" \
    "th.large-offset-5.first,\r\n" \
    "th.large-offset-5.last {\r\n" \
    "  padding-left: 257.66667px; }\r\n" \
    "\r\n" \
    "td.large-offset-6,\r\n" \
    "td.large-offset-6.first,\r\n" \
    "td.large-offset-6.last,\r\n" \
    "th.large-offset-6,\r\n" \
    "th.large-offset-6.first,\r\n" \
    "th.large-offset-6.last {\r\n" \
    "  padding-left: 306px; }\r\n" \
    "\r\n" \
    "td.large-offset-7,\r\n" \
    "td.large-offset-7.first,\r\n" \
    "td.large-offset-7.last,\r\n" \
    "th.large-offset-7,\r\n" \
    "th.large-offset-7.first,\r\n" \
    "th.large-offset-7.last {\r\n" \
    "  padding-left: 354.33333px; }\r\n" \
    "\r\n" \
    "td.large-offset-8,\r\n" \
    "td.large-offset-8.first,\r\n" \
    "td.large-offset-8.last,\r\n" \
    "th.large-offset-8,\r\n" \
    "th.large-offset-8.first,\r\n" \
    "th.large-offset-8.last {\r\n" \
    "  padding-left: 402.66667px; }\r\n" \
    "\r\n" \
    "td.large-offset-9,\r\n" \
    "td.large-offset-9.first,\r\n" \
    "td.large-offset-9.last,\r\n" \
    "th.large-offset-9,\r\n" \
    "th.large-offset-9.first,\r\n" \
    "th.large-offset-9.last {\r\n" \
    "  padding-left: 451px; }\r\n" \
    "\r\n" \
    "td.large-offset-10,\r\n" \
    "td.large-offset-10.first,\r\n" \
    "td.large-offset-10.last,\r\n" \
    "th.large-offset-10,\r\n" \
    "th.large-offset-10.first,\r\n" \
    "th.large-offset-10.last {\r\n" \
    "  padding-left: 499.33333px; }\r\n" \
    "\r\n" \
    "td.large-offset-11,\r\n" \
    "td.large-offset-11.first,\r\n" \
    "td.large-offset-11.last,\r\n" \
    "th.large-offset-11,\r\n" \
    "th.large-offset-11.first,\r\n" \
    "th.large-offset-11.last {\r\n" \
    "  padding-left: 547.66667px; }\r\n" \
    "\r\n" \
    "td.expander,\r\n" \
    "th.expander {\r\n" \
    "  visibility: hidden;\r\n" \
    "  width: 0;\r\n" \
    "  padding: 0 !important; }\r\n" \
    "\r\n" \
    "table.container.radius {\r\n" \
    "  border-radius: 0;\r\n" \
    "  border-collapse: separate; }\r\n" \
    "\r\n" \
    ".block-grid {\r\n" \
    "  width: 100%;\r\n" \
    "  max-width: 580px; }\r\n" \
    "  .block-grid td {\r\n" \
    "    display: inline-block;\r\n" \
    "    padding: 8px; }\r\n" \
    "\r\n" \
    ".up-2 td {\r\n" \
    "  width: 274px !important; }\r\n" \
    "\r\n" \
    ".up-3 td {\r\n" \
    "  width: 177px !important; }\r\n" \
    "\r\n" \
    ".up-4 td {\r\n" \
    "  width: 129px !important; }\r\n" \
    "\r\n" \
    ".up-5 td {\r\n" \
    "  width: 100px !important; }\r\n" \
    "\r\n" \
    ".up-6 td {\r\n" \
    "  width: 80px !important; }\r\n" \
    "\r\n" \
    ".up-7 td {\r\n" \
    "  width: 66px !important; }\r\n" \
    "\r\n" \
    ".up-8 td {\r\n" \
    "  width: 56px !important; }\r\n" \
    "\r\n" \
    "table.text-center,\r\n" \
    "th.text-center,\r\n" \
    "td.text-center,\r\n" \
    "h1.text-center,\r\n" \
    "h2.text-center,\r\n" \
    "h3.text-center,\r\n" \
    "h4.text-center,\r\n" \
    "h5.text-center,\r\n" \
    "h6.text-center,\r\n" \
    "p.text-center,\r\n" \
    "span.text-center {\r\n" \
    "  text-align: center; }\r\n" \
    "\r\n" \
    "table.text-left,\r\n" \
    "th.text-left,\r\n" \
    "td.text-left,\r\n" \
    "h1.text-left,\r\n" \
    "h2.text-left,\r\n" \
    "h3.text-left,\r\n" \
    "h4.text-left,\r\n" \
    "h5.text-left,\r\n" \
    "h6.text-left,\r\n" \
    "p.text-left,\r\n" \
    "span.text-left {\r\n" \
    "  text-align: left; }\r\n" \
    "\r\n" \
    "table.text-right,\r\n" \
    "th.text-right,\r\n" \
    "td.text-right,\r\n" \
    "h1.text-right,\r\n" \
    "h2.text-right,\r\n" \
    "h3.text-right,\r\n" \
    "h4.text-right,\r\n" \
    "h5.text-right,\r\n" \
    "h6.text-right,\r\n" \
    "p.text-right,\r\n" \
    "span.text-right {\r\n" \
    "  text-align: right; }\r\n" \
    "\r\n" \
    "span.text-center {\r\n" \
    "  display: block;\r\n" \
    "  width: 100%;\r\n" \
    "  text-align: center; }\r\n" \
    "\r\n" \
    "@media only screen and (max-width: 596px) {\r\n" \
    "  .small-float-center {\r\n" \
    "    margin: 0 auto !important;\r\n" \
    "    float: none !important;\r\n" \
    "    text-align: center !important; }\r\n" \
    "  .small-text-center {\r\n" \
    "    text-align: center !important; }\r\n" \
    "  .small-text-left {\r\n" \
    "    text-align: left !important; }\r\n" \
    "  .small-text-right {\r\n" \
    "    text-align: right !important; } }\r\n" \
    "\r\n" \
    "img.float-left {\r\n" \
    "  float: left;\r\n" \
    "  text-align: left; }\r\n" \
    "\r\n" \
    "img.float-right {\r\n" \
    "  float: right;\r\n" \
    "  text-align: right; }\r\n" \
    "\r\n" \
    "img.float-center,\r\n" \
    "img.text-center {\r\n" \
    "  margin: 0 auto;\r\n" \
    "  Margin: 0 auto;\r\n" \
    "  float: none;\r\n" \
    "  text-align: center; }\r\n" \
    "\r\n" \
    "table.float-center,\r\n" \
    "td.float-center,\r\n" \
    "th.float-center {\r\n" \
    "  margin: 0 auto;\r\n" \
    "  Margin: 0 auto;\r\n" \
    "  float: none;\r\n" \
    "  text-align: center; \r\n" \
    "}\r\n" \
    "\r\n" \
    ".hide-for-large {\r\n" \
    "  display: none !important;\r\n" \
    "  mso-hide: all;\r\n" \
    "  overflow: hidden;\r\n" \
    "  max-height: 0;\r\n" \
    "  font-size: 0;\r\n" \
    "  width: 0;\r\n" \
    "  line-height: 0; }\r\n" \
    "  @media only screen and (max-width: 596px) {\r\n" \
    "    .hide-for-large {\r\n" \
    "      display: block !important;\r\n" \
    "      width: auto !important;\r\n" \
    "      overflow: visible !important;\r\n" \
    "      max-height: none !important;\r\n" \
    "      font-size: inherit !important;\r\n" \
    "      line-height: inherit !important; } }\r\n" \
    "\r\n" \
    "table.body table.container .hide-for-large * {\r\n" \
    "  mso-hide: all; }\r\n" \
    "\r\n" \
    "@media only screen and (max-width: 596px) {\r\n" \
    "  table.body table.container .hide-for-large,\r\n" \
    "  table.body table.container .row.hide-for-large {\r\n" \
    "    display: table !important;\r\n" \
    "    width: 100% !important; } }\r\n" \
    "\r\n" \
    "@media only screen and (max-width: 596px) {\r\n" \
    "  table.body table.container .callout-inner.hide-for-large {\r\n" \
    "    display: table-cell !important;\r\n" \
    "    width: 100% !important; } }\r\n" \
    "\r\n" \
    "@media only screen and (max-width: 596px) {\r\n" \
    "  table.body table.container .show-for-large {\r\n" \
    "    display: none !important;\r\n" \
    "    width: 0;\r\n" \
    "    mso-hide: all;\r\n" \
    "    overflow: hidden; } }\r\n" \
    "\r\n" \
    "body,\r\n" \
    "table.body,\r\n" \
    "h1,\r\n" \
    "h2,\r\n" \
    "h3,\r\n" \
    "h4,\r\n" \
    "h5,\r\n" \
    "h6,\r\n" \
    "p,\r\n" \
    "td,\r\n" \
    "th,\r\n" \
    "a {\r\n" \
    "  color: #0a0a0a;\r\n" \
    "  font-family: Helvetica, Arial, sans-serif;\r\n" \
    "  font-weight: normal;\r\n" \
    "  padding: 0;\r\n" \
    "  margin: 0;\r\n" \
    "  Margin: 0;\r\n" \
    "  text-align: left;\r\n" \
    "  line-height: 1.3; }\r\n" \
    "\r\n" \
    "h1,\r\n" \
    "h2,\r\n" \
    "h3,\r\n" \
    "h4,\r\n" \
    "h5,\r\n" \
    "h6 {\r\n" \
    "  color: inherit;\r\n" \
    "  word-wrap: normal;\r\n" \
    "  font-family: Helvetica, Arial, sans-serif;\r\n" \
    "  font-weight: normal;\r\n" \
    "  margin-bottom: 10px;\r\n" \
    "  Margin-bottom: 10px; }\r\n" \
    "\r\n" \
    "h1 {\r\n" \
    "  font-size: 34px; }\r\n" \
    "\r\n" \
    "h2 {\r\n" \
    "  font-size: 30px; }\r\n" \
    "\r\n" \
    "h3 {\r\n" \
    "  font-size: 28px; }\r\n" \
    "\r\n" \
    "h4 {\r\n" \
    "  font-size: 24px; }\r\n" \
    "\r\n" \
    "h5 {\r\n" \
    "  font-size: 20px; }\r\n" \
    "\r\n" \
    "h6 {\r\n" \
    "  font-size: 18px; }\r\n" \
    "\r\n" \
    "body,\r\n" \
    "table.body,\r\n" \
    "p,\r\n" \
    "td,\r\n" \
    "th {\r\n" \
    "  font-size: 16px;\r\n" \
    "  line-height: 1.3; }\r\n" \
    "\r\n" \
    "p {\r\n" \
    "  margin-bottom: 10px;\r\n" \
    "  Margin-bottom: 10px; }\r\n" \
    "  p.lead {\r\n" \
    "    font-size: 20px;\r\n" \
    "    line-height: 1.6; }\r\n" \
    "  p.subheader {\r\n" \
    "    margin-top: 4px;\r\n" \
    "    margin-bottom: 8px;\r\n" \
    "    Margin-top: 4px;\r\n" \
    "    Margin-bottom: 8px;\r\n" \
    "    font-weight: normal;\r\n" \
    "    line-height: 1.4;\r\n" \
    "    color: #8a8a8a; }\r\n" \
    "\r\n" \
    "small {\r\n" \
    "  font-size: 80%;\r\n" \
    "  color: #cacaca; }\r\n" \
    "\r\n" \
    "a {\r\n" \
    "  color: #2199e8;\r\n" \
    "  text-decoration: none; }\r\n" \
    "  a:hover {\r\n" \
    "    color: #147dc2; }\r\n" \
    "  a:active {\r\n" \
    "    color: #147dc2; }\r\n" \
    "  a:visited {\r\n" \
    "    color: #2199e8; }\r\n" \
    "\r\n" \
    "h1 a,\r\n" \
    "h1 a:visited,\r\n" \
    "h2 a,\r\n" \
    "h2 a:visited,\r\n" \
    "h3 a,\r\n" \
    "h3 a:visited,\r\n" \
    "h4 a,\r\n" \
    "h4 a:visited,\r\n" \
    "h5 a,\r\n" \
    "h5 a:visited,\r\n" \
    "h6 a,\r\n" \
    "h6 a:visited {\r\n" \
    "  color: #2199e8; }\r\n" \
    "\r\n" \
    "pre {\r\n" \
    "  background: #f3f3f3;\r\n" \
    "  margin: 30px 0;\r\n" \
    "  Margin: 30px 0; }\r\n" \
    "  pre code {\r\n" \
    "    color: #cacaca; }\r\n" \
    "    pre code span.callout {\r\n" \
    "      color: #8a8a8a;\r\n" \
    "      font-weight: bold; }\r\n" \
    "    pre code span.callout-strong {\r\n" \
    "      color: #ff6908;\r\n" \
    "      font-weight: bold; }\r\n" \
    "\r\n" \
    "table.hr {\r\n" \
    "  width: 100%; }\r\n" \
    "  table.hr th {\r\n" \
    "    height: 0;\r\n" \
    "    max-width: 580px;\r\n" \
    "    border-top: 0;\r\n" \
    "    border-right: 0;\r\n" \
    "    border-bottom: 1px solid #0a0a0a;\r\n" \
    "    border-left: 0;\r\n" \
    "    margin: 20px auto;\r\n" \
    "    Margin: 20px auto;\r\n" \
    "    clear: both; }\r\n" \
    "\r\n" \
    ".stat {\r\n" \
    "  font-size: 40px;\r\n" \
    "  line-height: 1; }\r\n" \
    "  p \ .stat {\r\n" \
    "    margin-top: -16px;\r\n" \
    "    Margin-top: -16px; }\r\n" \
    "\r\n" \
    "span.preheader {\r\n" \
    "  display: none !important;\r\n" \
    "  visibility: hidden;\r\n" \
    "  mso-hide: all !important;\r\n" \
    "  font-size: 1px;\r\n" \
    "  color: #f3f3f3;\r\n" \
    "  line-height: 1px;\r\n" \
    "  max-height: 0px;\r\n" \
    "  max-width: 0px;\r\n" \
    "  opacity: 0;\r\n" \
    "  overflow: hidden; }\r\n" \
    "\r\n" \
    "table.button {\r\n" \
    "  width: auto;\r\n" \
    "  margin: 0 0 16px 0;\r\n" \
    "  Margin: 0 0 16px 0; }\r\n" \
    "  table.button table td {\r\n" \
    "    text-align: left;\r\n" \
    "    color: #fefefe;\r\n" \
    "    background: #2199e8;\r\n" \
    "    border: 2px solid #2199e8; }\r\n" \
    "    table.button table td a {\r\n" \
    "      font-family: Helvetica, Arial, sans-serif;\r\n" \
    "      font-size: 16px;\r\n" \
    "      font-weight: bold;\r\n" \
    "      color: #fefefe;\r\n" \
    "      text-decoration: none;\r\n" \
    "      display: inline-block;\r\n" \
    "      padding: 8px 16px 8px 16px;\r\n" \
    "      border: 0 solid #2199e8;\r\n" \
    "      border-radius: 3px; }\r\n" \
    "  table.button.radius table td {\r\n" \
    "    border-radius: 3px;\r\n" \
    "    border: none; }\r\n" \
    "  table.button.rounded table td {\r\n" \
    "    border-radius: 500px;\r\n" \
    "    border: none; }\r\n" \
    "\r\n" \
    "table.button:hover table tr td a,\r\n" \
    "table.button:active table tr td a,\r\n" \
    "table.button table tr td a:visited,\r\n" \
    "table.button.tiny:hover table tr td a,\r\n" \
    "table.button.tiny:active table tr td a,\r\n" \
    "table.button.tiny table tr td a:visited,\r\n" \
    "table.button.small:hover table tr td a,\r\n" \
    "table.button.small:active table tr td a,\r\n" \
    "table.button.small table tr td a:visited,\r\n" \
    "table.button.large:hover table tr td a,\r\n" \
    "table.button.large:active table tr td a,\r\n" \
    "table.button.large table tr td a:visited {\r\n" \
    "  color: #fefefe; }\r\n" \
    "\r\n" \
    "table.button.tiny table td,\r\n" \
    "table.button.tiny table a {\r\n" \
    "  padding: 4px 8px 4px 8px; }\r\n" \
    "\r\n" \
    "table.button.tiny table a {\r\n" \
    "  font-size: 10px;\r\n" \
    "  font-weight: normal; }\r\n" \
    "\r\n" \
    "table.button.small table td,\r\n" \
    "table.button.small table a {\r\n" \
    "  padding: 5px 10px 5px 10px;\r\n" \
    "  font-size: 12px; }\r\n" \
    "\r\n" \
    "table.button.large table a {\r\n" \
    "  padding: 10px 20px 10px 20px;\r\n" \
    "  font-size: 20px; }\r\n" \
    "\r\n" \
    "table.button.expand,\r\n" \
    "table.button.expanded {\r\n" \
    "  width: 100% !important; }\r\n" \
    "  table.button.expand table,\r\n" \
    "  table.button.expanded table {\r\n" \
    "    width: 100%; }\r\n" \
    "    table.button.expand table a,\r\n" \
    "    table.button.expanded table a {\r\n" \
    "      text-align: center;\r\n" \
    "      width: 100%;\r\n" \
    "      padding-left: 0;\r\n" \
    "      padding-right: 0; }\r\n" \
    "  table.button.expand center,\r\n" \
    "  table.button.expanded center {\r\n" \
    "    min-width: 0; }\r\n" \
    "\r\n" \
    "table.button:hover table td,\r\n" \
    "table.button:visited table td,\r\n" \
    "table.button:active table td {\r\n" \
    "  background: #147dc2;\r\n" \
    "  color: #fefefe; }\r\n" \
    "\r\n" \
    "table.button:hover table a,\r\n" \
    "table.button:visited table a,\r\n" \
    "table.button:active table a {\r\n" \
    "  border: 0 solid #147dc2; }\r\n" \
    "\r\n" \
    "table.button.secondary table td {\r\n" \
    "  background: #777777;\r\n" \
    "  color: #fefefe;\r\n" \
    "  border: 0px solid #777777; }\r\n" \
    "\r\n" \
    "table.button.secondary table a {\r\n" \
    "  color: #fefefe;\r\n" \
    "  border: 0 solid #777777; }\r\n" \
    "\r\n" \
    "table.button.secondary:hover table td {\r\n" \
    "  background: #919191;\r\n" \
    "  color: #fefefe; }\r\n" \
    "\r\n" \
    "table.button.secondary:hover table a {\r\n" \
    "  border: 0 solid #919191; }\r\n" \
    "\r\n" \
    "table.button.secondary:hover table td a {\r\n" \
    "  color: #fefefe; }\r\n" \
    "\r\n" \
    "table.button.secondary:active table td a {\r\n" \
    "  color: #fefefe; }\r\n" \
    "\r\n" \
    "table.button.secondary table td a:visited {\r\n" \
    "  color: #fefefe; }\r\n" \
    "\r\n" \
    "table.button.success table td {\r\n" \
    "  background: #3adb76;\r\n" \
    "  border: 0px solid #3adb76; }\r\n" \
    "\r\n" \
    "table.button.success table a {\r\n" \
    "  border: 0 solid #3adb76; }\r\n" \
    "\r\n" \
    "table.button.success:hover table td {\r\n" \
    "  background: #23bf5d; }\r\n" \
    "\r\n" \
    "table.button.success:hover table a {\r\n" \
    "  border: 0 solid #23bf5d; }\r\n" \
    "\r\n" \
    "table.button.alert table td {\r\n" \
    "  background: #ec5840;\r\n" \
    "  border: 0px solid #ec5840; }\r\n" \
    "\r\n" \
    "table.button.alert table a {\r\n" \
    "  border: 0 solid #ec5840; }\r\n" \
    "\r\n" \
    "table.button.alert:hover table td {\r\n" \
    "  background: #e23317; }\r\n" \
    "\r\n" \
    "table.button.alert:hover table a {\r\n" \
    "  border: 0 solid #e23317; }\r\n" \
    "\r\n" \
    "table.button.warning table td {\r\n" \
    "  background: #ffae00;\r\n" \
    "  border: 0px solid #ffae00; }\r\n" \
    "\r\n" \
    "table.button.warning table a {\r\n" \
    "  border: 0px solid #ffae00; }\r\n" \
    "\r\n" \
    "table.button.warning:hover table td {\r\n" \
    "  background: #cc8b00; }\r\n" \
    "\r\n" \
    "table.button.warning:hover table a {\r\n" \
    "  border: 0px solid #cc8b00; }\r\n" \
    "\r\n" \
    "table.callout {\r\n" \
    "  margin-bottom: 16px;\r\n" \
    "  Margin-bottom: 16px; }\r\n" \
    "\r\n" \
    "th.callout-inner {\r\n" \
    "  width: 100%;\r\n" \
    "  border: 1px solid #cbcbcb;\r\n" \
    "  padding: 10px;\r\n" \
    "  background: #fefefe; }\r\n" \
    "  th.callout-inner.primary {\r\n" \
    "    background: #def0fc;\r\n" \
    "    border: 1px solid #444444;\r\n" \
    "    color: #0a0a0a; }\r\n" \
    "  th.callout-inner.secondary {\r\n" \
    "    background: #ebebeb;\r\n" \
    "    border: 1px solid #444444;\r\n" \
    "    color: #0a0a0a; }\r\n" \
    "  th.callout-inner.success {\r\n" \
    "    background: #e1faea;\r\n" \
    "    border: 1px solid #1b9448;\r\n" \
    "    color: #fefefe; }\r\n" \
    "  th.callout-inner.warning {\r\n" \
    "    background: #fff3d9;\r\n" \
    "    border: 1px solid #996800;\r\n" \
    "    color: #fefefe; }\r\n" \
    "  th.callout-inner.alert {\r\n" \
    "    background: #fce6e2;\r\n" \
    "    border: 1px solid #b42912;\r\n" \
    "    color: #fefefe; }\r\n" \
    "\r\n" \
    ".thumbnail {\r\n" \
    "  border: solid 4px #fefefe;\r\n" \
    "  box-shadow: 0 0 0 1px rgba(10, 10, 10, 0.2);\r\n" \
    "  display: inline-block;\r\n" \
    "  line-height: 0;\r\n" \
    "  max-width: 100%;\r\n" \
    "  transition: box-shadow 200ms ease-out;\r\n" \
    "  border-radius: 3px;\r\n" \
    "  margin-bottom: 16px; }\r\n" \
    "  .thumbnail:hover, .thumbnail:focus {\r\n" \
    "    box-shadow: 0 0 6px 1px rgba(33, 153, 232, 0.5); }\r\n" \
    "\r\n" \
    "table.menu {\r\n" \
    "  width: 580px; }\r\n" \
    "  table.menu td.menu-item,\r\n" \
    "  table.menu th.menu-item {\r\n" \
    "    padding: 10px;\r\n" \
    "    padding-right: 10px; }\r\n" \
    "    table.menu td.menu-item a,\r\n" \
    "    table.menu th.menu-item a {\r\n" \
    "      color: #2199e8; }\r\n" \
    "\r\n" \
    "table.menu.vertical td.menu-item,\r\n" \
    "table.menu.vertical th.menu-item {\r\n" \
    "  padding: 10px;\r\n" \
    "  padding-right: 0;\r\n" \
    "  display: block; }\r\n" \
    "  table.menu.vertical td.menu-item a,\r\n" \
    "  table.menu.vertical th.menu-item a {\r\n" \
    "    width: 100%; }\r\n" \
    "\r\n" \
    "table.menu.vertical td.menu-item table.menu.vertical td.menu-item,\r\n" \
    "table.menu.vertical td.menu-item table.menu.vertical th.menu-item,\r\n" \
    "table.menu.vertical th.menu-item table.menu.vertical td.menu-item,\r\n" \
    "table.menu.vertical th.menu-item table.menu.vertical th.menu-item {\r\n" \
    "  padding-left: 10px; }\r\n" \
    "\r\n" \
    "table.menu.text-center a {\r\n" \
    "  text-align: center; }\r\n" \
    "\r\n" \
    ".menu[align=\"center\"] {\r\n" \
    "  width: auto !important; }\r\n" \
    "\r\n" \
    "body.outlook p {\r\n" \
    "  display: inline !important; }\r\n" \
    "\r\n" \
    "@media only screen and (max-width: 596px) {\r\n" \
    "  table.body img {\r\n" \
    "    width: auto;\r\n" \
    "    height: auto; }\r\n" \
    "  table.body center {\r\n" \
    "    min-width: 0 !important; }\r\n" \
    "  table.body .container {\r\n" \
    "    width: 95% !important; }\r\n" \
    "  table.body .columns,\r\n" \
    "  table.body .column {\r\n" \
    "    height: auto !important;\r\n" \
    "    -moz-box-sizing: border-box;\r\n" \
    "    -webkit-box-sizing: border-box;\r\n" \
    "    box-sizing: border-box;\r\n" \
    "    padding-left: 16px !important;\r\n" \
    "    padding-right: 16px !important; }\r\n" \
    "    table.body .columns .column,\r\n" \
    "    table.body .columns .columns,\r\n" \
    "    table.body .column .column,\r\n" \
    "    table.body .column .columns {\r\n" \
    "      padding-left: 0 !important;\r\n" \
    "      padding-right: 0 !important; }\r\n" \
    "  table.body .collapse .columns,\r\n" \
    "  table.body .collapse .column {\r\n" \
    "    padding-left: 0 !important;\r\n" \
    "    padding-right: 0 !important; }\r\n" \
    "  td.small-1,\r\n" \
    "  th.small-1 {\r\n" \
    "    display: inline-block !important;\r\n" \
    "    width: 8.33333% !important; }\r\n" \
    "  td.small-2,\r\n" \
    "  th.small-2 {\r\n" \
    "    display: inline-block !important;\r\n" \
    "    width: 16.66667% !important; }\r\n" \
    "  td.small-3,\r\n" \
    "  th.small-3 {\r\n" \
    "    display: inline-block !important;\r\n" \
    "    width: 25% !important; }\r\n" \
    "  td.small-4,\r\n" \
    "  th.small-4 {\r\n" \
    "    display: inline-block !important;\r\n" \
    "    width: 33.33333% !important; }\r\n" \
    "  td.small-5,\r\n" \
    "  th.small-5 {\r\n" \
    "    display: inline-block !important;\r\n" \
    "    width: 41.66667% !important; }\r\n" \
    "  td.small-6,\r\n" \
    "  th.small-6 {\r\n" \
    "    display: inline-block !important;\r\n" \
    "    width: 50% !important; }\r\n" \
    "  td.small-7,\r\n" \
    "  th.small-7 {\r\n" \
    "    display: inline-block !important;\r\n" \
    "    width: 58.33333% !important; }\r\n" \
    "  td.small-8,\r\n" \
    "  th.small-8 {\r\n" \
    "    display: inline-block !important;\r\n" \
    "    width: 66.66667% !important; }\r\n" \
    "  td.small-9,\r\n" \
    "  th.small-9 {\r\n" \
    "    display: inline-block !important;\r\n" \
    "    width: 75% !important; }\r\n" \
    "  td.small-10,\r\n" \
    "  th.small-10 {\r\n" \
    "    display: inline-block !important;\r\n" \
    "    width: 83.33333% !important; }\r\n" \
    "  td.small-11,\r\n" \
    "  th.small-11 {\r\n" \
    "    display: inline-block !important;\r\n" \
    "    width: 91.66667% !important; }\r\n" \
    "  td.small-12,\r\n" \
    "  th.small-12 {\r\n" \
    "    display: inline-block !important;\r\n" \
    "    width: 100% !important; }\r\n" \
    "  .columns td.small-12,\r\n" \
    "  .column td.small-12,\r\n" \
    "  .columns th.small-12,\r\n" \
    "  .column th.small-12 {\r\n" \
    "    display: block !important;\r\n" \
    "    width: 100% !important; }\r\n" \
    "  table.body td.small-offset-1,\r\n" \
    "  table.body th.small-offset-1 {\r\n" \
    "    margin-left: 8.33333% !important;\r\n" \
    "    Margin-left: 8.33333% !important; }\r\n" \
    "  table.body td.small-offset-2,\r\n" \
    "  table.body th.small-offset-2 {\r\n" \
    "    margin-left: 16.66667% !important;\r\n" \
    "    Margin-left: 16.66667% !important; }\r\n" \
    "  table.body td.small-offset-3,\r\n" \
    "  table.body th.small-offset-3 {\r\n" \
    "    margin-left: 25% !important;\r\n" \
    "    Margin-left: 25% !important; }\r\n" \
    "  table.body td.small-offset-4,\r\n" \
    "  table.body th.small-offset-4 {\r\n" \
    "    margin-left: 33.33333% !important;\r\n" \
    "    Margin-left: 33.33333% !important; }\r\n" \
    "  table.body td.small-offset-5,\r\n" \
    "  table.body th.small-offset-5 {\r\n" \
    "    margin-left: 41.66667% !important;\r\n" \
    "    Margin-left: 41.66667% !important; }\r\n" \
    "  table.body td.small-offset-6,\r\n" \
    "  table.body th.small-offset-6 {\r\n" \
    "    margin-left: 50% !important;\r\n" \
    "    Margin-left: 50% !important; }\r\n" \
    "  table.body td.small-offset-7,\r\n" \
    "  table.body th.small-offset-7 {\r\n" \
    "    margin-left: 58.33333% !important;\r\n" \
    "    Margin-left: 58.33333% !important; }\r\n" \
    "  table.body td.small-offset-8,\r\n" \
    "  table.body th.small-offset-8 {\r\n" \
    "    margin-left: 66.66667% !important;\r\n" \
    "    Margin-left: 66.66667% !important; }\r\n" \
    "  table.body td.small-offset-9,\r\n" \
    "  table.body th.small-offset-9 {\r\n" \
    "    margin-left: 75% !important;\r\n" \
    "    Margin-left: 75% !important; }\r\n" \
    "  table.body td.small-offset-10,\r\n" \
    "  table.body th.small-offset-10 {\r\n" \
    "    margin-left: 83.33333% !important;\r\n" \
    "    Margin-left: 83.33333% !important; }\r\n" \
    "  table.body td.small-offset-11,\r\n" \
    "  table.body th.small-offset-11 {\r\n" \
    "    margin-left: 91.66667% !important;\r\n" \
    "    Margin-left: 91.66667% !important; }\r\n" \
    "  table.body table.columns td.expander,\r\n" \
    "  table.body table.columns th.expander {\r\n" \
    "    display: none !important; }\r\n" \
    "  table.body .right-text-pad,\r\n" \
    "  table.body .text-pad-right {\r\n" \
    "    padding-left: 10px !important; }\r\n" \
    "  table.body .left-text-pad,\r\n" \
    "  table.body .text-pad-left {\r\n" \
    "    padding-right: 10px !important; }\r\n" \
    "  table.menu {\r\n" \
    "    width: 100% !important; }\r\n" \
    "    table.menu td,\r\n" \
    "    table.menu th {\r\n" \
    "      width: auto !important;\r\n" \
    "      display: inline-block !important; }\r\n" \
    "    table.menu.vertical td,\r\n" \
    "    table.menu.vertical th, table.menu.small-vertical td,\r\n" \
    "    table.menu.small-vertical th {\r\n" \
    "      display: block !important; }\r\n" \
    "  table.menu[align=\"center\"] {\r\n" \
    "    width: auto !important; }\r\n" \
    "  table.button.small-expand,\r\n" \
    "  table.button.small-expanded {\r\n" \
    "    width: 100% !important; }\r\n" \
    "    table.button.small-expand table,\r\n" \
    "    table.button.small-expanded table {\r\n" \
    "      width: 100%; }\r\n" \
    "      table.button.small-expand table a,\r\n" \
    "      table.button.small-expanded table a {\r\n" \
    "        text-align: center !important;\r\n" \
    "        width: 100% !important;\r\n" \
    "        padding-left: 0 !important;\r\n" \
    "        padding-right: 0 !important; }\r\n" \
    "    table.button.small-expand center,\r\n" \
    "    table.button.small-expanded center {\r\n" \
    "      min-width: 0; } }\r\n" \
    " </style>\r\n" \
    "</head>\r\n"
