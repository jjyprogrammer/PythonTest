import subprocess, os

cmd = 'python %s' % ("cmd.py");
print(cmd)
current_dir = os.getcwd();
print(current_dir);
cmd_output = subprocess.call('python %s' % ("cmd.py"))
if(cmd_output) :
    raise SystemError("1")
print(cmd_output)