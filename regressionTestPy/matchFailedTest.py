from __future__ import print_function
import os, shutil,io, json, re
import sys
import argparse


current_dir = os.path.split(os.path.realpath(__file__))[0];
failed_report_dir = os.path.join(current_dir, "failedReport");

double_map_matching_array = ["map matching callback number .*\n\s*map matching callback number", "map matching callback number .*\n\s*callback adas coming.*\n\s*map matching callback number", "callback adas coming.*\n\s*callback adas coming.*\n\s*", "map matching callback number .*\n\s*callback adas coming.*\n\s*adas coming:.*\n\s*add message :.*\n\s*map matching callback number"];

def getFailedFolderList(dir_path) :
    failed_report_path_list = [];
    num = 1;
    new_folder = "";
    index = len(str(dir_path).split("/")) - 1;
    dir_name = str(dir_path).split("/")[index];
    while True :
        new_folder = dir_name + "_" + str(num);
        num = num + 1;
        if(not os.path.exists(new_folder)) :
            break;
        else :
            failed_report_path_list.append(new_folder)
    return failed_report_path_list;

def getLogFileList(dir_path) :
    log_file_list = [];
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            if name.endswith(".txt") :
                log_file_list.append(os.path.join(root, name));
    return log_file_list;
    
def main() :
    failed_report_path_list = getFailedFolderList(failed_report_dir);
    for dir in failed_report_path_list :
        print(dir)
        log_file_list = getLogFileList(dir);
        for path in log_file_list :
            file = open(path);
            lines = file.read();
            file.close;
            for match_regular in double_map_matching_array :
                match = re.search(match_regular, lines)
                if match :
                    print(path);

        

if __name__ == '__main__' :
    main();


