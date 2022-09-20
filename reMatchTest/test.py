import subprocess, os
sourceDirectory = os.getcwd()
cmd = "python %s//myDir/test1.py" % (sourceDirectory)
test_dir = "%s/myDir" % sourceDirectory
os.chdir(test_dir)
os.system(cmd)
subprocess.call(cmd)


import re
branch_name = 'bugfix/MSL-1339-first-ni-build-failed-in-regression-revert-base-version'
if(re.match('^(release|master|feature/mosel-1.0)+.*', branch_name)) :
    print(True)
else:
    print(False)
