#Create CAN packets from ID and Data strings
import serial
import codecs
import canpakError

class Canpak(object):
	#Usage: message = Canpak(0x111, 0x1122334455667788, 0x8)
	#		message.send(COM8) OR message.send(/dev/ttyACM1) on linux (untested, check serial documentation)
	def __init__(self, id, data, length):
	#Length is in Bytes (0x1122334455667788 has length 0x8)

		#Make a standard CAN frame
		self.packet = '0' + format(id, '011b') + '000' + format(length, '04b') + format(data, '0' + str(int(length)) + 'b')
		#append 0b to the start of the packet to signify that this is a binary value
		self.packet = '0b' + self.packet.ljust(112, '0')
		#convert packet from base 2 to an integer in base 10
		self.packet = int(self.packet, 2)
		
	def hex_to_bytes(self):
		byte_packet = bytes.fromhex(str(hex(self.packet))[2:]) 
		return byte_packet
	
	def send(self, port):
		
		ser = serial.Serial(port,timeout=0, xonxoff = True)
		
		print("  " + port + ":\n")
		print("    " + "Writing :  [ " + hex(self.packet) + " ] ")
		# Check if serial port is closed
		if ser.is_open() == False:
			ser.open()	# Open the serial port
		# Write CAN data to serial port
		number_of_bytes_written = ser.write(self.hex_to_bytes())
		# Close the serial port
		ser.close()
		print("    " + "Wrote :    [ " + str(number_of_bytes_written) + " Bytes ]")
		return number_of_bytes_written

	# Purpose: Read serial for CAN data, identify CAN frames, extract CAN frames from the 
	# bitstream, form a queue of CAN frames which can be decomposed and processed later
	def read(self, port):
		# create instance of serial using the port input
		ser = serial.Serial(port,timeout=0, xonxoff = True)
		# determine the length of 
		bytesToRead = ser.inWaiting()
		data = ser.read(bytesToRead)
		return data

	# Purpose: Take a CAN frame (bitstream) and decompose it into its constituent components,
	# (11-bit CAN ID, 4-bit Data Length Code, Variable Length Data). Package the data into a
	# tuple for easy processing of the data.
	def decompose(frame):


	# Purpose: Return the 11-bit CAN identifier read from a CAN packet
	def getIdentifier():

