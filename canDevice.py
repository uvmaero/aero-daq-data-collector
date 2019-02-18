# Peter Ferland 02.07.2019
# AERO Data Acquisition Project

# Purpose: Create a Controller Area Network (CAN) Object which will be used to create
# extended classes. A can object will represent a device communicating on the can bus
import CanError

class canDevice(object):

    # Inputs:
    #   filename - the name of a csv file containing a list of 11-bit CAN addresses
    #   and address id tags which are strings which identify the CAN data ex)
    #   0x0A0,T1
    #   0x0A1,T2
    #   0x0A2,T3
    #   0x0A3,AIV ... and so on
    #   Offset - a decimal value describing the CAN offset applied
    def __init__(self, filename, Offset)
        self.Offset = Offset
        self.addressBook = readAddress("%s" % filename)

    # Purpose: Read a csv file and create a tuple using its contents. Used during initialization to
    # create a list of relevant CAN addresses with the CAN ID offset preapplied
    # Output Format: ((CANID1,ID_NAME1),(CANID2,ID_NAME2),...)
    # Example:       ((0x0A0,Temp1),(0x0A1,Temp2),(0x0A2,Temp3),(0x0A3,AIV),...)
    def readAddress(filename):
        try:
            with open(filename, newline='') as csvfile:
                # Make an empty list to hold data for the tuple
                addressBook = []
                csvread = csv.reader(csvfile)
                # Read each line of the csv file & extract the address as an integer
                for line in csvread:
                    address = self.offset + int(line[0,16])
                    name = line[1]
                    #write a tuple to the address book containing (CANID,ID_Name)
                    addressBook.append(tuple(address,name))
                # Return the address book as a tuple
                return tuple(address_book)
        except Exception as e:
            print(e.message,e.args)

    # Purpose: Check if a received CAN frame originates from the specified object,
    # if it was sent by the specified object then return a tuple with the 
    # appropriate CANID and IDNAME
    # Input: Frame - A tuple containing 3 hex values (ID,DLC,DATA)
    # Output: Output is either a boolean or a tuple
    # Output: Tuple: (IDNAME,BYTEARRAY) containing the CAN ID and IDNAME of the message
    # Output: Boolean: False - The received CAN frame was not sent by the rinehart 
    def process(frame):
        # Check if the object passed in is indeed a tuple
        if isinstance(frame, tuple):
            # Loop over all tuples in the daqAddress structure
            for tup in self.addressBook
                # Check if the CAN ID supplied is within the tuple, if so return a tuple
                # containing the IDNAME related to the CANID in the address book, and 
                # a byte array containing the data from the can data
                # format (IDNAME,BYTEARRAY)
                if frame[0] in tup:
                    # Ensure consistent formatting of hex data
                    # tup[1] contains the IDNAME of the current tuple observed from the addressBook
                    # frame[1] contains the data length code of the can frame
                    data = format(int(tup[1],16), '0' + str(int(frame[1])) + 'X')
                    # Create a bytearray from the data
                    data = bytearray.fromhex(data)
                    # return IDNAME and Bytearray
                    return tuple(tup[1],data)
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
    def concatBytes(*args):
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
        
            





       