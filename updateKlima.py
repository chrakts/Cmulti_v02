import sys, os
import time

sys.path.append("/home/chrak/Daten/Software/repositories") 

from Cmulti_v02.cmulti import CMULTI
import Secrets.secrets as secrets
import Cmulti_v02.Klima as KLIMA


test = KLIMA.Klima('CC','C1',comPort="/dev/ttyUSB0")
print( test.setSecurityKey(secrets.SECURITY_LEVEL_DEVELOPMENT_KEY) )
time.sleep(0.2) 
print( test.prepareBootload(secrets.BOOTLOADER_ATTENTION_KEY) )
time.sleep(0.2) 
print( test.startBootload() )
time.sleep(1) 
test.close()
os.system("avrdude -v  -c avr109 -p x32a4u -P /dev/ttyUSB0 -b 115200 -U flash:'w:/home/chrak/Daten/Software/repositories/Klimastation/bin/Release/Klimastation.hex':i  -D")




