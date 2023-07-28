# Util File 
import DigitalCodes

def intToHex(intNum):
    # converts an integer to a hex string of length 4 
    hexNum = hex(intNum)[2:]  # Convert decimal to hexadecimal and remove the '0x' prefix
    hexNum = hexNum.zfill(4)  # Pad with leading zeros if necessary
    hexNum = str(hexNum)
    hexNum = hexNum.upper()
    return hexNum

def hexToInt(hexNum):
    # converts string in hex to int
    hexNum = hexNum.strip()
    return int(hexNum, 16)

def hexToBin(hexNum):
    # converts hex to binary
    hexNum = hexNum.strip()
    return bin(int(hexNum, 16))[2:].zfill(8)

def parseLDState(state):
    print(state)
    # gets the last four digits of the state code 
    state = str(state)[:-3][-4:]
    # parses each bit of the state code and returns a list of the states
    state = hexToBin(state)
    interlock = int(state[0]) 
    ntc = int(state[1]) 
    enable = int(state[3]) 
    current = int(state[5]) 
    start = int(state[6]) 
    return [interlock, ntc, enable, current, start]

def parseTECState(state):
    print(state)
    state = str(state)[:-3][-4:]
    # parses each bit of the state code and returns a list of the states
    state = hexToBin(state)
    internal_enable= int(state[3]) 
    internal_temp = int(state[5]) 
    start = int(state[6]) 
    return [internal_enable, internal_temp, start]

def strToHex(ascii_string):
    str = ascii_string.encode('utf-8')
    return str.hex()

def buildReadCode(writeCode): 
    writeCode = writeCode.replace('P', 'J')
    writeCode = writeCode + '\r'
    command = bytes(writeCode, 'ascii')
    #print(command)
    return command

# takes in a base code 
def buildWriteCode(digitalCode, newValue=-1): 
    # builds the ascii code by converting the integer to hexidecimal string
    if newValue < 0: 
        textCode = digitalCode + '\r'
    else: 
        textCode = digitalCode + ' ' + intToHex(newValue) + '\r'
    command = bytes(textCode, 'ascii')
    #print(command)
    return command

# gets the last four digits of the response in hex and converts to int 
def getResponseValue(response): 
    #print(response)
    value = int(hexToInt(str(response)[:-3][-4:]))
    return value