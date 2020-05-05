import sys, os
import time

sys.path.append("/home/chrak/Daten/Software/repositories") 

from Cmulti_v02.cmulti import CMULTI
import Secrets.secrets as secrets

class Klima(CMULTI):
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
    return(self.sendCommand(self.target,"S","0","A",parameter=key))

  def startBootload(self):
    return(self.sendCommand(self.target,"S","0","B"))

  def setBeSilent(self,silent):
    return(self.sendCommand(self.target,"S","0","S",parameter=str(int(silent))))

  def doReset(self):
    return(self.sendCommand(self.target,"S","0","R"))
  
  def setBlockTime(self,time):
    return(self.sendCommand(self.target,"T","0","B",parameter=str(int(time))))

  def setWaitBetweenSample(self,time):
    return(self.sendCommand(self.target,"T","0","W",parameter=str(int(time))))

if __name__ == "__main__":
  test = Klima('CC','C1',comPort="mqtt")
  print( test.getCompilationDate() )
  print( test.setSecurityKey(secrets.SECURITY_LEVEL_DEVELOPMENT_KEY) )
  print( test.getCompilationDate() )
  print( test.getCompilationTime() )
  print( test.getFreeMemory() )
  print( test.setBlockTime(12000) )
  print( test.setWaitBetweenSample(1000) )
  print( test.setBeSilent(False) )
  print( test.doReset() )


