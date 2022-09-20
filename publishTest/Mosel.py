from Component import *
from process import *

class Mosel(Component):
    
    def publish(self, buildNumber) :
        print("son publish");
        print("son publish", buildNumber);
        Component.publish(self, buildNumber)
    
        
        
        
com = Mosel()
test(com);