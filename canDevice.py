# Peter Ferland 02.07.2019
# AERO Data Acquisition Project

# Purpose: Create a Controller Area Network (CAN) Object which will be used to create
# extended classes. A can object will represent a device communicating on the can bus
from CanError import CanError
import csv

class CanDevice(object):

    # Inputs:
    #   filename - the name of a csv file containing a list of 11-bit CAN addresses
    #   and address id tags which are strings which identify the CAN data ex)
    #   0x0A0,T1
    #   0x0A1,T2
    #   0x0A2,T3
    #   0x0A3,AIV ... and so on
    #   Offset - a decimal value describing the CAN offset applied
    def __init__(self, filename, deviceName: str):
        self.deviceName = deviceName
        self.addressBook = self.readAddress("%s" % filename)

    # Purpose: Read a csv file and create a tuple using its contents. Used during initialization to
    # create a list of relevant CAN addresses with the CAN ID offset preapplied
    # Output Format: ((CANID1,ID_NAME1),(CANID2,ID_NAME2),...)
    # Example:       ((0x0A0,Temp1),(0x0A1,Temp2),(0x0A2,Temp3),(0x0A3,AIV),...)
    def readAddress(self,filename):
        try:
            with open(filename, newline='') as csvfile:
                # Make an empty list to hold data for the tuple
                addressBook = {}
                csvread = csv.reader(csvfile)
                # Read each line of the csv file & extract the address as an integer
                for line in csvread:
                    # Check if the line of the CSV file is intended for this device
                    if line[2] == self.deviceName:
                        # Check if the Address is of any interest to us
                        if line[4] not in (None,""):
                            address = int(line[0])
                            name = line[4]
                            #write a tuple to the address book containing (CANID,ID_Name)
                            addressBook[name] = address
                # Return the address book as a tuple
                return addressBook
        except Exception as e:
            print(e)

    # Purpose: Check if a received CAN frame originates from the specified object,
    # if it was sent by the specified object then return a tuple with the 
    # appropriate CANID and IDNAME
    # Input: Frame - A tuple containing 3 hex values (ID,DLC,DATA)
    # Output: Output is either a boolean or a tuple
    # Output: Tuple: (IDNAME,BYTEARRAY) containing the CAN ID and IDNAME of the message
    # Output: Boolean: False - The received CAN frame was not sent by the rinehart 
    def process(self,frame):
        # Check if the object passed in is indeed a tuple
        if isinstance(frame,tuple):
            # Loop over all keys and values in the addresBook to determine if 
            # the address passed is relevant to this instance
            for addr_name,addr in self.addressBook.items():
                # Check if the CAN ID supplied is in the dictionary, if so return a tuple
                # containing the IDNAME related to the CANID in the address book, and 
                # a byte array containing the data from the can data
                # format (IDNAME,BYTEARRAY)
                if frame[0] == addr:
                    # Ensure consistent formatting of hex data
                    # frame[1] contains the hex data of the can frame
                    data = format(int(frame[1],16), '0' + str(int(len(frame[1])/2) + 'X'))
                    # Create a bytearray from the data
                    data = bytearray.fromhex(data)
                    # return IDNAME and Bytearray
                    return tuple([addr_name,data])
            # If we do not find the supplied CAN ID in any of the tuples then return false
            return False
        else:
            raise CanError("Cannot process " + str(frame) + "is not a tuple!")

    # Purpose: Concatenate multiple separate bytes of integer data into a single integer representation
    # Input:
    #   *args - 2 or more bytes of integer data taken form a bytearray
    #   The first byte input is assumed to be the most significant byte
    #   The last byte input is assumed to be the least significant byte
    #   Ex) concatBytes(0xFF,0xAA,0xBB) -> 0xFFAABB
    #   Ex) concatBytes(255,170,187) -> 16755387
    # Output:
    #   data - one integer containing multiple bytes of data
    def concatBytes(self,*args):
        numBytes = len(args)
        # make a number to bitwise or with
        data = 0 
        # Loop over all bytes in args, count is loop count
        for count,arg in enumerate(args):
            # ensure argument passed is no more than 1 byte of data
            if arg > 255:
                raise CanError('Error %s arg > 255' % arg)
            # calculate the number of bits to shift, this will shift
            # 8 bits at a time (1 byte shift)
            shift = (numBytes - count - 1) * 8
            # perform bit shift to the left
            argShift = arg << shift
            # Bitwise or data
            data = data|argShift
        return data

    # Purpose: Determine if a fault code was sent, the EMUS will send bytes with each bit 
    # representing an individual fault code. This function takes a byte from a bytearray
    # and the bit of the flag being checked and determines if the flag was set. This is 
    # performed by converting the byte data to an integer and performing a bitwise and
    # with the flag bit, if the result of this bitwise and is greater than 0 then the flag
    # was set and the function will return a 1, otherwise the function will return a zero
    # Inputs: 
    #   byteData: a single byte of data
    #   bit: the flag bit to be checked
    # Outputs:
    #   int(1) if the flag is set
    #   int(0) if the flag isn't set
    def interpretFlags(self,byteData,bit):
        return (1 if int(byteData) & (1 << bit) > 0 else 0)
        
            





       