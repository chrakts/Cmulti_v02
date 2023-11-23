import cmulti
import datetime

cm = cmulti.CMULTI("CP", "/dev/ttyUSB0")

while True:
    message = cm._readline()
    try:
        text = message.decode('utf-8')
    except:
        text = message.decode('utf-8', "ignore")
    with open("test.txt", "a") as myfile:
        myfile.write(text)