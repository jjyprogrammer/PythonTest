import os,sys


if(not os.path.exists("build")) :
    os.mkdir("build")

os.environ["Build_Type"] = "CI"
os.chdir("build")
os.system("cmake ..")
os.system("cmake --build .")