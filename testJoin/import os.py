import os

current_dir = os.path.split(os.path.realpath(__file__))[0];
dir = os.path.join(current_dir, "123", '123');
print(dir);