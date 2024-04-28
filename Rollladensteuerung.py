import sys
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
        return self.sendCommand(self.target, "S", chr(address + 48), "S", parameter="%.2f" % position)

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


if __name__ == "__main__":
    import time

    test = Rollladensteuerung('CC', 'R0', comPort="/dev/RS485-1")
    print(test.setSecurityKey(secrets.SECURITY_LEVEL_DEVELOPMENT_KEY))
    print(test.getCompilationTime())
    print(test.getCompilationDate())
    print(test.setRolloPosition(1, 45.5))
    print(test.setFixPosition0(1, 83))
    print(test.setFixPosition1(1, 53))
    print(test.setFixPosition2(1, 63))
    print(test.setUptime(1, 4231))
    print(test.setDowntime(1, 3331))
    print(test.setToFixPos0(1))
    #for v in range(0, 2):
    #    print(test.getHeaterSetStatus(v))
    time.sleep(0.5)
