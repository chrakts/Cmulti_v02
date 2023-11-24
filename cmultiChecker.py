import cmulti
import datetime
import codecs

cm = cmulti.CMULTI("CP", "/dev/ttyUSB0")

while True:
    message = cm._readline()
    try:
        text = message.decode('ascii', 'backslashreplace')
    except:
        text = message.decode('utf-8', "ignore").replace('^M', '\n\r') + "++++"
    with codecs.open("test.txt", "a", "utf-8") as myfile:
        myfile.write(datetime.datetime.now().ctime() + ' : ' + text)

