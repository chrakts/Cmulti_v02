from PyCRC.CRCCCITT import CRCCCITT
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import yaml
import serial


class cmulti_crc_constants_t(object):
    noCRC = 0
    CRC_8 = 1
    CRC_16 = 2
    CRC_32 = 3
    CRC_ccitt_1d0f = 4
    CRC_ccitt_ffff = 5
    CRC_dnp = 6
    CRC_kermit = 7
    CRC_modbus = 8
    CRC_sick = 9
    CRC_xmodem = 10

    def __init__(self):
        pass


class CMULTI(object):
    def __init__(self, source, comPort="", baudRate=57600, backChannel="Klima", withCrc=True, timeout=1000):
        if comPort.lower() != "mqtt":
            self.interface = serial.Serial(comPort, baudRate, timeout=timeout)
        else:
            self.interface = "mqtt"

            path = "/home/christof/Daten/Software/repositories/bridges"
            with open(path + '/config.yaml') as f:
                self.dataMap = yaml.safe_load(f)

            self.auth = {'username': self.dataMap["mqtt"]["user"], 'password': self.dataMap["mqtt"]["password"]}

        if withCrc is True:
            self.crc = cmulti_crc_constants_t.CRC_xmodem
        else:
            self.crc = cmulti_crc_constants_t.noCRC
        self.source = source
        self.backChannel = backChannel
        self.timeout = timeout
        self.gotAnswer = False

    def sendStandard(self, text, target, function, address, job, dataType, expectAnswer=True):
        if type(self.interface) != str:
            return self.sendStandard_tty(text, target, function, address, job, dataType, expectAnswer)
        else:
            return self.sendStandard_mqtt(text, target, function, address, job, dataType, expectAnswer)

    def sendStandard_tty(self, text, target, function, address, job, dataType, expectAnswer=True):
        # Mqtt/Quelle/Function/Address/Job/Target/Datatype
        # 0    1      2        3       4   5      6
        # 10DCQCPSC0l?510e
        # 11DCPCQA719<b570

        st = 'D' + target + self.source + 'S' + function + address + job + dataType + text
        if dataType != '?':
            st = st + '<'
        l = len(st) + 6
        st = "#%02x" % l + st
        crcString = ("%04x" % (CRCCCITT().calculate(st)))
        st = st + crcString + "\r\n"
        print(st)
        self.outputTTY(st)
        if expectAnswer:
            result, resultBool, resultCRC, inTime = self.input()
            return resultBool, result

    def sendStandard_mqtt(self, text, target, function, address, job, dataType, expectAnswer=True):
        # Mqtt/DT/d/1/d/BR/T
        publish.single("Mqtt/%s/%s/%s/%s/%s/%s/" % (self.source, function, address, job, target, dataType),
                       payload=str(text),
                       hostname=self.dataMap["mqtt"]["serverIP"],
                       auth=self.auth)
        if expectAnswer:
            msg = subscribe.simple("Answer/%s/#" % target, qos=0, msg_count=1,
                                   hostname=self.dataMap["mqtt"]["serverIP"], port=1883, keepalive=60, auth=self.auth)
            # print("%s %s" % (msg.topic, msg.payload))
            if msg.topic.split('/')[-1] != 'true':
                ret = False
            else:
                ret = True
            return msg.payload.decode('utf-8'), ret

    def sendCommand(self, target, function, address, job, parameter="", expectAnswer=True):
        if len(parameter) == 0:
            return self.sendStandard(parameter, target, function, address, job, "?", expectAnswer)
        else:
            return self.sendStandard(parameter, target, function, address, job, "T", expectAnswer)

    def outputTTY(self, text):
        towrite = text
        self.interface.write(towrite.encode('ascii'))

    def _readline(self):
        eol = b'\r'
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self.interface.read(1)
            if c:
                line += c
                if line[-leneol:] == eol:
                    break
            else:
                break
        return bytes(line)

    """
    #10DC1CCSS0C?05ad
    #24DCCC1rS0CTcommand not allowed<5bd7
    #1fDC1CCSS0KTD=&27ane%24dez<16cb
    #12DCCC1RS0KT2<edc5
    #10DC1CCSS0C?05ad
    #1cDCCC1RS0CTDec 23 2020<3682
    #12DBRDTSFKoT0<31b2
    #10DC1CCSS0T?9f49
    #19DCCC1RS0TT21:41:14<c9d6
    #10DC1CCSS0m?2044
    #15DCCC1RS0mT2778<8944
    #16DC1CCST0BT12000<b008
    #16DCCC1RT0BT12000<6c5e
    #15DC1CCST0WT1000<be44
    #15DCCC1RT0WT1000<21ea
    """
    def input(self):
        inTime = True
        hello = self._readline().decode('utf-8')
        if len(hello) == 0:
            return "", False, False, False
        crcState = True
        crcString = ""
        if hello[0] != '<':
            print("!! start character error")
        if hello[-1] != '>':
            print("!! end character error")
        if self.crc != cmulti_crc_constants_t.noCRC:
            crcString = hello[-5:-1]
            signString = hello[-6:-5]
            answerString = hello[1:-5]
            if crcString == ("%04x" % (CRCCCITT().calculate(answerString))):
                crcState = True
            else:
                crcState = False
                print("!! CRC error")
            answerString = answerString[0:-1]  # das sign abtrennen
        else:
            answerString = hello[1:-2]
            signString = hello[-2:-1]
        if signString == '.':
            return answerString, True, crcState, inTime
        elif signString == '!':
            return answerString, False, crcState, inTime
        else:
            print("!! sign character error")
            return answerString, False, crcState, inTime

    def answer_handler(self, channel, data):
        self.msganswer = cmulti_answer_t.decode(data)
        self.gotAnswer = True

    def close(self):
        if type(self.interface) != str:
            self.interface.close()
