from distutils.command.build import build
import os, subprocess


current_dir = os.getcwd()
root_path = os.path.join(current_dir, "..")
root_path = os.path.normpath(root_path)
print(root_path)
build_path = os.path.join(root_path, "build", "Debug", "CppProject.exe")

build_path = build_path.split()
print(build_path)
subprocess.check_call(build_path)