# Peter Ferland 02.07.2019
# AERO Data Acquisition Project

# Purpose: Create a Controller Area Network (CAN) Object which will be used to create
# extended classes. A can object will represent a device communicating on the can bus

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



       