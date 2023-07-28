class LaserModel: 

    def __init__(self): 
        self.Settings = Settings()
        self.DriverState = DriverState()

class Settings: 

    def __init__(self): 
        self.current = 0
        self.duration = 10
        self.frequency = 0
        self.tec_temp = 1500
    
class DriverState: 

    def __init__(self): 
        
        self.laser_on = False 

        self.internal_current_set = False 
        self.internal_enable = False

        self.tec_internal_temp = False 
        self.tec_internal_enable = False 


        self.ignore_interlock = False
        self.ignore_ext_ntc = False


