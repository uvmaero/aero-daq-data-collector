# Peter Ferland 02.07.2019
# AERO Data Acquisition Project

# Purpose: Grab information off the CAN BUS, format it nicely and save it to a .csv file
# Information Sources: Rinehart Motor Controller, EMUS BMS, Temp Monitor Board
# Information Sources: Steering Position, Wheel Speed, Throttle Position, Brake Pressure, Damper Position

from enum import Enum, auto
import canpak
import csv
import RinehartError


class Rinehart(object):
    # Inputs:
    # Offset - a decimal value describing the CAN offset applied, default is 160
    # filename - the filename of a csv file containing a list of CAN addresses
    def __init__(self, filename, Offset=160):
        # Offset is a decimal value which describes the CAN offset applied, (Default is 160)
        self.Offset = Offset
        # Create a tuple of data acquisition related CAN addresses from the csvAddress file
        self.daqAddress = readAddress("filename")

        # Describes whether the motor is enabled or not, default is boolean false
        #self.motorEnable = False
        # Can Bitrate, default is 250 kbps, we will set this to 1 Mbps
        #self.canBitrate = Bitrate 
    
    # Purpose: create a can address for a CAN packet intended for the Rinehart Motor Controller
    # The Rinehart Motor Controller defines its CAN addresses in the spec sheet using an offset
    # and a relative address. The offset is 0x0A0 (160 in decimal) by default but can be adjusted 
    # to any value in the range of 0x000 to 0x7C0 (0 - 1984 in decimal). The relative addresses 
    # are a contiguous range of values in the range of 1 - 400 (decimal).
    # Inputs: (addr_off) Address Offset (A decimal int), (addr) Relative Address (A decimal int)
    # Output: A 3 digit hex string with the corresponding  
    def canAddr(addr):
        try:
            if len(str(addr)) > 3 | len(str(addr_off)):
                
            elif :

            else:
                return format(addr+addr_off,'03X')
        except:

    '''
    # Purpose: Create and return a CAN packet to operate the Rinehart
    # Input:
    # Output: A CAN frame ready for transmission
    def command():
        canId = 0x0C0   #CAN ID to send a Command Message
    '''

    # Purpose: Check if a received CAN frame originates from the rinehart
    # Input: Frame - A tuple containing 3 hex values (ID,DLC,DATA)
    # Output: A boolean - True = The CAN frame is believed to be sent by the rinehart 
    def process(frame):
        # Check if the object passed in is indeed a tuple
        if isinstance(frame, tuple):
            if tuple[0] in self.daqAddress:
                return True
            else:
                return False
        else:
            raise RinehartError("Cannot process " + str(frame) + "is not a tuple!")

    # Purpose: Check the CAN Status Register, this is updated every 3ms
    # CAN Status Word: 0x0001 = Transmit Mode (TM), 1 = CAN TX active, 0 = CAN TX inactive
    # CAN Status Word: 0x0002 = Received Mode (RM)
    # CAN Status Word: 0x0004 = Power Down Acknowledge
    # CAN Status Word: 0x0008 = Change Configuration Enable
    # CAN Status Word: 0x0010 = Suspend Mode Acknowledge
    # CAN Status Word: 0x0020 = Warning Status (EW) 1 = One of the two error counters CANREC or 
    #                           CANTEC has reached the warning level of 96
    # CAN Status Word: 0x0040 = Error Passive 1 = CAN module is in error-passive mode. CANTEC has
    #                           reached 128
    # CAN Status Word: 0x0080 = Buss Off (BO) 1 = There is an abnormal rate of errors on the CAN 
    #                           Bus (CANTEC = 256). During Bus Off no messages can be received or 
    #                           Transmitted. Bus-off state can be exited by clearing the CCR bit 
    #                           in the CANMC register or if the Auto Bus On (ABO) (CANMC.7) bit is
    #                           set after 128 * 11 receive bits have been received. After leaving 
    #                           bus off, the errors are cleared
    def checkStatus():

    # Purpose: Check the CAN Faults Register for faults
    # Input: None
    # Output: An Array containing all fault codes reported by the Rinehart, if no codes are present
    # then an empty Array is Returned
    # CAN Faults Word: 0x01 = Acknowledge Error 1 = The CAN module received no acknowledge
    # CAN Faults Word: 0x02 = Stuff Error 1 = A stuff bit error occurred, (see CAN standard)
    # CAN Faults Word: 0x04 = Cyclic Redundancy Check Error 1 = CAN received a wrong CRC
    # CAN Faults Word: 0x08 = Stuck at Dominant 1 Error (see CAN docs for rinehart)
    # CAN Faults Word: 0x10 = Bit Error 1 = Bit Error Detected
    # CAN Faults Word: 0x20 = Form Error 1 = A form error occurred (improper formation of CAN frame)
    def checkFaults():

    # Purpose: Read a csv file and create a tuple using its contents. Used during initialization to
    # create a list of relevant CAN addresses
    def readAddress(filename):
        try:
            with open(filename, newline='') as csvfile:
                # Make an empty list to hold data for the tuple
                address_book = []
                csvread = csv.reader(csvfile)
                # Read each line of the csv file & extract the address as an integer
                for line in csvread:
                    address_book.append(int(line[0],16))
                return tuple(address_book)
        except Exception as e:
            print(e.message,e.args)

    '''  # Implement later  
    # Purpose: Clear Faults from the Rinehart CAN Faults register, this is called by the checkFaults
    #          command if faults are present.  
    def clearFaults():

    '''
    '''    
    # Purpose: Clear the rinehart CAN Status Register
    def clearStatus():

    '''
''' # The ability to change EEPPROM over CAN isn't really necessary, could be implemented later if desired
    # Select which data terms to request from the Rinehart Motor Controller (RMC),
    # Refer to the RMS CAN protocol section 2.1 for more information
    # https://www.rinehartmotion.com/support.html 
    # Purpose: Send parameter 'CAN Active Messages Word' to enable/disable individual CAN
    # Broadcast Messages. 

    # NOTICE This is an EEPROM parameter, This value can only be set while the motor is not enabled
    # and the rinehart power must be recycled before the params are set

    # 0 = CAN Message broadcast disabled
    # 1 = CAN Message  broadcast enabed

    # Input: RMC_AMW ENUM, supplied input will DEACTIVATE its respective broadcast term
    # Output: A CAN packet (CAN Active Messages Word) is sent to the address 
    def setBroadcast(**kwargs):
        #Check if motor is enabled, if it is then raise an exception
        try:
            if self.motorEnable == True:
                raise RinehartError("Cannot edit EEPROM, motorEnable =" + str(self.motorEnable))
            else:
            byte0 = format(148)
            for value in kwargs.items():
        except:
    '''        

    '''        
    # Rinehart Motor Controller Active Messages Word used to enable/disable 
    class castmsg(Enum):
        T1 = auto()      #Temperatures 1
        T2 = auto()      #Temperatures 2
        T3 = auto()      #Temperatures 3
        AIV = auto()     #Analog Input Voltages
        DIS = auto()     #Digital Input Status
        MPI = auto()     #Motor Position Information
        CI = auto()      #Current Information
        VI = auto()      #Voltage Information
        FLUX = auto()    #Flux Information
        IV = auto()      #Internal Voltages
        IS = auto()      #Internal States
        FAULT = auto()   #Fault Codes
        TT = auto()      #Torque and Timer Information
        #MIF = auto()     #Modulation Index & Flux Weakening Output Information (Can't Disable)
        #FI = auto()      #Firmware Information (Can't Disable)
        #DD = auto()      #Diagnostic Data  (Can't Disable)
    '''


