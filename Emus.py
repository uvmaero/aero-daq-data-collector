# Peter Ferland 02.07.2019
# AERO Data Acquisition Project

# Purpose: Grab information off the CAN BUS, format it nicely and save it to a .csv file
# Information Sources: Rinehart Motor Controller, EMUS BMS, Temp Monitor Board
# Information Sources: Steering Position, Wheel Speed, Throttle Position, Brake Pressure, Damper Position

from Canpak import Canpak
import csv
from CanError import CanError
from CanDevice import CanDevice

class Emus(CanDevice):

    def __init__(self, filename, offset = 0, deviceName="Emus"):
        super().__init__(filename,offset,deviceName)
        # pre allocate a list of 80 elements to hold 80 cell voltages
        self.cellVoltages = [0] * 80
        self.voltageDict = {"cell_volt":self.cellVoltages}
        self.dataDict = {"UnderVoltage":0,\
                        "OverVoltage":0,\
                        "DischargeOverCurrent":0,\
                        "ChargeOverCurrent":0,\
                        "CellModuleOverheat":0,\
                        "Leakage":0,\
                        "NoCellCommunication":0,\
                        "LowVoltage":0,\
                        "HighCurrent":0,\
                        "HighTemperature":0,\
                        "CellOverheat":0,\
                        "NoCurrentSensor":0,\
                        "PackUnderVoltage":0,\
                        "CellVoltageValidity":0,\
                        "CellModuleTemperatureValidity":0,\
                        "CellBalanceRateValidity":0,\
                        "LiveCellCountValidity":0,\
                        "BatteryChargeFinished":0,\
                        "CellTemperatureValidity":0}
    
    # Purpose: Process Individual Cell Voltage Data From the EMUS
    # Input:
    #   data - byte array of hex data
    #   ID - CAN ID, used to determine which cell voltages to update
    def processVoltages(self,ID,data):

        if ID == "VG0":
            # Update cell voltage list for cells 0 - 7
            self.cellVoltages[0:7] = data
        if ID == "VG1":
            # Update cell voltage list for cells 8 - 15
            self.cellVoltages[8:15] = data
        if ID == "VG2":
            # Update cell voltage list for cells 16 - 23
            self.cellVoltages[16:23] = data
        if ID == "VG3":
            # Update cell voltage list for cells 24 - 31
            self.cellVoltages[24:31] = data
        if ID == "VG4":
            # Update cell voltage list for cells 32 - 39
            self.cellVoltages[32:39] = data
        if ID == "VG5":
           # Update cell voltage list for cells 48 - 55
            self.cellVoltages[48:55] = data
        if ID == "VG6":
            # Update cell voltage list for cells 56 - 63
            self.cellVoltages[56:63] = data
        if ID == "VG7":
            # Update cell voltage list for cells 64 - 71
            self.cellVoltages[64:71] = data
        if ID == "VG8":
            # Update cell voltage list for cells 72 - 79
            self.cellVoltages[72:79] = data
        # Return a dictionary containing cell voltages
        self.voltageDict["cell_volt"] = self.cellVoltages

    # Purpose: Process Individual Cell Voltage Data From the EMUS
    # Input:
    #   data - byte array of hex data (bytes 4-7 are unused)
    #   ID - CAN ID, used to determine which cell voltages to update
    def processFaults(self,data):
        # Protection Flags (LSB) (byte 0)
        # Bit 0 Cell Under Voltage - some cell is below critical minimum voltage
        self.dataDict["UnderVoltage"] = super().interpretFlags(data[0],0)
        # Bit 1 Cell Over Voltage - some cell is above critical maximum voltage
        self.dataDict["OverVoltage"] = super().interpretFlags(data[0],1)
        # Bit 2 Discharge OverCurrent - discharge current (negative current) exceeds max
        self.dataDict["DischargeOverCurrent"] = super().interpretFlags(data[0],2)
        # Bit 3 Charge OverCurrent - charge current (positive current) exceeds max
        self.dataDict["ChargeOverCurrent"] = super().interpretFlags(data[0],3)
        # Bit 4 Cell Module Overheat - cell module temperature exceeds maximum
        self.dataDict["CellModuleOverheat"] = super().interpretFlags(data[0],4)
        # Bit 5 Leakage - Leakage signal was detected on the leakage input pin
        self.dataDict["Leakage"] = super().interpretFlags(data[0],5)
        # Bit 6 No Cell Communication - Loss of communication to cells
        self.dataDict["NoCellCommunication"] = super().interpretFlags(data[0],6)
        
        # Warning (reduction) flags (byte 1)
        # Bit 0 Low Voltage - some cell is below low voltage warning setting
        self.dataDict["LowVoltage"] = super().interpretFlags(data[1],0)
        # Bit 1 High Current - discharge current (negative current) exceeds the current warning setting 
        self.dataDict["HighCurrent"] = super().interpretFlags(data[1],1)
        # Bit 2 High Temperature - Cell Module Tempreture Exceeds Warning Temperature Setting
        self.dataDict["HighTemperature"] = super().interpretFlags(data[1],2)

        # Protection flags (MSB) (byte 2)
        # Bits 0-2 and 4-7 are reserved!
        # Bit 3 Cell Overheat - Cell Temperature Exceeds Maximum Cell Temperature Threshold
        self.dataDict["CellOverheat"] = super().interpretFlags(data[2],3)
        # Bit 4 No Current Sensor
        self.dataDict["NoCurrentSensor"] = super().interpretFlags(data[2],4)
        # Bit 5 Pack Under Voltage
        self.dataDict["PackUnderVoltage"] = super().interpretFlags(data[2],5)

        # Battery Status Flags (byte 3)
        # Bit 0 Cell Voltages Validity - (1 if valid, 0 if invalid)
        self.dataDict["CellVoltageValidity"] = super().interpretFlags(data[3],0)
        # Bit 1 Cell Module Temperatures Validity
        self.dataDict["CellModuleTemperatureValidity"] = super().interpretFlags(data[3],1)
        # Bit 2 Cell Balancing Rate Validity
        self.dataDict["CellBalanceRateValidity"] = super().interpretFlags(data[3],2)
        # Bit 3 Number of Live Cells Validity
        self.dataDict["LiveCellCountValidity"] = super().interpretFlags(data[3],3)
        # Bit 4 Battery Charging Finished, Used only when using a non-CAN charger
        self.dataDict["BatteryChargeFinished"] = super().interpretFlags(data[3],4)
        # Bit 5 Cell Temperatures Validity
        self.dataDict["CellTemperatureValidity"] =super().interpretFlags(data[3],5)

    # Purpose: Determine which message was sent by the rinehart, perform appropriate data processing
    # and return the updated emus data dictionaries
    # Input: Frame - A tuple containing 3 hex values (ID,DLC,DATA)
    # Output: dataList - a dictionary of dictionaries of the following format

    # {"rinehart":{"DataID1": DataValue1, "DataID2": DataValue2, ...}}
    def checkBroadcast(self,frame):
        # check if the data supplied is a rinehart message, if so continue processing
        # if the message is from the rinehart chk will be a tuple with the format
        # chk = (ID,DATA)
        processedData = super().process(frame)
        # if process returns a boolean we know this isn't rinehart data, exit without returning data
        if isinstance(processedData, bool):
            return self.dataDict,self.voltageDict
        
        if processedData[0] == "DC":
            self.processFaults(processedData[1])
            return self.dataDict,self.voltageDict
        
        if "VG0" or "VG1" or "VG1" or "VG2" or "VG3" or "VG4" or "VG5" or "VG6" or "VG7" or "VG8" in processedData[0]:
            self.processVoltages(processedData[0],processedData[1])
            return self.dataDict,self.voltageDict

