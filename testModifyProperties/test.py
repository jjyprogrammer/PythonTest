import os, sys, logging

file = open("gradle.properties", 'r')
content = file.readlines()
for i in range(len(content)) :
    if(content[i].find("versionName=") != -1) :
        content[i] = "versionName=" + "123"
file.close()
file = open("gradle.properties", 'w')
for line in content :
    file.write(line)
    print(line)
file.close()