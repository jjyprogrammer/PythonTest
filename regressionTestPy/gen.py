import os
import glob
import shutil
import sys
import math
import copy
import json
import difflib
from unittest import result
import webbrowser


INPUT_FORMAT = ".json"
TOTAL_COUNT = 0
FAILED_COUNT = 0

#diff files list
BASE_LIST = []
NEWER_LIST = []

INPUT_LIST = []
INPUT_LIST_ADD = []
INPUT_LIST_REMOVE = []
 
BE_TESTED_FILE_NAME_LIST = []
CHANGED_FILE_LIST = []
ADD_FILE_NAME_LIST = []
REMOVE_FILE_NAME_LIST = []
#Index character
Index = "road"


#global
WORK_PATH  = os.path.abspath('.')
REPORT_PATH = "" 
HTML5_PATH = ""
REPORT_HTML = ""

#input file
BASE_DIR = ""
NEW_DIR = ""
JSON_FILE = ""


#input index
input_index = "-1";
failed_test = False;
failed_backup_path = "";

def setIndex(index) :
    global input_index;
    input_index = index;

def setNewFailedBackupPath(new_path) :
    global failed_backup_path
    failed_backup_path = new_path;

def setRegion(region):
    print("setRegion " + region)
    global REPORT_PATH
    global HTML5_PATH
    global REPORT_HTML
    global BASE_DIR
    global NEW_DIR
    global JSON_FILE

    print(WORK_PATH)

    REPORT_PATH = WORK_PATH + "/result/report"
    if not  os.path.exists(REPORT_PATH):
        os.makedirs(REPORT_PATH)
        print(REPORT_PATH)
    HTML5_PATH = REPORT_PATH + "/" + region +"/"
    REPORT_HTML = HTML5_PATH  + "report.html"
    #input file
    BASE_DIR = WORK_PATH + "/result/baseline/" + region + "/"
    NEW_DIR = WORK_PATH + "/result/new/" + region + "/"
    JSON_FILE = WORK_PATH + "/cases/" +  region +"/" + 'MoselADASCase.json'
        
    print(os.path.exists(BASE_DIR))
    print(os.path.exists(NEW_DIR))
    print(os.path.exists(JSON_FILE))

def read_file(filename):
    try:
        with open(filename, mode='r') as f:
            return f.readlines()
    except IOError:
        print("can't open file!" + filename)
        sys.exit(1)

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def compare_file(file1, file2, out_file):
    #print("compare_file")
    file1_contet = read_file(file1)
    file2_content = read_file(file2)

    diff_path =  HTML5_PATH + "diffHtml"
    create_dir(diff_path)
    
    rate = difflib.SequenceMatcher(None, file1_contet, file2_content)
    #print (rate.ratio())     #judget if the file is same
    
    if(rate.ratio() < 1):
        global CHANGED_FILE_LIST
        CHANGED_FILE_LIST.append(getFileName(file2))
        
        d = difflib.HtmlDiff()
        result = d.make_file(file1_contet,file2_content)
        
        with open(out_file, 'w+') as f:
            f.writelines(result)
        return False
           
    else:
        #print("file is the same!")
        return True

def getFileIndex(filename):
    a = os.path.basename(filename)
    tmp = a.split('.')[0]
    tmp = tmp.replace(Index,'')
    return tmp

def getFileName(filename):
    a = os.path.basename(filename)
    tmp = a.split('.')[0]
    return tmp

def open_report():
    webbrowser.open(REPORT_HTML)
 
def getChangedRate():
    return str(FAILED_COUNT) + "/" + str(len(BE_TESTED_FILE_NAME_LIST))

def getFileNameList(targetList):
    t_list = []
    for i in targetList:
        t_list.append(getFileName(i))
    return t_list

def getRemoveFiles(base,new):
    print("getRemoveFiles")   
    t_list = getFileNameList(base)
    for i in new:
        name = getFileName(i)
        if(t_list.__contains__(name)):
            t_list.remove(name)
    
    print(t_list)
    return t_list

def getAddedFiles(base,new):
    print("getAddedFiles")
    t_list = getFileNameList(new)
    for i in base:
        name = getFileName(i)
        if(t_list.__contains__(name)):
            t_list.remove(name)    
    #print(t_list)
    return t_list

def getListItem2string(Itemlist):
    itemString=' '
    for i in Itemlist:
        itemString = itemString + i + ",  " 
    return itemString

# list1 - list2 
# list1 > list2
def removeSameValue(list1,list2):
    print("removeSameValue")  
    for j in list2:
        for i in list1:        
            if(i == j):
                list1.remove(i)
    return list1

def gengrate_report():
    print("gengrate_report")
    print(CHANGED_FILE_LIST)
    head = """
        <html>
        <head></head>
        <body text-align:center> 
        <style type=""text/css"">
        .mytable{
            margin:0px auto;
        }
        </style>  
        """

    tail = """   
        </body>
        </html>
        """   

    result_color = "<font color=""orange"">"
    result_color_warning = "<font color=""red"">"
    tab = "&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"
    newline = "<br></br>"

    char_summary = "<table cellspacing=""2"" bgcolor=""black""  width=""800"" height=""200""  class=""mytable""><caption><h3>Summary<h3></caption>" 
    char_summary = char_summary + "<tr bgcolor=""white"" align=""center""><td></td><td><font font-wight:700>files change<font></td>"
    head = head + char_summary

    if(len(INPUT_LIST_ADD) + len(INPUT_LIST_REMOVE) > 0):
        head = head + "<tr bgcolor=""white""><td>Baseline compared with case input</td><td>"
        head = head + "<font size=""2"">" + "Input case counts:"    + result_color + str(len(INPUT_LIST)) + "</font>"+ newline 
        head = head + "<font size=""2"">" + "Baseline counts:" + result_color + str(len(BASE_LIST)) + "</font>"+ newline 
        head = head + "<font size=""2"">" + "Added files"  + "("+ str(len(INPUT_LIST_ADD))+")"+":    "+ result_color + getListItem2string(INPUT_LIST_ADD) + "</font>"+ newline 
        head = head + "<font size=""2"">" + "Removed files" + "("+ str(len(INPUT_LIST_REMOVE))+")"+":  "+result_color +getListItem2string(INPUT_LIST_REMOVE) + "</font>"
        head = head + "</td>" 
        
    
    head = head + "<tr bgcolor=""white""><td>Output compared with baseline input</td><td>"
    head = head + "<font size=""2"">" + "Baseline counts:" + result_color + str(len(BASE_LIST)) + "</font>" + newline
    head = head + "<font size=""2"">" + "Newer counts:"    + result_color + str(len(NEWER_LIST)) + "</font>" + newline
    head = head + "<font size=""2"">" + "Added files"  + "("+ str(len(ADD_FILE_NAME_LIST))+")"+":    "+ result_color + getListItem2string(ADD_FILE_NAME_LIST) + "</font>"+ newline
    head = head + "<font size=""2"">" + "Removed files" + "("+ str(len(REMOVE_FILE_NAME_LIST))+")"+":  "+ result_color + getListItem2string(REMOVE_FILE_NAME_LIST) + "</font>"+ newline
    head = head + "<font size=""2"">" + "Compared file counts:    "    + result_color+str(len(BE_TESTED_FILE_NAME_LIST)) + "</font>"+ newline
    head = head + "<font size=""2"">" + "Changed files"   +"(" + str(len(CHANGED_FILE_LIST))+")"+":    " + result_color_warning + getListItem2string(CHANGED_FILE_LIST)  + "</font>"
    head = head + "</td>" + "</tr></table>"

    f = open(REPORT_HTML,'w')    
    if(len(CHANGED_FILE_LIST)>0):
        result = newline 
        
        result = result + "<table cellspacing=""3"" bgcolor=""black""  width=""800"" height=""200"" class=""mytable""><caption><h3>Compare Result%s</h3></caption>" %( "("+ str(getChangedRate()) +")")
        result = result + "<tr bgcolor=""white"" align=""center""><td>num</td><td>name</td><td>status</td>"
        head = head + result
        

        order = 0
        for name in BE_TESTED_FILE_NAME_LIST:            
            if getFileName(name) in CHANGED_FILE_LIST:
                #opened_html = HTML5_PATH + "diffHtml\\" + "diff_road" + str(getFileIndex(name)) + ".html"
                opened_html = "./diffHtml/" + "diff_" + str(getFileIndex(name)) + ".html"
                order = order + 1
                #fail_url = "<a href=%s><font color=""red"" target=""_blank"">%s</font></a>"  %(opened_html,"Failed!")
                fail_url = "<a href=%s target=""_blank""><font color=""red"">%s</font></a>"  %(opened_html,"Failed!")
                tmp = "<tr bgcolor=""white"" align=""center""><td>%d</td><td>%s</td><td>%s</td>" %(order,getFileName(name),fail_url)
                
            else:
                order = order + 1
                success_url = "<font color=""green"">%s</font>" %("Success!")
                tmp = "<tr bgcolor=""white"" align=""center""><td>%d</td><td>%s</td><td>%s</td>" %(order,getFileName(name),success_url)

            head = head + tmp + "<p></p>"
           
    else:        
         result = "<h3 align=""center"">"+ "Common routes have not been  changed!" +"</h3>"
         head = head + result        

    htmlMessage = head + tail    
    f.write(htmlMessage)
    f.close()

def getInputJsonRouteList():
    tmp_list = []
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    for i in range(len(data['case_items'])):
        tmp_list.append(data['case_items'][i]['case_name']) 
    f.close()
    return  tmp_list

#=================================main()===========================================
#get file count
def startExec(region):
    setRegion(region)
    global BASE_LIST
    global NEWER_LIST
    global INPUT_LIST
    global INPUT_LIST_ADD
    global INPUT_LIST_REMOVE
    global TOTAL_COUNT
    global REMOVE_FILE_NAME_LIST
    global ADD_FILE_NAME_LIST
    global BE_TESTED_FILE_NAME_LIST
    base_list  = glob.glob( BASE_DIR +'*'+ INPUT_FORMAT)
    new_list = glob.glob( NEW_DIR + '*' + INPUT_FORMAT)


    #compare with base routes
    BASE_LIST  = getFileNameList(base_list)
    NEWER_LIST = getFileNameList(new_list)
    # INPUT_LIST = getInputJsonRouteList()

    # INPUT_LIST_ADD = getAddedFiles(INPUT_LIST,BASE_LIST)
    # INPUT_LIST_REMOVE = getRemoveFiles(INPUT_LIST,BASE_LIST)

    BE_TESTED_FILE_NAME_LIST = copy.copy(NEWER_LIST)
    # BE_TESTED_FILE_NAME_LIST = sortFileNames(INPUT_LIST, BE_TESTED_FILE_NAME_LIST);
    TOTAL_COUNT = len(new_list)
    REMOVE_FILE_NAME_LIST = getRemoveFiles(base_list,new_list)
    ADD_FILE_NAME_LIST = getAddedFiles(base_list,new_list)


    #gen common files list
    BE_TESTED_FILE_NAME_LIST = removeSameValue(BE_TESTED_FILE_NAME_LIST,ADD_FILE_NAME_LIST)
    BE_TESTED_FILE_NAME_LIST = removeSameValue(BE_TESTED_FILE_NAME_LIST,REMOVE_FILE_NAME_LIST)

    print("base_list:" + str(len(BASE_LIST)))
    #print(BASE_LIST)
    print("new_list" + str(len(NEWER_LIST)))
    #print(NEWER_LIST)
    print("BE_TESTED_FILE_NAME_LIST" + str(len(BE_TESTED_FILE_NAME_LIST)))
    print(BE_TESTED_FILE_NAME_LIST)

    #compare common files
    create_dir(HTML5_PATH)
    print("HTML5_PATH  " + HTML5_PATH )
    for i in BE_TESTED_FILE_NAME_LIST:
        base_route  =  BASE_DIR + i + INPUT_FORMAT
        new_route =  NEW_DIR + i + INPUT_FORMAT
        output_html =  HTML5_PATH + "diffHtml/" + "diff_" + i + ".html";
        global FAILED_COUNT
        if(compare_file(base_route, new_route, output_html)==False):
            FAILED_COUNT = FAILED_COUNT + 1

    gengrate_report()

    # if(FAILED_COUNT > 0 or failed_test) :
    #     print("*" * 50, "remove report");
    #     backupResultFiles();
    #     FAILED_COUNT = 0;
    #     return -1;
    backupResultFiles();
    return 0;
    
def backupResultFiles() :    
    global failed_backup_path
    new_folder = failed_backup_path;
    result_dir = "result";
    dest_dir = result_dir + str(input_index);
    dest_dir = os.path.join(new_folder, dest_dir);
    
    dest_log_dir = os.path.join(dest_dir, "MoselLog")
    src_dir = os.path.join(WORK_PATH, "result");
    src_log_dir = os.path.join(WORK_PATH, "MoselLog");

    shutil.copytree(src_dir, dest_dir);
    shutil.copytree(src_log_dir, dest_log_dir);

    
def sortFileNames(input_file_name_list, be_tested_file_name_list) :
    results = [];
    for i in input_file_name_list :
        for j in be_tested_file_name_list :
            if(i == j) :
                results.append(i);
    return results;

import sys
if __name__ == '__main__':
    print("main() :" + sys.argv[1])
    input_index = sys.argv[2];
    startExec(sys.argv[1])
    
