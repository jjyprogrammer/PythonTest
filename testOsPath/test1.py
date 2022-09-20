import os, logging, subprocess

logging.basicConfig(level=logging.INFO)

print(os.path.normpath("A/foo/../B"))

source_dir = "..";
logging.info("dir is %s", source_dir)
logging.info("dir is %s", source_dir)
exist_no = subprocess.call("python 123.py")
error_str = "exit no : %s" % exist_no
raise Exception("exit no : %s" % exist_no)
