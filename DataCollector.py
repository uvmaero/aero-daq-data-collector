# Peter Ferland 03.14.19
# AERO Data Acquisition Project

from Rinehart import Rinehart
from Emus import Emus
from Canpak import Canpak
import json
from DataCollectorError import DataCollectorError
import os
from time import time
import serial

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
        # create a Rinehart canDevice using
        self.rinehart = Rinehart('rinehart_addresses.csv')
        self.emus = Emus('emus_addresses.csv')
        self.tempboard = Tempboard('temp_addresses.csv')
        self.frontdaq = Daqboard('frontdaq_addresses.csv')
        self.reardaq = Daqboard('reardaq_addresses.csv')
        self.imu = imu()
        self.fileSize = fileSize * 10**6
        self.fileCount = fileCount
        self.indX = 0
        self.dataDict = {'ts':0,\
                        'rinehart': 0,\
                         'emus': 0,\
                         'imu': 0,\
                         'cell_volt': 0,\
                         'cell_temp': 0,\
                         'fl_data': 0,\
                         'fr_data': 0,\
                         'rl_data': 0,\
                         'rr_data': 0}


    # Purpose: take the data dictionaries created by other data-device objects and build the overall data dictionary
    def buildData(self,can_data,ser_data):
        self.dataDict['ts'] = time()
        self.dataDict['rinehart'] = self.rinehart.checkBroadcast(can_data)
        self.dataDict['emus'] = self.emus.checkBroadcast(can_data)[0]
        self.dataDict['cell_volt'] = self.emus.checkBroadcast(can_data)[1]
        self.dataDict['cell_temp'] = self.tempboard.checkBroadcast(can_data)
        self.dataDict['fl_data'] = self.frontdaq.checkBroadcast(can_data)
        self.dataDict['fr_data'] = self.frontdaq.checkBroadcast(can_data)
        self.dataDict['rl_data'] = self.reardaq.checkBroadcast(can_data)
        self.dataDict['rr_data'] = self.reardaq.checkBroadcast(can_data)
        self.dataDict['imu'] = self.imu.checkBroadcast(ser_data)

    # Make a function to create a new data.json file if the current
    # data.json file size becomes too large
    # Inputs:
    #   file_size: an integer representing the maximum allowable number of bytes for each file
    #   file_name: the name of the .json file to write data into 
    #   count: the maximum number of files you will allow to be created
    #   data: the data to write to the json file, this will likely be a python dictionary
    def RotateFile(self,data, max_count, file_size, file_name = ''):
        current_file = file_name + str(self.indX) + ".dat"
        # Check if the current file has exceeded its size limit, if so increase
        # the counter index and return the updated counter index to the user
        if int(os.path.getsize(current_file)) > file_size:
            self.indX += 1
            # Check if we have exceeded the max file count
            if self.indX > max_count:
                raise DataCollectorError("TooManyFilesError: dataCollector.py can no longer create new data logging files, the file limit has been exceeded!")
            # update the filename
            current_file = file_name + str(self.indX) + ".dat"
            
            print("New Data Log File: " + current_file)
        # Write data to the current file  
        with open(current_file,"a") as write_file:  
            json.dump(data,write_file)
            write_file.write('\n')
    
        
    # Purpose: begin logging data
    def startLogging(self,imu_port,can_port = '/dev/ttyACM0'):
        while True:
            with serial.Serial(can_port,xonxoff = True) as ser:

                # For TESTING ONLY, DISABLE LATER!!!!!!!!!!!
                self.rinehart.heartbeat()

                can_data = ser.readline()
                can_data = tuple(str(can_data).split())
                ser.close()
            with serial.Serial(imu_port,xonxoff = True) as ser:
                imu_data = ser.readline()
                ser.close()
            # Update the data dictionary
            self.buildData(can_data,imu_data)
            # write data to logging file
            self.RotateFile(self.dataDict,self.fileCount,self.indX,self.fileSize)
            
