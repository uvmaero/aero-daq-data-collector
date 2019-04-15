# Peter Ferland 02.07.2019
# AERO Data Acquisition Project

# Purpose: Grab information off the CAN BUS, format it nicely and save it to a .csv file
# Information Sources: Rinehart Motor Controller, EMUS BMS, Temp Monitor Board
# Information Sources: Steering Position, Wheel Speed, Throttle Position, Brake Pressure, Damper Position

from Canpak import Canpak
import csv
from CanError import CanError
from CanDevice import CanDevice

class Pedalboard(CanDevice):

    def __init__(self, filename, offset, deviceName="Pedal"):
        super().__init__(filename,offset,deviceName)
        # pre allocate a list of 80 elements to hold 80 cell voltages
        self.dataDict = {"pedal0":0,\
                        "pedal1":0,\
                        "brake0":0,\
                        "brake1":0,\
                        "steer":0}
    
    # Purpose: Process Individual Cell Voltage Data From the EMUS
    # Input:
    #   data - byte array of hex data (bytes 5-7 are unused)
    #   ID - CAN ID, used to determine which cell voltages to update
    def processData(self,data):
        # Protection Flags (LSB) (byte 0)
        # Byte 0 is left wheel speed data
        self.dataDict["pedal0"] = data[0] * (1/255)
        # Byte 1 is right wheel speed data
        self.dataDict["pedal1"] = data[1] * (1/255)
        # Byte 2 is left damper data
        self.dataDict["brake0"] = data[2] * (1/255)
        # Byte 3 is right damper data
        self.dataDict["brake1"] = data[3] * (1/255)
        # Byte 4 is right damper data
        self.dataDict["steer"] = (data[4] - 127) * (180/255)

    # Purpose: Determine which message was sent by the rinehart, perform appropriate data processing
    # and return the updated emus data dictionaries
    # Input: Frame - A tuple containing 3 hex values (ID,DLC,DATA)
    # Output: dataList - a dictionary of dictionaries of the following format

    # {"rinehart":{"DataID1": DataValue1, "DataID2": DataValue2, ...}}
    def checkBroadcast(self,frame):
        # check if the data supplied is a Daqboard message, if so continue processing
        processedData = super().process(frame)
        # if process returns a boolean we know this isn't rinehart data, exit without returning data
        if isinstance(processedData, bool):
            return self.dataDict
        
        if processedData[0] == "DATA":
            self.processData(processedData[1])
            return self.dataDict