import serial.tools.list_ports

def findPort(): 
    ports = serial.tools.list_ports.comports()
    serialPort = None
    for port, desc, hwid in sorted(ports): 
        if 'USB to UART' in str(desc): 
            serialPort = port 
    
    if not serialPort: 
        raise Exception('Could not find port - check USB cable connection') 
    return str(serialPort)  

