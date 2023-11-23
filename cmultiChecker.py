import cmulti

cm = cmulti.CMULTI("CP", "/dev/ttyUSB0")

while True:
    message = cm._readline()
    try:
        text = message.decode('utf-8')
    except:
        text = message
    with open("test.txt", "a") as myfile:
        myfile.write(text)