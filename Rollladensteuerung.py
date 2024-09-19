import sys
import os
sys.path.append("/home/christof/Daten/Software/repositories")
from Cmulti_v02.cmulti import CMULTI
import Secrets.mySecrets as secrets


class Rollladensteuerung(CMULTI):
    def __init__(self, source, target, comPort="", baudRate=57600, backChannel="TLog", withCrc=True, timeout=5000):
        super(self.__class__, self).__init__(source, comPort, baudRate, backChannel, withCrc, timeout)
        self.target = target
        self.comPort = comPort

    def getSerialNumber(self):
        return self.sendCommand(self.target, "P", "0", "i")

    def getHeaterActualStatus(self, address):
        return self.sendCommand(self.target, "V", chr(address + 48), "a")

    def getHeaterSetStatus(self, address):
        return self.sendCommand(self.target, "V", chr(address + 48), "s")

    def getHeaterSwellValue(self, address):
        return self.sendCommand(self.target, "V", chr(address + 48), "d")

    def getHeaterNightSwellValue(self, address):
        return self.sendCommand(self.target, "V", chr(address + 48), "n")

    def getHeaterHystValue(self, address):
        return self.sendCommand(self.target, "V", chr(address + 48), "h")

    def setRolloPosition(self, address, position):
        return self.sendCommand(self.target, "X", chr(address + 48), "S", parameter="%.4f" % position)

    def setWurzelbrumf(self, address, position):
        return self.sendCommand(self.target, "X", chr(address + 48), "X", parameter="%.4f" % position)

    def setFixPosition0(self, address, position):
        return self.sendCommand(self.target, "a", chr(address + 48), "S", parameter="%d" % position)

    def setFixPosition1(self, address, position):
        return self.sendCommand(self.target, "b", chr(address + 48), "S", parameter="%d" % position)

    def setFixPosition2(self, address, position):
        return self.sendCommand(self.target, "c", chr(address + 48), "S", parameter="%d" % position)

    def setUptime(self, address, position):
        return self.sendCommand(self.target, "U", chr(address + 48), "S", parameter="%d" % position)

    def setDowntime(self, address, position):
        return self.sendCommand(self.target, "D", chr(address + 48), "S", parameter="%d" % position)

    def setToFixPos0(self, address):
        return self.sendCommand(self.target, "F", chr(address + 48), "0", parameter="")

    def setTimeBetweenBlocks(self, blockTime):
        return self.sendCommand(self.target, "R", "0", "B", parameter="%d" % blockTime)

    def setTimeBetweenSensors(self, repTime):
        return self.sendCommand(self.target, "R", "0", "S", parameter="%d" % repTime)

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

    test = Rollladensteuerung('CC', 'R0', comPort="/dev/RS485-1")
    print("SetSecurity")
    print(test.setSecurityKey(secrets.SECURITY_LEVEL_DEVELOPMENT_KEY))
    time.sleep(0.5)
    print(test.prepareBootload("34&dkjg+dl23"))
    time.sleep(0.5)
    test.startBootload()
    time.sleep(0.6)
    test.writeFlash("/home/christof/Daten/Software/repositories/RollladenSteuerung/bin/Release/RollladenSteuerung.hex")
