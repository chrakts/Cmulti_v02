import sys

sys.path.append("/home/christof/Daten/Software/repositories")

from Cmulti_v02.cmulti import CMULTI
import Secrets.mySecrets as secrets


class Ventilsteuerung(CMULTI):
    def __init__(self, source, target, comPort="", baudRate=57600, backChannel="TLog", withCrc=True, timeout=5000):
        super(self.__class__, self).__init__(source, comPort, baudRate, backChannel, withCrc, timeout)
        self.target = target
        self.comPort = comPort
    def getSerialNumber(self):
        return (self.sendCommand(self.target, "P", "0", "i"))

    def getHeaterActualStatus(self, address):
        return (self.sendCommand(self.target, "V", chr(address + 48), "a"))

    def getHeaterSetStatus(self, address):
        return (self.sendCommand(self.target, "V", chr(address + 48), "s"))

    def getHeaterSwellValue(self, address):
        return (self.sendCommand(self.target, "V", chr(address + 48), "d"))

    def getHeaterNightSwellValue(self, address):
        return (self.sendCommand(self.target, "V", chr(address + 48), "n"))

    def getHeaterHystValue(self, address):
        return (self.sendCommand(self.target, "V", chr(address + 48), "h"))

    def setHeaterSetStatus(self, address, status):
        return (self.sendCommand(self.target, "V", chr(address + 48), "S", parameter=status))

    def setHeaterSwellValue(self, address, swell):
        return self.sendCommand(self.target, "V", chr(address + 48), "D", parameter="%.2f" % swell)

    def setHeaterNightSwellValue(self, address, swell):
        return self.sendCommand(self.target, "V", chr(address + 48), "N", parameter="%.2f" % swell)

    def setHeaterHystValue(self, address, swell):
        return self.sendCommand(self.target, "V", chr(address + 48), "H", parameter="%.2f" % swell)

    def setTimeBetweenBlocks(self, blockTime):
        return self.sendCommand(self.target, "R", "0", "B", parameter="%d" % blockTime)

    def setTimeBetweenSensors(self, repTime):
        return self.sendCommand(self.target, "R", "0", "S", parameter="%d" % repTime)

    def setWaitAfterLastSensor(self, waitTime):
        return self.sendCommand(self.target, "R", "0", "L", parameter="%d" % waitTime)


if __name__ == "__main__":
    import time

    test = Ventilsteuerung('CC', 'V2', comPort="/dev/board-1")
    print(test.setSecurityKey(secrets.SECURITY_LEVEL_DEVELOPMENT_KEY))
    print(test.getCompilationTime())
    print(test.getCompilationDate())
    for v in range(0, 2):
        print(test.getHeaterSetStatus(v))
        print(test.getHeaterActualStatus(v))
        print(test.getHeaterSwellValue(v))
        print(test.getHeaterNightSwellValue(v))
        print(test.getHeaterHystValue(v))
        print(test.setHeaterSetStatus(v, 'Auto'))
        print(test.setHeaterSwellValue(v, 22.4562))
        print(test.setHeaterNightSwellValue(v, 25.6354))
        print(test.setHeaterHystValue(v, 0.2))
    print(test.setTimeBetweenBlocks(3000))
    print(test.setTimeBetweenSensors(30))
    print(test.setWaitAfterLastSensor(100))
    print(test.getSerialNumber())
    time.sleep(0.5)
    # print(test.prepareBootload(secrets.BOOTLOADER_ATTENTION_KEY))
    # test.startBootload()
    # time.sleep(1)
    # test.writeFlash("/home/christof/Daten/Software/repositories/VentilSteuerung/bin/Release/VentilSteuerung.hex", "atxmega128a4u")

