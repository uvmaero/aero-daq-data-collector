# Peter Ferland 03.14.19
# AERO Data Acquisition Project

# Import Extensions of canDevice Class for processing can data
from Rinehart import Rinehart
from Emus import Emus
from Tempmonitor import Tempmonitor
from Daqboard import Daqboard
from Pedalboard import Pedalboard
from Canpak import Canpak
from INS import INS
import json
from DataCollectorError import DataCollectorError
import os
from time import time
import serial
import datetime

# Purpose: The Datacollector object will create an instance of all CAN and Serial devices which send vehicle data for logging.
# This object will handle creation of data and json files and will do some general data preparation
# Inputs:
#   fileSize - an integer representing the maximum allowable file size in Megabytes
#   fileCount - an integer representing the maximum number of data files allowed
class Datacollector():
    # Inputs:
    #   fileSize - an integer representing the maximum allowable file size in Megabytes
    #   fileCount - an integer representing the maximum number of data files allowed
    def __init__(self,fileSize,fileCount):
        # create a Rinehart canDevices using the extended canDevice classes
        self.rinehart = Rinehart('CAN Addresses.csv')
        self.emus = Emus('CAN Addresses.csv')
        self.tempmonitor = Tempmonitor('CAN Addresses.csv')
        self.frontdaq = Daqboard('CAN Addresses.csv',deviceName='Front DAQ')
        self.reardaq = Daqboard('CAN Addresses.csv',deviceName='Rear DAQ')
        self.ins = INS('/dev/ttyS1')
        
        # Make new directory to save files to
        self.fileDir = os.path.join(os.getcwd(),datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(self.fileDir)
        # Datalogging file parameters
        self.fileSize = fileSize * 10**6
        self.fileCount = fileCount
        self.indX = 0
        self.dataDict = {'ts':0,\
                        'rinehart': 0,\
                         'emus': 0,\
                         'ins': 0,\
                         'cell_volt': 0,\
                         'cell_temp': 0,\
                         'front_left': 0,\
                         'front_right': 0,\
                         'rear_left': 0,\
                         'rear_right': 0}


    # Purpose: take the data dictionaries created by other data-device objects and build the overall data dictionary
    def buildData(self,can_data):
        self.dataDict['ts'] = time()
        self.dataDict['rinehart'] = self.rinehart.checkBroadcast(can_data)
        self.dataDict['emus'] = self.emus.checkBroadcast(can_data)[0]
        self.dataDict['cell_volt'] = self.emus.checkBroadcast(can_data)[1]
        self.dataDict['temp_faults'] = self.tempmonitor.checkBroadcast(can_data)[0]
        self.dataDict['cell_temp'] = self.tempmonitor.checkBroadcast(can_data)[1]
        # Think about how to do this
        self.dataDict['front_left'] = self.frontdaq.checkBroadcast(can_data)[0]
        self.dataDict['front_right'] = self.frontdaq.checkBroadcast(can_data)[1]
        self.dataDict['rear_left'] = self.reardaq.checkBroadcast(can_data)[0]
        self.dataDict['rear_right'] = self.reardaq.checkBroadcast(can_data)[1]
        self.dataDict['ins'] = self.ins.get_data(10)

    # Make a function to create a new data.json file if the current
    # data.json file size becomes too large
    # Inputs:
    #   file_size: an integer representing the maximum allowable number of bytes for each file
    #   file_name: the name of the .json file to write data into 
    #   count: the maximum number of files you will allow to be created
    #   data: the data to write to the json file, this will likely be a python dictionary
    def RotateFile(self,data, max_count, file_size):
        current_file = f'{self.indX}.dat'
        # Check if the current file has exceeded its size limit, if so increase
        # the counter index and return the updated counter index to the user
        flags = 'w'
        if os.path.join(self.fileDir).isfile(current_file):
            flags = 'a'
            # Join the fileDirectory which contains datalogging files
            if int(os.path.join(self.fileDir).getsize(current_file)) > file_size*1000:
                self.indX += 1
                # Check if we have exceeded the max file count
                if self.indX > max_count:
                    raise DataCollectorError("TooManyFilesError: dataCollector.py can no longer create new data logging files, the file limit has been exceeded!")
                # update the filename
                current_file = f'{self.indX}.dat'
                
                print("New Data Log File: " + current_file)
        # Write data to the current file
        # join the fileDirectory which contains datalogging files
        with open(os.path.join(self.fileDir,current_file),flags) as write_file:  
            json.dump(data,write_file)
            write_file.write('\n')
    
        
    # Purpose: begin logging data
    def startLogging(self,can_port = '/dev/ttyACM0'):
        while True:
            with serial.Serial(can_port,xonxoff = True,timeout=.01) as ser:
                can_data = ser.readline()
                can_data = tuple(str(can_data).split())
            # Update the data dictionary
            self.buildData((0,0))
            # write data to logging file
            self.RotateFile(self.dataDict,self.fileCount,self.fileSize)

# Start Logging
if __name__=="__main__":
    test = Datacollector(1,10)
    test.startLogging()

            
