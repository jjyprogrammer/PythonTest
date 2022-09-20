from __future__ import print_function
import os, shutil,io, json
import sys
import argparse
import gen


current_dir = os.path.split(os.path.realpath(__file__))[0];
result_path = os.path.join(current_dir, "result");
new_path = os.path.join(result_path, "new");
base_path = os.path.join(result_path, "baseline");
report_path = os.path.join(result_path, "report");
report_failed_path = os.path.join(result_path, "failedReport");
pe_persist_file_path = os.path.join(current_dir, "pe_persist.bin")

region = "NA";
execute_cmd = "run_test_tnehp_sdk.exe" + " " + "-region=" + region;
script_cmd = "python script/gen.py" + " " + region;


failed_count = 0;
test_count = 1;
failed_test = False;
once_run_base = False;
    

def clear() :
    try :
        global new_path
        global base_path
        global report_path
        shutil.rmtree(new_path);
        shutil.rmtree(base_path);
        shutil.rmtree(report_path);
    except Exception as e:
        print("-- exception :", str(e));
    
def executeCmd(args) :
    global execute_cmd
    cmd = execute_cmd + " " + args;
    try :
        print("-- ", "start cmd " + cmd);
        if(os.system(cmd)) :
            raise Exception(cmd + " error");
    except Exception as e :
        print("-- exception", str(e));

def modifyDir() :
    print("-- ", "modify dir", new_path, base_path);
    os.rename(new_path, base_path);

def executeScript(index) :
    global failed_count
    global failed_test
    gen.setIndex(index);
    gen.failed_test = failed_test;
    if(gen.startExec(region) == -1) :
        failed_count = failed_count + 1;

def getNewFailedFolder(dir_path) :
    num = 1;
    new_folder = "";
    index = len(str(dir_path).split("/")) - 1;
    dir_name = str(dir_path).split("/")[index];
    while True :
        new_folder = dir_name + "_" + str(num);
        num = num + 1;
        if(not os.path.exists(new_folder)) :
            break;
    return new_folder;

def setFailedBackupPath() :
    global current_dir;
    failed_dir = "failedReport";
    failed_report_path = os.path.join(current_dir, failed_dir);
    new_folder = getNewFailedFolder(failed_report_path);
    gen.setNewFailedBackupPath(new_folder);

def removePEPersistFile() :
    global pe_persist_file_path;
    if(os.path.exists(pe_persist_file_path)) :
        os.remove(pe_persist_file_path)

def getCaseCount() :
    global region
    global current_dir
    case_count = 0;
    case_file_name = "MoselADASCase.json";
    case_path = os.path.join(current_dir, "cases", region, case_file_name);
    with io.open(case_path, 'r', encoding='utf-8') as f :
        case_obj = json.load(f);
        case_count = len(case_obj['case_items']);
        f.close;
    return case_count;

def main() :
    global test_count;
    global failed_test;
    case_count = getCaseCount();
    print("-- ", "test count ", test_count);
    print("-- ", "clear environment");
    clear();
    setFailedBackupPath();
    index = 0
    for i in range(0, test_count) :
        print("-- ", "test index ", i + 1);
        for j in range(0, case_count) :
            args = "-case-index=" + str(j);
            if not failed_test and not once_run_base:
                executeCmd(args);
                removePEPersistFile();
            executeCmd(args);
            removePEPersistFile();
            modifyDir();
            executeCmd(args);
            removePEPersistFile();
            index = index + 1;
            executeScript(index);
            clear();
            
    
    print("*" * 50);
    print("failed count : ", failed_count);
        

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--failed-test', required = False, action = 'store_true');
    parser.add_argument('--once-run', required = False, action = 'store_true');
    parser.add_argument('--count', required = False, type = int, default = 1);
    args = parser.parse_args()
    failed_test = args.failed_test
    test_count = args.count
    once_run_base = args.once_run;
    print("-- failed_test ", failed_test);
    print("-- test_count ", test_count);
    print("-- once_run_base ", once_run_base);
    main();


