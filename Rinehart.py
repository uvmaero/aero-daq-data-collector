# Peter Ferland 02.07.2019
# AERO Data Acquisition Project

# Purpose: Grab information off the CAN BUS, format it nicely and save it to a .csv file
# Information Sources: Rinehart Motor Controller, EMUS BMS, Temp Monitor Board
# Information Sources: Steering Position, Wheel Speed, Throttle Position, Brake Pressure, Damper Position

from canpak import Canpak
import csv
from RinehartError import RinehartError
from CanDevice import CanDevice


class Rinehart(CanDevice):
    # Inputs:
    #   filename - the name of a csv file containing a list of 11-bit CAN addresses
    #   and address id tags which are strings which identify the CAN data ex)
    #   0x0A0,T1
    #   0x0A1,T2
    #   0x0A2,T3
    #   0x0A3,AIV ... and so on
    #   Offset - a decimal value describing the CAN offset applied 
    # Outputs:
    #   addressBook - used to parse data
    def __init__(self, filename, offset=160, deviceName="Rinehart"):
        # 
        super().__init__(filename,offset,deviceName)
        # Initialize a dictionary to be used to return all data at once
        # TODO 03/19/18: Make a dictionary builder function which uses a csv file
        # to define the dictionary keys
        self.dataDict = {"IGBT_PhaseA_Temp":0,\
                        "IGBT_PhaseB_Temp":0,\
                        "IGBT_PhaseC_Temp":0,\
                        "Gate_Driver_Temp":0,\
                        "Control_Board_Temp":0,\
                        "RTD_Input1_Temp":0,\
                        "RTD_Input2_Temp":0,\
                        "RTD_Input3_Temp":0,\
                        "RTD_Input4_Temp":0,\
                        "RTD_Input5_Temp":0,\
                        "Motor_Temp":0,\
                        "Torque_Shudder":0,\
                        "AIV1":0,\
                        "AIV2":0,\
                        "AIV3":0,\
                        "AIV4":0,\
                        "Forward_Switch":0,\
                        "Reverse_Switch":0,\
                        "Brake_Switch":0,\
                        "Regen_Disable":0,\
                        "Ignition_Switch":0,\
                        "Start_Switch":0,\
                        "DIS7":0,\
                        "DIS8":0,\
                        "Electrical_Angle":0,\
                        "Motor_Speed":0,\
                        "Electrical_Frequency":0,\
                        "Delta_Resolver":0,\
                        "Phase_A_Current":0,\
                        "Phase_B_Current":0,\
                        "Phase_C_Current":0,\
                        "DC_Bus_Current":0,\
                        "DC_Bus_Voltage":0,\
                        "Output_Voltage":0,\
                        "VAB_Vd_Voltage":0,\
                        "VAB_Vq_Voltage":0,\
                        "Flux_Command":0,\
                        "Flux_Feedback":0,\
                        "Id_Current":0,\
                        "Iq_Current":0,\
                        "Ref_Voltage_15":0,\
                        "Ref_Voltage_25":0,\
                        "Ref_Voltage_50":0,\
                        "Ref_Voltage_12":0,\
                        "VSM_State":0,\
                        "Inverter_State":0,\
                        "Relay_State":0,\
                        "Inverter_Run_Mode":0,\
                        "Inverter_Active_Discharge":0,\
                        "Inverter_Command_Mode":0,\
                        "Inverter_Enable_State":0,\
                        "Inverter_Enable_Lockout":0,\
                        "Direction_Command":0,\
                        "BMS_Active":0,\
                        "BMS_Limiting":0,\
                        "Post_Fault_Lo":0,\
                        "Post_Fault_Hi":0,\
                        "Run_Fault_Lo":0,\
                        "Run_Fault_Hi":0,\
                        "Commanded_Torque":0,\
                        "Torque_Feedback":0,\
                        "Power_on_Timer":0,\
                        "Modulation_Index":0,\
                        "Flux_Weakening_Output":0,\
                        "Id_Command":0,\
                        "Iq_Command":0}
   
    
    # Purpose: Create and return a CAN packet to operate the Rinehart
    # Input:
    # Output: A CAN frame ready for transmission
    def heartbeat(self):
        port = '/dev/ttyACM0'
        canId = 0xC0   #CAN ID to send a Command Message
        data = 0x0000000000000000 # ALL ZEROS FOR HEARTBEAT
        dlc = 0x8
        beat = Canpak(port,canId,data,dlc)
        beat.send()

    

    # Purpose: process boolean data from the rinehart, certain rinehart flags use an 
    # entire byte to encode 1 bit of information, this code is intended to process such
    # flags. Not All flags are handled in this wasteful manner, but some are.
    # Input:
    #   data - 1 byte of data, either 00000000 or 00000001
    # Output: A boolean
    def processBool(self,data):
        if data == 0:
            return False
        elif data == 1:
            return True
        else:
            raise RinehartError('processBool Error, input %s isnt a boolean' % data)

    # Purpose: Process temperature data from a CAN frame. Determine which temperature 
    # set the data originates from (temps 1,2,or3) and return a an appropriate dictionary
    # of values
    # Input: data - byte array of hex data
    # Output: a dictionary containing an ID tag and its value
    def processTemps(self,ID,data):
        
        if ID == "T1":
            # Byte 0,1 is IGBT Phase A temperature -3276.8 to +3276.7 Celsius
            # concatenate byte 0 and byte 1 data
            IGBT_PhaseA_Temp = super().concatBytes(data[0],data[1]) / 10
        
            # Byte 2,3 is IGBT Phase B temperature -3276.8 to +3276.7 Celsius
            IGBT_PhaseB_Temp = super().concatBytes(data[2],data[3]) / 10

            # Byte 4,5 is IGBT Phase C temperature -3276.8 to +3276.7 Celsius
            IGBT_PhaseC_Temp = super().concatBytes(data[4],data[5]) / 10

            # Byte 6,7 is Gate Driver Board temperature -3276.8 to +3276.7 Celsius
            Gate_Driver_Temp = super().concatBytes(data[6],data[7]) / 10

            # Update the values of the following keys of the rinehart data dictionary 
            self.dataDict["IGBT_PhaseA_Temp"] = IGBT_PhaseA_Temp
            self.dataDict["IGBT_PhaseB_Temp"] = IGBT_PhaseB_Temp
            self.dataDict["IGBT_PhaseC_Temp"] = IGBT_PhaseC_Temp
            self.dataDict["Gate_Driver_Temp"] = Gate_Driver_Temp

        elif ID == "T2":
            # Byte 0,1 is Control Board Temperature -3276.8 to +3276.7 Celsius
            Control_Board_Temp = super().concatBytes(data[0],data[1]) / 10

            # Byte 2,3 is RTD input 1 temperature -3276.8 to +3276.7 Celsius
            RTD_Input1_Temp = super().concatBytes(data[2],data[3]) / 10

            # Byte 4,5 is RTD input 2 temperature -3276.8 to +3276.7 Celsius
            RTD_Input2_Temp = super().concatBytes(data[4],data[5]) / 10

            # Byte 6,7 is RTD input 3 temperature -3276.8 to +3276.7 Celsius
            RTD_Input3_Temp = super().concatBytes(data[6],data[7]) / 10

            # Update the values of the following keys of the rinehart data dictionary 
            self.dataDict["Control_Board_Temp"] = Control_Board_Temp
            self.dataDict["RTD_Input1_Temp"] = RTD_Input1_Temp
            self.dataDict["RTD_Input2_Temp"] = RTD_Input2_Temp
            self.dataDict["RTD_Input3_Temp"] = RTD_Input3_Temp

        elif ID == "T3":
            # Byte 0,1 is RTD input 4 temperature -3276.8 to +3276.7 Celsius
            RTD_Input4_Temp = super().concatBytes(data[0],data[1]) / 10

            # Byte 2,3 is RTD input 5 temperature -3276.8 to +3276.7 Celsius
            RTD_Input5_Temp = super().concatBytes(data[2],data[3]) / 10

            # Byte 4,5 is Motor Temperature -3276.8 to +3276.7 Celsius
            Motor_Temp = super().concatBytes(data[4],data[5]) / 10

            # Byte 6,7 is Torque used in shudder compensation -3276.8 to +3276.7 N-m
            Torque_Shudder = super().concatBytes(data[6],data[7]) / 10

            # Update the values of the following keys of the rinehart data dictionary
            self.dataDict["RTD_Input4_Temp"] = RTD_Input4_Temp
            self.dataDict["RTD_Input5_Temp"] = RTD_Input5_Temp
            self.dataDict["Motor_Temp"] = Motor_Temp
            self.dataDict["Torque_Shudder"] = Torque_Shudder

    # Process Analog Input Voltages
    def processAIV(self,data):
        # Byte 0,1 AIV #1 -327.68 to +327.67 volts
        AIV1 = super().concatBytes(data[0],data[1]) / 100
        # Byte 2,3 AIV #2 -327.68 to +327.67 volts
        AIV2 = super().concatBytes(data[2],data[3]) / 100
        # Byte 4,5 AIV #3 -327.68 to +327.67 volts
        AIV3 = super().concatBytes(data[4],data[5]) / 100
        # Byte 6,7 AIV #4 -327.68 to +327.67 volts
        AIV4 = super().concatBytes(data[6],data[7]) / 100
        # Update the values of the following keys of the rinehart data dictionary
        self.dataDict["AIV1"] = AIV1
        self.dataDict["AIV2"] = AIV2
        self.dataDict["AIV3"] = AIV3
        self.dataDict["AIV4"] = AIV4

    # Process Digital Input Status
    # Digital Input Status are represented as a boolean (unsigned byte)
    # 0 = false/off, 1 = true/on
    # yes that is pretty wasteful to encode 1 bit of data inside of a byte
    # this is just how the rinehart does this.
    def processDIS(self,data):
        # Byte 0 Digital Input 1 (boolean, unsigned byte) forward switch 
        Forward_Switch = self.processBool(data[0])
        # Byte 1 Digital Input 2 (boolean, unsigned byte) reverse switch
        Reverse_Switch = self.processBool(data[1])
        # Byte 2 Digital Input 3 (boolean, unsigned byte) brake switch
        Brake_Switch = self.processBool(data[2])
        # Byte 3 Digital Input 4 (boolean, unsigned byte) Regen Disable Switch
        Regen_Disable = self.processBool(data[3])
        # Byte 4 Digital Input 5 (boolean, unsigned byte) Ignition switch
        Ignition_Switch = self.processBool(data[4])
        # Byte 5 Digital Input 6 (boolean, unsigned byte) Start Switch
        Start_Switch = self.processBool(data[5])
        # Byte 6 Digital Input 7 (boolean, unsigned byte)
        DIS7 = self.processBool(data[6])
        # Byte 7 Digital Input 8 (boolean, unsigned byte)
        DIS8 = self.processBool(data[7])
        # Update the values of the following keys of the rinehart data dictionary
        self.dataDict["Forward_Switch"] = Forward_Switch
        self.dataDict["Reverse_Switch"] = Reverse_Switch
        self.dataDict["Brake_Switch"] = Brake_Switch
        self.dataDict["Regen_Disable"] = Regen_Disable
        self.dataDict["Ignition_Switch"] = Ignition_Switch
        self.dataDict["Start_Switch"] = Start_Switch
        self.dataDict["DIS7"] = DIS7
        self.dataDict["DIS8"] = DIS8
    
    # Process Motor Position Information
    def processMPI(self,data):
        # Byte 0,1 Motor Electrical (Angle) 0.0 to +/-359.9 degrees
        Electrial_Angle = super().concatBytes(data[0],data[1]) / 10
        # Byte 2,3 Motor Speed (Angular Velocity) -32768 to +32767 RPM
        Motor_Speed = super().concatBytes(data[2],data[3])
        # Byte 4,5 Electrical Output Frequency (Frequency) -3276.8 to +3726.7
        Electrical_Frequency = super().concatBytes(data[4],data[5]) / 10
        # Byte 6,7 Delta Resolver Filtered (Angle) +/- 180 degrees
        Delta_Resolver = super().concatBytes(data[6],data[7]) / 10
        # Update the values of the following keys of the rinehart data dictionary
        self.dataDict["Electrical_Angle"] = Electrial_Angle
        self.dataDict["Motor_Speed"] = Motor_Speed
        self.dataDict["Electrical_Frequency"] = Electrical_Frequency
        self.dataDict["Delta_Resolver"] = Delta_Resolver
    
    # Process Motor electrical current information
    def processCI(self,data):
        # Byte 0,1 Phase A current (current) -3276.8 to +3276.7 amps
        Phase_A_Current = super().concatBytes(data[0],data[1]) / 10
        # Byte 2,3 Phase B current (current) -3276.8 to +3276.7 amps
        Phase_B_Current = super().concatBytes(data[2],data[3]) / 10
        # Byte 4,5 Phase C current (current) -3276.8 to +3276.7 amps
        Phase_C_Current = super().concatBytes(data[4],data[5]) / 10
        # Byte 6,7 DC Bus current (current) -3276.8 to +3276.7 amps
        DC_Bus_Current = super().concatBytes(data[6],data[7]) / 10
        # Update the values of the following keys of the rinehart data dictionary
        self.dataDict["Phase_A_Current"] = Phase_A_Current
        self.dataDict["Phase_B_Current"] = Phase_B_Current
        self.dataDict["Phase_C_Current"] = Phase_C_Current
        self.dataDict["DC_Bus_Current"] = DC_Bus_Current

    # Process Motor Voltage Information
    def processVI(self,data):
        # Byte 0,1 DC Bus Voltage (High Voltage) -3276.8 to +3276.7 volts
        DC_Bus_Voltage = super().concatBytes(data[0],data[1]) / 10
        # Byte 2,3 Output Voltage (High Voltage) -3276.8 to +3276.7 volts
        Output_Voltage =  super().concatBytes(data[2],data[3]) / 10
        # Byte 4,5 VAB_Vd_Voltage (High Voltage) -3276.8 to +3276.7 volts
        VAB_Vd_Voltage = super().concatBytes(data[4],data[5]) / 10
        # Byte 6,7 VBC_Vq_Voltage (High Voltage) -3276.8 to +3276.7 volts
        VAB_Vq_Voltage = super().concatBytes(data[4],data[5]) / 10
        # Update the values of the following keys of the rinehart data dictionary
        self.dataDict["DC_Bus_Voltage"] = DC_Bus_Voltage
        self.dataDict["Output_Voltage"] = Output_Voltage
        self.dataDict["VAB_Vd_Voltage"] = VAB_Vd_Voltage
        self.dataDict["VAB_Vq_Voltage"] = VAB_Vq_Voltage
    # Process Flux Information
    def processFI(self,data):
        # Byte 0,1 Flux Command (Flux) -32.768 to 32.767 Webers
        Flux_Command = super().concatBytes(data[0],data[1]) / 1000
        # Byte 2,3 Flux Feedback (Flux)  -32.768 to 32.767 Webers
        Flux_Feedback = super().concatBytes(data[2],data[3]) / 1000
        # Byte 4,5 Id Feedback (Current) -3276.8 to +3276.7 amps
        Id_Current = super().concatBytes(data[4],data[5]) / 10
        # Byte 6,7 Iq Feedback (Current) -3276.8 to +3276.7 amps
        Iq_Current = super().concatBytes(data[6],data[7]) / 10
        # Update the values of the following keys of the rinehart data dictionary
        self.dataDict["Flux_Command"] = Flux_Command
        self.dataDict["Flux_Feedback"] = Flux_Feedback
        self.dataDict["Id_Current"] = Id_Current
        self.dataDict["Iq_Current"] = Iq_Current

    # Process Internal Voltages
    def processIV(self,data):
        # Byte 0,1 1.5V Reference Voltage (Low Voltage) -327.68 to +327.67 volts
        Ref_Voltage_15 = super().concatBytes(data[0],data[1]) / 100
        # Byte 2,3 2.5V Reference Voltage (Low Voltage) -327.68 to +327.67 volts
        Ref_Voltage_25 = super().concatBytes(data[2],data[3]) / 100
        # Byte 4,5 5.0V Reference Voltage (Low Voltage) -327.68 to +327.67 volts
        Ref_Voltage_50 = super().concatBytes(data[4],data[5]) / 100
        # Byte 6,7 12V System Voltage (Low Voltage) -327.68 to +327.67 volts
        Ref_Voltage_12 = super().concatBytes(data[6],data[7]) / 100
        # Update the values of the following keys of the rinehart data dictionary
        self.dataDict["Ref_Voltage_15"] = Ref_Voltage_15
        self.dataDict["Ref_Voltage_25"] = Ref_Voltage_25
        self.dataDict["Ref_Voltage_50"] = Ref_Voltage_50
        self.dataDict["Ref_Voltage_12"] = Ref_Voltage_12

    # Purpose: Check the Internal States, see the docs for this one
    def processIS(self,data):
        # Byte 0,1 VSM State
        VSM_State = super.concatBytes(data[0],data[1])
        # Byte 2 Inverter State
        Inverter_State = data[2]
        # Byte 3 Relay State
        Relay_State = data[3]
        # Byte 4 Bit(0) Inverter Run Mode
        Inverter_Run_Mode = int(data[4]) & 1
        # Byte 4 Bit(5-7) Inverter Active Discharge State
        Inverter_Active_Discharge = int(data[4]) & (111 << 5)
        # Byte 5 Inverter Command Mode
        Inverter_Command_Mode = data[5]
        # Byte 6 Bit(0) Inverter Enable State
        Inverter_Enable_State = int(data[6]) & 1
        # Byte 6 Bit(7) Inverter Enable Lockout
        Inverter_Enable_Lockout = int(data[6]) & (1 << 7)
        # Byte 7 Bit(0) Direction Command
        Direction_Command = int(data[7]) & 1
        # Byte 7 Bit(1) BMS Active
        BMS_Active = int(data[7]) & (1 << 1)
        # Byte 7 Bit(2) BMS Limiting Torque
        BMS_Limiting = int(data[7]) & (1 << 2)
        # Update the values of the following keys of the rinehart data dictionary
        self.dataDict["VSM_State"] = VSM_State
        self.dataDict["Inverter_State"] = Inverter_State
        self.dataDict["Relay_State"] = Relay_State
        self.dataDict["Inverter_Run_Mode"] = Inverter_Run_Mode
        self.dataDict["Inverter_Active_Discharge"] = Inverter_Active_Discharge
        self.dataDict["Inverter_Command_Mode"] = Inverter_Command_Mode
        self.dataDict["Inverter_Enable_State"] = Inverter_Enable_State
        self.dataDict["Inverter_Enable_Lockout"] = Inverter_Enable_Lockout
        self.dataDict["Direction_Command"] = Direction_Command
        self.dataDict["BMS_Active"] = BMS_Active
        self.dataDict["BMS_Limiting"] = BMS_Limiting
    # Purpose: Check Fault Codes
    def processFC(self,data):
        # Byte 0,1 POST Fault Lo
        Post_Fault_Lo = super().concatBytes(data[0],data[1])
        # Byte 2,3 POST Fault Hi
        Post_Fault_Hi = super().concatBytes(data[2],data[3])
        # Byte 4,5 Run Fault Lo
        Run_Fault_Lo = super().concatBytes(data[4],data[5])
        # Byte 6,7 Run Fault Hi
        Run_Fault_Hi = super().concatBytes(data[6],data[7])
        # Update the values of the following keys of the rinehart data dictionary
        self.dataDict["Post_Fault_Lo"] = Post_Fault_Lo
        self.dataDict["Post_Fault_Hi"] = Post_Fault_Hi
        self.dataDict["Run_Fault_Lo"] = Run_Fault_Lo
        self.dataDict["Run_Fault_Hi"] = Run_Fault_Hi
    
    # Purpose: Process torque and Timer information
    def processTT(self,data):
        # Byte 0,1 Commanded Torque (Torque) -3276.8 to +3276.7 N-m
        Commanded_Torque = super().concatBytes(data[0],data[1]) / 10
        # Byte 2,3 Torque Feedback (Torque) -3276.8 to +3276.7 N-m
        Torque_Feedback = super().concatBytes(data[2],data[3]) / 10
        # Byte 4,5,6,7 Power on Timer (Counts x .003) sec
        Power_on_Timer = super().concatBytes(data[4],data[5],data[6],data[7]) * .003
        # Update the values of the following keys of the rinehart data dictionary
        self.dataDict["Commanded_Torque"] = Commanded_Torque
        self.dataDict["Torque_Feedback"] = Torque_Feedback
        self.dataDict["Power_on_Timer"] = Power_on_Timer
    
    # Purpose: Process Modulation Index and Flux Weakining Output Information
    def processMIF(self,data):
        # Byte 0,1 Modulation Index (Per-Unit Value) (divide by 100, see docs)
        Modulation_Index = super().concatBytes(data[0],data[1]) / 100
        # Byte 2,3 Flux Weakening Output (Current) -3276.8 to +3276.7 amps
        Flux_Weakening_Output = super().concatBytes(data[2],data[3]) / 10
        # Byte 4,5 Id Command (Current) -3276.8 to +3276.7 amps
        Id_Command = super().concatBytes(data[4],data[5]) / 10
        # Byte 6,7 Iq Command (Current) -3276.8 to +3276.7 amps
        Iq_Command = super().concatBytes(data[6],data[7]) / 10
        # Update the values of the following keys of the rinehart data dictionary
        self.dataDict["Modulation_Index"] = Modulation_Index
        self.dataDict["Flux_Weakening_Output"] = Flux_Weakening_Output
        self.dataDict["Id_Command"] = Id_Command
        self.dataDict["Iq_Command"] = Iq_Command
    '''
    # Do Not Care Implement Later
    def processFIRM(self,data):
        # Byte 0,1 EEPROM Version / Project Code
        EEPROM_Version = super().concatBytes(data[0],data[1])
        # Byte 2,3 Software Version
        Software_Version = super().concatBytes(data[2],data[3])
        # Byte 4,5 Date Code (mmdd)
        Date_Code_mmdd = super().concatBytes(data[4],data[5])
        # Byte 6,7 Date Code (yyyy)
        Date_Code_yyyy = super().concatBytes(data[6],data[7])
        # Update the values of the following keys of the rinehart data dictionary
        return {"EEPROM_Version":EEPROM_Version,\
                "Software_Version":Software_Version,\
                "Date_Code_mmdd":Date_Code_mmdd,\
                "Date_Code_yyyy":Date_Code_yyyy} 
    
    # Do Not Care Implement Later
    def processDD(self,data):
        # Refer to the Manual, "Download Diagnostic Data for Details"
        return
    '''
    # Purpose: Determine which message was sent by the rinehart, perform appropriate data processing
    # and return a dictionary containing a data ID and its corresponding value
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
            return self.dataDict
        # If we get here then we know that the data is from the rinehart, so we will iterate over all
        # known message types to determine how to process the CAN data
        # processedData[0] is the message type that was sent, which is used to determine how to process the data
        # Process Temperature 1
        if "T1" or "T2" or "T3" in processedData[0]:
            # Pass the Bytearray of processed data to the temperature processing function
            self.processTemps(processedData[0],processedData[1])

        # Process Analog Input Voltages    
        elif processedData[0] == "AIV":
            self.processAIV(processedData[1])

        # Process Digital Input States
        elif processedData[0] == "DIS":
            self.processDIS(processedData[1])

        # Process Motor Position Information    
        elif processedData[0] == "MPI":
            self.processMPI(processedData[1])

        # Process Electrical Current Information    
        elif processedData[0] == "CI":
            self.processCI(processedData[1])

        # Process Voltage Information    
        elif processedData[0] == "VI":
            self.processVI(processedData[1])

        # Process Flux Information   
        elif processedData[0] == "FI":
            self.processFI(processedData[1])

        # Process Internal Voltages Information
        elif processedData[0] == "IV":
            self.processIV(processedData[1])

        # Process Internal State Code Information
        elif processedData[0] == "IS":
            self.processIS(processedData[1])

        # Process Fault Code Information
        elif processedData[0] == "FC":
            self.processFC(processedData[1])

        # Process Torque and Timer Information
        elif processedData[0] == "TT":
            self.processTT(processedData[1])

        # Process Modulation and Flux Information
        elif processedData[0] == "MIF":
            self.processMIF(processedData[1])

        return self.dataDict
       
    
    
       


