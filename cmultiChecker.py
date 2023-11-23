import cmulti

cm = cmulti.CMULTI("CP", "/dev/ttyUSB0")

print(cm._readline().decode('utf-8'))
