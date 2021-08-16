import sys, os
import time
sys.path.append("/home/christof/Daten/Software/repositories")


from Cmulti_v02.cmulti import CMULTI
import Secrets.secrets as secrets


class Lueftersteuerung(CMULTI):
  def __init__(self,source,target,comPort="", baudRate=57600, backChannel="TLog", withCrc = True, timeout=5000):
    super(self.__class__,self).__init__(source,comPort , baudRate, backChannel, withCrc, timeout)
    self.target = target
    self.comPort = comPort
    
  def getFreeMemory(self):
    return self.sendCommand(self.target, "S", "0", "m")
      
  def getCompilationDate(self):
    return self.sendCommand(self.target, "S", "0", "C")
    
  def getCompilationTime(self):
    return self.sendCommand(self.target, "S", "0", "T")
    
  def setSecurityKey(self, key):
    return self.sendCommand(self.target, "S", "0", "K", parameter=key)

  def prepareBootload(self, key):
    return self.sendCommand(self.target, "S", "0", "A", parameter=key)

  def startBootload(self):
    return self.sendCommand(self.target, "S", "0", "B")

  def setBeSilent(self, silent):
    return self.sendCommand(self.target, "S", "0", "S", parameter=str(int(silent)))

  def doReset(self):
    return self.sendCommand(self.target, "S", "0", "R")
  
  def setBlockTime(self, time):
    return self.sendCommand(self.target, "T", "0", "B", parameter=str(int(time)))

  def setWaitBetweenSample(self, time):
    return self.sendCommand(self.target, "T", "0", "W", parameter=str(int(time)))

  def writeFlash(self, flashFile):
    os.system(
      "avrdude -e -c avr109 -p ATxmega128A4U -P " + self.comPort +
      " -b 57600 -U flash:w:"+flashFile+":i")


if __name__ == "__main__":
  import time
  test = Lueftersteuerung('CC', 'LB', comPort="/dev/RS485-1")
  print( test.setSecurityKey(secrets.SECURITY_LEVEL_DEVELOPMENT_KEY) )
  time.sleep(0.5)
  print( test.prepareBootload("34&dkjg+dl23") )
  test.startBootload()
  time.sleep(1)
  test.writeFlash("/home/christof/Daten/Software/repositories/LuefterSteuerung/bin/Release/LuefterSteuerung.hex")

