# This is a motor object used by the Rinehart class to keep track of the state of the motor
class Motor(object):
    def __init__(self):
        self.motorEnable = False
        self.motorRunning = False

    def getMotorStatus()