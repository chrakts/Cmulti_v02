import sys
sys.path.append("/home/christof/Daten/Software/repositories")

from Cmulti_v02.cmulti import CMULTI
import Secrets.secrets as secrets


class Ventilsteuerung(CMULTI):
  def __init__(self, source, target, comPort="", baudRate=57600, backChannel="TLog", withCrc=True, timeout=5000):
    super(self.__class__, self).__init__(source, comPort, baudRate, backChannel, withCrc, timeout)
    self.target = target
    self.comPort = comPort


if __name__ == "__main__":
  import time
  test = Ventilsteuerung('CC', 'V1', comPort="/dev/RS485-1")
  print(test.setSecurityKey(secrets.SECURITY_LEVEL_DEVELOPMENT_KEY))
  time.sleep(0.5)
  print(test.prepareBootload(secrets.BOOTLOADER_ATTENTION_KEY))
  test.startBootload()
  time.sleep(1)
  test.writeFlash("/home/christof/Daten/Software/repositories/VentilSteuerung/bin/Release/VentilSteuerung.hex", "atxmega128a4u")

