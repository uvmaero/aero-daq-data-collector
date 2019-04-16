import serial

class LiveData:
    def __init__(self, ser):
        self.ser = ser
    
    def sendLivePacket(self, type, value):
        print(f'{type} {value}')
        self.ser.write(bytearray(f'{type} {value}\r\n', 'utf-8'))

class LivePacketType:
    CURRENT = "current"
    PITCH = "pitch"
