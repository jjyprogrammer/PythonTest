import sys

force_verbose = True;
for arg in sys.argv :
    print(arg);

print(any("-v" in arg for arg in sys.argv));

if force_verbose and not any("-v" in arg for arg in sys.argv):
    print("hello");