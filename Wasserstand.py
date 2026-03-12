import sys
import os
sys.path.append("./..")
from Cmulti_v02.cmulti import CMULTI
import Secrets.mySecrets as secrets


class Wasserstand(CMULTI):
    def __init__(self, source, target, comPort="", baudRate=57600, backChannel="TLog", withCrc=True, timeout=5000):
        super(self.__class__, self).__init__(source, comPort, baudRate, backChannel, withCrc, timeout)
        self.target = target
        self.comPort = comPort

    def getSerialNumber(self):
        return self.sendCommand(self.target, "P", "0", "i")

    def setWater(self, water):
        return self.sendCommand(self.target, "W", "0", "s", parameter="%d" % water, expectAnswer=False)

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

    def writeFlash(self, flashFile):
        os.system(
          "avrdude -e -c avr109 -p ATxmega32A4U -P " + self.comPort +
          " -b 57600 -U flash:w:"+flashFile+":i") # avrdude -c avrispmkII -P usb  -p $(MCU) -v -Uflash:w:$(TARGET_OUTPUT_DIR)$(TARGET_OUTPUT_BASENAME).hex:i


if __name__ == "__main__":
    import time

    test = Wasserstand('HA', 'W1', comPort="/dev/RS485-1")
    

    test.setWater(315467)
    time.sleep(1)
