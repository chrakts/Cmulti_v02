import cmulti

cm = cmulti.CMULTI("CP", "/dev/ttyUSB0")

message = cm._readline()
try:
    print(message.decode('utf-8'))
except:
    print(message)
