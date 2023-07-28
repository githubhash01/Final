# communicates via serial port 
import serial 
import time 
import PortSearcher

class Port: 
    
    def __init__(self, waitTime=0.1): 
     
        self.waitTime = waitTime
        self.port = serial.Serial(
                            port=PortSearcher.findPort(), 
                            baudrate=115200, 
                            bytesize=8, 
                            timeout=1, 
                            stopbits=serial.STOPBITS_ONE)
        
        # connects on initialisation 
        self.connect()
        
    # closes any open port - opens new port
    def connect(self): 
        if(self.port.isOpen() == False):
            self.port.open()

    # disconnects from port 
    def disconnect(self): 
        self.port.close()

    # sends a write command
    def write(self, command):
        print(command) 
        # converts command to bytes
        self.port.write(command)
        time.sleep(self.waitTime)
    
    # sends a read command, and tries to get a response 
    def read(self, command): 
        # tries to get response 5 times
        for i in range(5):
            #print(command) 
            self.write(command)
            time.sleep(self.waitTime)
            response = str(self.port.readline())
            print(response)
            if 'K' in response: 
                break 

        if 'K' not in response:
            raise Exception("No Valid Response") 
            
        return response 
        
    


