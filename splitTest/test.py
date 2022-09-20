import subprocess, os


current_dir = os.getcwd();

cmd = "python %s/123.py" % current_dir;
# cmd = cmd.split();
subprocess.call(cmd)
subprocess.check_call(cmd)