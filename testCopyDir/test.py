
import shutil
import os

def backupReportFiles(dir_path) :
    num = 1;
    new_folder = "";
    index = len(str(dir_path).split("/")) - 1;
    dir_name = str(dir_path).split("/")[index];
    while True :
        new_folder = dir_name + "_" + str(num);
        num = num + 1;
        if(not os.path.exists(new_folder)) :
            break;

    shutil.copytree(dir_path, new_folder);
    

backupReportFiles("34/56");

import argparse
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--gpus', type=str, default = None)
parser.add_argument('--batch-size', type=int, default=32)
args = parser.parse_args()
print args.gpus
print args.batch_size
