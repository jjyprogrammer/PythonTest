from asyncore import write
import json, collections, os

with open("ngx_core_config.json", "r") as read_file :
    lines = read_file.readlines();
    with open("ngx_core_config.json.tmp", "w") as write_file :
        for line in lines :
            if line.find("\"adas_chs\": 0") != -1 :
                print("====")
                print(line)
                newline = line.replace("\"adas_chs\": 0", "\"adas_chs\": 1");
                print(newline);
                write_file.write(newline)
            else:
                write_file.write(line)
                print(line);
os.remove("ngx_core_config.json")
os.rename("ngx_core_config.json.tmp", "ngx_core_config.json")


