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
from LiveData import LiveData, LivePacketType
import json
from DataCollectorError import DataCollectorError
import os
from time import time
import serial
import datetime
import gzip
import shutil

# Purpose: The Datacollector object will create an instance of all CAN and Serial devices which send vehicle data for logging.
# This object will handle creation of data and json files and will do some general data preparation
# Inputs:
#   fileSize - an integer representing the maximum allowable file size in Megabytes
#   fileCount - an integer representing the maximum number of data files allowed
class Datacollector():
    # Inputs:
    #   fileSize - an integer representing the maximum allowable file size in Megabytes
    #   fileCount - an integer representing the maximum number of data files allowed
    def __init__(self,fileSize,fileCount,workingDir=''):
        # create a Rinehart canDevices using the extended canDevice classes
        self.rinehart = Rinehart('CAN Addresses.csv')
        self.emus = Emus('CAN Addresses.csv')
        self.tempmonitor = Tempmonitor('CAN Addresses.csv')
        self.frontdaq = Daqboard('CAN Addresses.csv',deviceName='Front DAQ')
        self.reardaq = Daqboard('CAN Addresses.csv',deviceName='Rear DAQ')
        self.ins = INS('/dev/ttyS0')
        self.pedalboard = Pedalboard('CAN Addresses.csv')
        
        # workingDir used by the zipIt function to navigate to the folder and 
        # check for subfolders to zip
        self.workingDir = workingDir

        # Make new directory to save files to, first check if user supplied a
        # custom directory
        if workingDir == '':
            self.fileDir = os.path.join(os.getcwd(),datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            self.zipIt(directory=os.getcwd())
            os.makedirs(self.fileDir)
        else:
            self.fileDir = os.path.join(workingDir,datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            self.zipIt(directory=self.workingDir)
            os.makedirs(self.fileDir)

        # Manifest.json dict
        self.manifest = {
            # set date to mm-dd-yy format
            "date": datetime.datetime.now().strftime('%m-%d-%Y'),
            # set start_time using 24 hr clock with hh:mm
            "start_time": datetime.datetime.now().strftime('%H:%M'),
            # set start_time using 24 hr clock with hh:mm
            "end_time": datetime.datetime.now().strftime('%H:%M'),
            # The number of data files (equal to self.indX + 1)
            "data_files": 1
        }
        # Datalogging file parameters
        self.fileSize = fileSize * 10**6
        self.fileCount = fileCount
        self.indX = 0
        self.dataDict = {'ts':0,\
                        'rinehart': self.rinehart.dataDict,\
                         'emus': self.emus.dataDict,\
                         'ins': self.ins.ins_data,\
                         'cell_volt': 0,\
                         'cell_temp': 0,\
                         'front_left': 0,\
                         'front_right': 0,\
                         'rear_left': 0,\
                         'rear_right': 0,\
                         'pedal_board':self.pedalboard.dataDict}
    
    # Get a list of subfolders in a directory
    def subfolders(self, path):
        try:
            return next(os.walk(path))[1]
        except StopIteration:
            return []

    # Purpose: zip any folders currently contained in the user specified base directory
    def zipIt(self,directory):
        # see if the supplied directory contains any subfolders
	
        if len(self.subfolders(directory)) > 0:
            # zip all directories insize the working directory
            for root, dirs, files in os.walk(directory):
                for d in dirs:
                    folder_dir = os.path.join(directory, d)
                    shutil.make_archive(folder_dir, 'zip',folder_dir)
                    shutil.rmtree(folder_dir)

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
        #self.dataDict['pedal_board'] = self.pedalboard.checkBroadcast(can_data)
        self.dataDict['ins'] = self.ins.get_data(10)
        
        #self.live.sendLivePacket(LivePacketType.PITCH, self.dataDict["ins"]["pitch"])
        # Send Current from rinehart
        try:
            current_msg = f'current {self.dataDict["rinehart"]["Id_Current"]}\r\n'
            self.live_ser.write(current_msg.encode(encoding='UTF-8'))
        except:
            pass
        # Send Cell Voltages from emus
        try:
            for cell,volt in enumerate(self.dataDict['cell_volt']):
                volt_msg = f'cell_volt {cell} {volt}\r\n'
                self.live_ser.write(volt_msg.encode(encoding='UTF-8'))
        except:
            pass
        # Send State of Charge from emus
        try:
            soc_msg = f'soc {0}\r\n'
            self.live_ser.write(soc_msg.encode(encoding='UTF-8'))
        except:
            pass
        # Send Cell Temps from TempMonitor
        try:
            for cell,temp in enumerate(self.dataDict['cell_temp']):
                temp_msg = f'cell_temp {cell} {temp}\r\n'
                self.live_ser.write(temp_msg.encode(encoding='UTF-8'))
        except:
            pass
        # Send INS Speed
        try:
            speed_msg = f'speed {self.dataDict["ins"]["speed"]}\r\n'
            self.live_ser.write(speed_msg.encode(encoding='UTF-8'))
        except:
            pass
        # Send INS pitch
        try:
            pitch_msg = f'pitch {self.dataDict["ins"]["pitch"]}\r\n'
            self.live_ser.write(pitch_msg.encode(encoding='UTF-8'))
        except:
            pass
        # Send Rinehart Motor Temp
        try:
            mtemp_msg = f'motor_temp {self.dataDict["rinehart"]["Motor_Temp"]}\r\n'
            self.live_ser.write(mtemp_msg.encode(encoding='UTF-8'))
        except:
            pass
        # Send Rinehart Controller Temp
        try:
            rtemp_msg = f'controller_temp {self.dataDict["rinehart"]["Gate_Driver_Temp"]}\r\n'
            self.live_ser.write(rtemp_msg.encode(encoding='UTF-8'))
        except:
            pass
        # send throttle from pedal board
        try:
            throttle_msg = f'throttle {self.dataDict["pedal"]["pedal0"]}\r\n'
            self.live_ser.write(throttle_msg.encode(encoding='UTF-8'))
        except:
            pass
        # send
	

    # Make a function to create a new data.json file if the current
    # data.json file size becomes too large
    # Inputs:
    #   file_size: an integer representing the maximum allowable number of bytes for each file
    #   file_name: the name of the .json file to write data into 
    #   count: the maximum number of files you will allow to be created
    #   data: the data to write to the json file, this will likely be a python dictionary
    def RotateFile(self,data, max_count, file_size):
        current_file = f'{self.indX}.dat'   # This is the .dat file used for storing data
        manifest_file = 'manifest.json'     # This is the manifest.json file
        current_file_path = os.path.join(self.fileDir, current_file)
        #manifest_file_path = os.path.join(self.fileDir, manifest_file)
        # Check if the current file has exceeded its size limit, if so increase
        # the counter index and return the updated counter index to the user
        flags = 'w'
        if os.path.isfile(current_file_path):
            flags = 'a'
            # Join the fileDirectory which contains datalogging files
            if int(os.path.getsize(current_file_path)) > file_size:                
                # Zip the last file created
                with open(current_file_path,'rb') as fin, gzip.open(f'{current_file_path}.gz','wb') as fout:
                    fout.writelines(fin)
                #print(current_file_path)
                # Remove the unzipped version of the newly zipped file to save space
                os.remove(current_file_path)                
                #Increment filecount index

                self.indX += 1
                # Check if we have exceeded the max file count
                if self.indX > max_count:
                    raise DataCollectorError("TooManyFilesError: dataCollector.py can no longer create new data logging files, the file limit has been exceeded!")                
                # update the filename
                current_file = f'{self.indX}.dat'
                current_file_path = os.path.join(self.fileDir, current_file)
                
                print("New Data Log File: " + current_file)
        # Write data to the current file
        # join the fileDirectory which contains datalogging files
        with open(current_file_path,flags) as write_file:  
            json.dump(data,write_file)
            write_file.write('\n')
        # Update manifest.json
        with open(os.path.join(self.fileDir,manifest_file),'w') as write_file:
            self.manifest['end_time'] = datetime.datetime.now().strftime('%H:%M')
            self.manifest['data_files'] = self.indX + 1
            json.dump(self.manifest,write_file)
    
        
    # Purpose: begin logging data
    def startLogging(self,can_port = '/dev/ttyACM0',live_port='/dev/ttyUSB0'):
        # changed serial functionality
        can_ser = serial.Serial(can_port,xonxoff=True,timeout=0.1)
        live_ser = serial.Serial(live_port, baudrate=115200)
        self.live = LiveData(live_ser)
        while True:
            try:
                can_data = can_ser.readline()
                can_data = tuple(str(can_data).split())
            except:
                print('Datacollector Serial Read Error')
                pass
            # Update the data dictionary
            self.buildData((0,0))
            # write data to logging file
            self.RotateFile(self.dataDict,self.fileCount,self.fileSize)

# Start Logging
if __name__=="__main__":
    # fileSize represents the max filesize in MegaBytes
    # fileCount represents the number of files which we will allow to be made
    # workingDir represents the base directory where subfolders containing Data will be written to
    # please don't change workingDir
    test = Datacollector(fileSize=1,fileCount=1000,workingDir='/home/aero/Datalog')
    test.startLogging()

            
