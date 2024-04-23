import sys
sys.path.append("/home/christof/Daten/Software/repositories")

from Cmulti_v02.cmulti import CMULTI
#import Secrets.secrets as secrets


class Dimmer(CMULTI):
    def __init__(self, source, target, comPort="", baudRate=57600, backChannel="TLog", withCrc=True, timeout=5000):
        super(self.__class__, self).__init__(source, comPort, baudRate, backChannel, withCrc, timeout)
        self.target = target

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
        return self.sendCommand(self.target, "S", "0", "S", parameter=str(int(silent)), expectAnswer=False)

    def doReset(self):
        return self.sendCommand(self.target, "S", "0", "R", expectAnswer=False)

    def setBlockTime(self, time):
        return self.sendCommand(self.target, "T", "0", "B", parameter=str(int(time)))

    def setWaitBetweenSample(self, time):
        return self.sendCommand(self.target, "T", "0", "W", parameter=str(int(time)), expectAnswer=False)

    def increase(self):
        return self.sendCommand(self.target, "D", "0", "+", expectAnswer=False)

    def decrease(self):
        return self.sendCommand(self.target, "D", "0", "-", expectAnswer=False)

    def set(self, status):
        return self.sendCommand(self.target, "D", "0", "S", parameter=str(int(status)), expectAnswer=False)


if __name__ == "__main__":
    test = Dimmer('CC', 'CB', comPort="/dev/RS485-1")
    print(test.set(200))
