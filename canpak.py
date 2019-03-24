#Create CAN packets from ID and Data strings
import serial
import codecs

class Canpak(object):
	#Usage: message = Canpak(0x111, 0x1122334455667788, 0x8)
	#		message.send(COM8) OR message.send(/dev/ttyACM1) on linux (untested, check serial documentation)
	def __init__(self, can_id, data, length, port = '/dev/ttyACM0'):
		#Length is in Bytes (0x1122334455667788 has length 0x8)
		self.port = port
		self.packet = '0' + format(can_id, '011b') + '000' + format(length, '04b') + format(data, '0' + str(int(length)) + 'b')
		self.packet = '0b' + self.packet.ljust(112, '0')
		self.packet = int(self.packet, 2)

	def hex_to_bytes(self):
		byte_packet = bytes.fromhex(str(hex(self.packet))[2:]) 
		return byte_packet
	
	def send(self):
		ser = serial.Serial(self.port,timeout=0, xonxoff = True)
		# Check if serial port is closed
		if ser.is_open == False:
			ser.open()	# Open the serial port
		ser.write(self.hex_to_bytes())
		# Close the serial port
		ser.close()

