# Peter Ferland 02.07.2019
# AERO Data Acquisition Project

# Purpose: Grab information off the CAN BUS, format it nicely and save it to a .csv file
# Information Sources: Rinehart Motor Controller, EMUS BMS, Temp Monitor Board
# Information Sources: Steering Position, Wheel Speed, Throttle Position, Brake Pressure, Damper Position

from Canpak import Canpak
import csv
from CanError import CanError
from CanDevice import CanDevice

class Tempmonitor(CanDevice):

    def __init__(self, filename, offset = 0):
        super().__init__(filename,offset)
        self.cellTemps = [0] * 80
        self.tempDict = {"cell_temp":self.cellTemps}
        # pre allocate a list of 80 elements to hold 80 cell voltages
        self.dataDict = {"overtemp1":0,\
                        "overtemp2":0}
    
    # Purpose: Process Individual Cell Voltage Data From the EMUS
    # bytes 0-3 contain info on max and min temperature, this will be ignored
    # byte 4 contains fault information
    # Input:
    #   data - byte array of hex data (bytes 4-7 are unused)
    #   ID - CAN ID, used to determine which cell voltages to update
    def processStatus(self,ID,data):
        # Protection Flags (LSB) (byte 0)
        # Byte 0 is left wheel speed data
        if ID == "S1":
            self.dataDict["overtemp1"] = super().interpretFlags(data[4],0)
        if ID == "S2":
            self.dataDict["overtemp2"] = super().interpretFlags(data[4],0)

    def processTemps(self,ID,data):
        if ID == "T0":
            self.cellTemps[0] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[1] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[2] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[3] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T1":
            self.cellTemps[4] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[5] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[6] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[7] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T2":
            self.cellTemps[8] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[9] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[10] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[11] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T3":
            self.cellTemps[12] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[13] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[14] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[15] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T4":
            self.cellTemps[16] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[17] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[18] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[19] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T5":
            self.cellTemps[20] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[21] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[22] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[23] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T6":
            self.cellTemps[24] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[25] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[26] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[27] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T7":
            self.cellTemps[28] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[29] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[30] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[31] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T8":
            self.cellTemps[32] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[33] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[34] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[35] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T9":
            self.cellTemps[36] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[37] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[38] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[39] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T10":
            self.cellTemps[40] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[41] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[42] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[43] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T11":
            self.cellTemps[44] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[45] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[46] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[47] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T12":
            self.cellTemps[48] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[49] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[50] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[51] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T13":
            self.cellTemps[52] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[53] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[54] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[55] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T14":
            self.cellTemps[56] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[57] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[58] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[59] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T15":
            self.cellTemps[60] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[61] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[62] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[63] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T16":
            self.cellTemps[64] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[65] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[66] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[67] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T17":
            self.cellTemps[68] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[69] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[70] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[71] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T18":
            self.cellTemps[72] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[73] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[74] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[75] = super().concatBytes(data[6],data[7]) / 100
        if ID == "T19":
            self.cellTemps[76] = super().concatBytes(data[0],data[1]) / 100
            self.cellTemps[77] = super().concatBytes(data[2],data[3]) / 100
            self.cellTemps[78] = super().concatBytes(data[4],data[5]) / 100
            self.cellTemps[79] = super().concatBytes(data[6],data[7]) / 100
        self.tempDict["cell_temp"] = self.cellTemps

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
            return self.dataDict,self.tempDict
        
        if "S1" or "S2" in processedData[0]:
            self.processStatus(processedData[0],processedData[1])
            return self.dataDict,self.tempDict

        if "T0" or "T1" or "T2" or "T3" or "T4" or "T5" or "T6" or "T7" or "T8" or "T9" or "T10" or "T11" or "T12" or "T13" or "T14" or "T15" or "T16" or "T17" or "T18" or "T19"  in processedData[0]:
            self.processTemps(processedData[0],processedData[1])
            return self.dataDict,self.tempDict