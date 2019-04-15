# Copyright 2019 Cullen Jemison, UVM AERO
#
# AERO DAQ INS Data Collector
# Collects data from the Lord GNSS modules used in the AERO data
# acquisition system

import mscl

ERROR_COLOR = "\033[91m"
END_COLOR = "\033[0m"

class INS:
    def __init__(self, serial_port):
        # connect to the device
        try:
            connection = mscl.Connection.Serial(serial_port, 115200)
        except:
            print(f'{ERROR_COLOR}ERROR:{END_COLOR} Could not open serial port {serial_port}')
            exit(1)

        # create InertialNode
        self.node = mscl.InertialNode(connection)

        # set node to idle
        self.node.setToIdle()

        # setup imu channels
        ahrsImuChs = mscl.MipChannels()
        ahrsImuChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_SENSOR_SCALED_ACCEL_VEC, mscl.SampleRate.Hertz(50)))
        ahrsImuChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_SENSOR_SCALED_GYRO_VEC, mscl.SampleRate.Hertz(50)))
        ahrsImuChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_SENSOR_EULER_ANGLES, mscl.SampleRate.Hertz(50)))

        # setup gps channels
        gnssChs = mscl.MipChannels()
        gnssChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_GNSS_LLH_POSITION, mscl.SampleRate.Hertz(4)))
        gnssChs.append(mscl.MipChannel(mscl.MipTypes.CH_FIELD_GNSS_NED_VELOCITY, mscl.SampleRate.Hertz(4)))

        # make channels active
        self.node.setActiveChannelFields(mscl.MipTypes.CLASS_AHRS_IMU, ahrsImuChs)
        self.node.setActiveChannelFields(mscl.MipTypes.CLASS_GNSS, gnssChs)

        # start sampling on the AHRS/INS class of the Node
        self.node.enableDataStream(mscl.MipTypes.CLASS_AHRS_IMU)

        # start sampling on the GNSS class of the Node
        self.node.enableDataStream(mscl.MipTypes.CLASS_GNSS)


        # resume the INS
        self.node.resume()

        # initialize the INS data structure
        self.ins_data = {
            "accelX": 0,
            "accelY": 0,
            "accelZ": 0,
            "gyroX": 0,
            "gyroY": 0,
            "gyroZ": 0,
            "pitch": 0,
            "roll": 0,
            "yaw": 0,
            "latitude": 0,
            "longitude": 0,
            "altitude": 0,
            "speed": 0,
            "heading": 0
        }

    # Returns a dictionary of the lastest data from the INS
    # If the node returns no data before timeout (in milliseconds), then the returned
    # dictionary will be identical to whatever was last returned. Not all fields will
    # be updated every time the function is called, depending on how often it is called.
    def get_data(self, timeout):
        # get all packets from the device
        packets = self.node.getDataPackets(timeout)

        # loop through received packets
        for packet in packets:
            # get data points from the packet
            points = packet.data()
            
            # process all the data points in the packet
            for dataPoint in points:
                # accelerometer data points
                if dataPoint.channelName() == 'scaledAccelX':
                    self.ins_data["accelX"] = dataPoint.as_float()
                if dataPoint.channelName() == 'scaledAccelY':
                    self.ins_data["accelY"] = dataPoint.as_float()
                if dataPoint.channelName() == 'scaledAccelZ':
                    self.ins_data["accelZ"] = dataPoint.as_float()

                # gyroscope data points
                if dataPoint.channelName() == 'scaledGyroX':
                    self.ins_data["gyroX"] = dataPoint.as_float()
                if dataPoint.channelName() == 'scaledGyroY':
                    self.ins_data["gyroY"] = dataPoint.as_float()
                if dataPoint.channelName() == 'scaledGyroZ':
                    self.ins_data["gyroZ"] = dataPoint.as_float()

                # GPS data points
                if dataPoint.channelName() == 'latitude':
                    self.ins_data["latitude"] = dataPoint.as_float()
                if dataPoint.channelName() == 'longitude':
                    self.ins_data["longitude"] = dataPoint.as_float()
                if dataPoint.channelName() == 'heightAboveMSL':
                    self.ins_data["altitude"] = dataPoint.as_float()
                if dataPoint.channelName() == 'groundSpeed':
                    self.ins_data["speed"] = dataPoint.as_float()
                if dataPoint.channelName() == 'heading':
                    self.ins_data["heading"] = dataPoint.as_float()

                # attitude data points
                if dataPoint.channelName() == 'pitch':
                    self.ins_data["pitch"] = dataPoint.as_float()
                if dataPoint.channelName() == 'roll':
                    self.ins_data["roll"] = dataPoint.as_float()
                if dataPoint.channelName() == 'yaw':
                    self.ins_data["yaw"] = dataPoint.as_float()
        
        # return the collected data
        return self.ins_data

# if running from command line
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} serial_port')
        print('To log data from the INS node connected to serial_port')
        exit()

    # create an INS instance, use command line argument as serial port
    ins = INS(sys.argv[1])

    while(True):
        ins_data = ins.get_data(100)
        print(ins_data)
