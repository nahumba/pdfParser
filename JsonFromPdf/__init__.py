# -*- coding: utf-8 -*-

# copyright Nahumba contact me at nahumba@cs.bgu.ac.il
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import re
import subprocess
import time
from CGIHTTPServer import executable

data ={}
OneChar =4
TwoChars = 2*OneChar
ThreeChars = 3*OneChar
#
#remember to add this 3 lines to sample-xpdfrc,and remove the first # from each line.
##----- begin Hebrew support package (2011-aug-15)
#unicodeMap	ISO-8859-8	c:\tmp\xpdfbin-win-3.04\hebrew\ISO-8859-8.unicodeMap
#unicodeMap	Windows-1255	c:\tmp\xpdfbin-win-3.04\hebrew\Windows-1255.unicodeMap
##----- end Hebrew support package
inputSederPdf = '\\..\\seder040216.pdf'
toolAt ='C:\\tmp\\xpdfbin-win-3.04'
#you need to install xpdf to use the pdftotext, then add the config sample-xpdfrc , then feed the pdf.
def extractText():
    callcallcall= [toolAt+"\\bin64\\pdftotext.exe", "-enc","UTF-8", "-cfg", toolAt+"\\doc\\sample-xpdfrc",  toolAt+inputSederPdf]
    print callcallcall
    subprocess.call(callcallcall)

    time.sleep(5)
    return

def SaveJsonToFile(data):
    with open('laws.json', 'w') as outfile:
        json.dump(data,outfile,ensure_ascii=False)
    return;

def LoadPdf():
    return open('c:\\tmp\\seder040216.txt','r');

def ParseFileToAST(pdfDump):
    law =''
    Started = 0
    for line in pdfDump: # in unicode each char is 8 length long?
        if Started == 0 :
            if line.find('נושא‬')>0:
                Started = 1
                data['first page header']= law
                law = ''
            law = law + line
            continue # ignore all first page header
        elif line.find('נושא')>0:
            continue # we ignore page start
        if len(line.strip())>8 :
            if ((line.find('.',8,9)) and (len(line)<=16)) or ((line.find('.',8,16)) and (len(line)<=20)):
                data[line] = law
                law = ''
            elif len(re.split('\.',line,1)[0])<=TwoChars  : # unicode
                data[re.split('\.',line,1)[0]] =re.split('\.',line,1)[1]
            else:
                law = law + line
                #print line
    print 'data output: '
    print data
    print 'i hope its clear'
    return data;

extractText()
pdfDump = LoadPdf()
#print pdfDump.read() # debug
data = ParseFileToAST(pdfDump)
SaveJsonToFile(data)
pdfDump.close()