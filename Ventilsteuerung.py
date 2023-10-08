import sys

sys.path.append("/home/christof/Daten/Software/repositories")

from Cmulti_v02.cmulti import CMULTI
import Secrets.secrets as secrets


class Ventilsteuerung(CMULTI):
    def __init__(self, source, target, comPort="", baudRate=57600, backChannel="TLog", withCrc=True, timeout=5000):
        super(self.__class__, self).__init__(source, comPort, baudRate, backChannel, withCrc, timeout)
        self.target = target
        self.comPort = comPort

    def getHeaterSetStatus(self, address):
        return (self.sendCommand(self.target, "V", chr(address+48), "s"))
    def setHeaterSetStatus(self, address, status):
        return (self.sendCommand(self.target, "V", chr(address+48), "S", parameter=status))
    def getHeaterActualStatus(self, address):
        return (self.sendCommand(self.target, "V", chr(address+48), "a"))
    def setHeaterSwellValue(self, address, swell):
        return self.sendCommand(self.target, "V", chr(address + 48), "D", parameter="%.2f" % swell)


if __name__ == "__main__":
    import time

    test = Ventilsteuerung('CC', 'V2', comPort="/dev/RS485-1")
    print(test.setSecurityKey(secrets.SECURITY_LEVEL_DEVELOPMENT_KEY))
    print(test.getCompilationTime())
    print(test.getCompilationDate())
    print(test.getHeaterSetStatus(5))
    print(test.getHeaterActualStatus(0))
    print(test.setHeaterSetStatus(1, 'ein'))
    print(test.setHeaterSwellValue(0, 30.4562))

    time.sleep(0.5)
    # print(test.prepareBootload(secrets.BOOTLOADER_ATTENTION_KEY))
    # test.startBootload()
    # time.sleep(1)
    # test.writeFlash("/home/christof/Daten/Software/repositories/VentilSteuerung/bin/Release/VentilSteuerung.hex", "atxmega128a4u")
