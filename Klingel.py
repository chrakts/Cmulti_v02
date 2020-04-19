import sys, os
import time

sys.path.append("/home/chrak/Daten/Software/repositories") 

from Cmulti_v02.cmulti import CMULTI
import Secrets.secrets as secrets


class Klingel(CMULTI):
  def __init__(self,source,target,comPort="", baudRate=57600, backChannel="TLog", withCrc = True, timeout=5000):
    super(self.__class__,self).__init__(source,comPort , baudRate, backChannel, withCrc, timeout)
    self.target = target
    
  def getFreeMemory(self):
    return(  self.sendCommand(self.target,"S","0","m")  )
      
  def getCompilationDate(self):
    return(  self.sendCommand(self.target,"S","0","C")  )
    
  def getCompilationTime(self):
    return(  self.sendCommand(self.target,"S","0","T")  )
    
  def setSecurityKey(self,key):
    return(self.sendCommand(self.target,"S","0","K",parameter=key))

  def prepareBootload(self,key):
    return(self.sendCommand(self.target,"M","0","A",parameter=key))

  def startBootload(self):
    return(self.sendCommand(self.target,"M","0","B"))

  def klingeln(self,klingel):
    return(self.sendCommand(self.target,"K","0","r",expectAnswer=False,parameter=str(klingel)))
  
  def pirTrigger(self):
    return(self.sendCommand(self.target,"P","0","t",expectAnswer=False))


test = Klingel('CC','Kg',comPort="mqtt")
print( test.getCompilationDate() )
print( test.setSecurityKey("D=&27ane%24dez") )
print( test.getCompilationDate() )
print( test.getCompilationTime() )
print( test.getFreeMemory() )
#print( test.prepareBootload("#34&dkjgdl23") )
#print( test.startBootload() )
test.klingeln(0)
#test.pirTrigger()




