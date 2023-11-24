import cmulti
import datetime
import codecs

cm = cmulti.CMULTI("CP", "/dev/ttyUSB0")

while True:
    message = cm._readline()
    text = message.decode('ascii', 'backslashreplace').encode().decode('utf-8')
    with codecs.open("test.txt", "a", "utf-8") as myfile:
        myfile.write(datetime.datetime.now().ctime() + ' : ' + text)

