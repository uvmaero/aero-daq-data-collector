import CanUtilError
class canUtils(object):
    # Purpose, specify which byte(s) of data you care about and some hex data,
    # and this function will return the byte(s) of interest as a hex string
    # without the '0x' hex prefix.
    # Inputs:
    #   data - a hex string of data, up to 8 bytes 
    #   dlc - data length code, an integer 1-8 representing the number of bytes
    # Output:
    #   A hex string consisting of bytes 
    def canByte(data,dlc):
        #Format data as a string without '0x' hex prefix, (data sanitization for function input)
        data = format(int(data,16), '0' + str(int(dlc)) + 'X')
        # Create an empty string (x) to append data to
        for 
            # If arg isn't an integer throw an error and exit the function
            if not isinstance(arg,int):
                raise CanUtilError("Error, Input isn't an Integer")
                return
            # append Nibble 1 of byte arg and Nibble 2 of byte arg
            # Nibble 1 of byte arg = data[(2*arg)+1]
            # Nibble 2 of byte arg = data[(2*arg)]
            x = x + data[(2*arg)] + data[(2*arg)]
        return x
        
print(canUtils.canByte('0xFABCD',3,1,2,3))