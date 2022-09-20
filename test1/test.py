import hello
import sys, os
import my_package.module1
import my_package.module1 as module
import my_package
from my_package import module2
from my_package.module2 import CLanguage as CLanguage
from my_package.module2 import testStr



print("test");


class MyTest:
    print("myTest")


my_package.module1.display("module1")
module.display("module")

lang = CLanguage();
lang.display();

print(testStr);


print(os.environ.keys())
print(os.environ["EXTERNAL_MODULES_PATH"])


