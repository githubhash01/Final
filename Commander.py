import Utils

""" 
Whenever a function is called, the command is sent to the port, and the response is checked.
If the response is not correct, an error is raised.
If the response is correct, the value is saved to the model.
"""

class LaserCommander: 

    def __init__(self, serialPort):
        
        self.Port = serialPort

    # Port Connection functions
    def connect(self): 
        self.Port.connect()
        print('Port Connected')

    def disconnect(self):
        self.Port.disconnect()

    """ 
    Commands for the View 

    # Set Value functions with check that value was sent correctly
    def loadLaserSettings(self, newCurrent, newDuration, newFrequency, newTemp):

        self.setCurrent(newCurrent)
        self.setDuration(newDuration)
        self.setFrequency(newFrequency)
        self.setTECTemp(newTemp)

        print(f"Current: {newCurrent}, Duration: {newDuration}, Frequency: {newFrequency}, Temperature: {newTemp}")

    # LD State: 
    def loadFullState(self, interlock_denied, ntc_denied, enable_internal, current_internal, tec_internal_enable, tec_internal_temp_set):

        # Goes through every state and checks all set correctly

        # Setting States
        if interlock_denied:
            self.blockInterlock()
        else:
            self.allowInterlock()
        if ntc_denied:
            self.blockNTC()
        else:
            self.allowNTC()
        if enable_internal:
            self.setInternalEnable()
        else:
            self.setExternalEnable()
        if current_internal:
            self.setInternalCurrent()
        else:
            self.setExternalCurrent()

        # TEC State 
        if tec_internal_enable:
            self.setTECInternalEnable()
        else:
            self.setTECExternalEnable()
        if tec_internal_temp_set:
            self.setTECInternalTemp()
        else:
            self.setTECExternalTemp()

        # Checking LD State Correct 
        sentLDState = [interlock_denied, ntc_denied, enable_internal, current_internal]
        sentTECState = [tec_internal_enable, tec_internal_temp_set]
        
        readLDState = self.readLDSState()
        if sentLDState == readLDState[:-1]: 
            print('LD: State Sent Correctly')
        else: 
            raise Exception('LD State Error')
        
        readTECState = self.readTECState()
        if sentTECState == readTECState[:-1]: 
            print("TEC: State Sent Correctly")
        else: 
            raise Exception('TEC State Error')


        # Checking if TEC State Correct 

    def readLDSState(self): 
        command = Utils.buildReadCode(DigitalCodes.READ_LD_STATE)
        ldsState = self.Port.read(command)
        ldsState = Utils.parseLDState(ldsState) 
        return ldsState

    def readTECState(self): 
        command = Utils.buildReadCode(DigitalCodes.READ_TEC_STATE) 
        tecState = self.Port.read(command)
        tecState = Utils.parseTECState(tecState)
        return tecState
    """
    def loadState(self, stateCode): 
        command = Utils.buildWriteCode(stateCode)
        self.Port.write(command)

    # Settings: 
    def loadSetting(self, settingCode, newValue): 
        command = Utils.buildWriteCode(digitalCode=settingCode, newValue=newValue)
        self.Port.write(command)

        response = self.readValue(digitalCode=settingCode)
        # checking command received 
        if  response != newValue: 
            raise Exception('Error in Loading Setting')
    
        else: 
            print(f'LD Reads: {response}')
        
    # helper function for checking setting value is correct
    def readValue(self, digitalCode): 
        command = Utils.buildReadCode(writeCode=digitalCode)
        response = self.Port.read(command)
        responseValue = Utils.getResponseValue(response)
        return responseValue
 