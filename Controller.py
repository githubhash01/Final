import DigitalCodes

class LaserController: 

    def __init__(self, model, commander): 
        self.Model = model 
        self.Commander = commander 

        # Value Settings: 
        self.current_prev = self.Model.Settings.current
        self.duration_prev = self.Model.Settings.duration 
        self.frequency_prev = self.Model.Settings.frequency
        self.tec_temp_prev = self.Model.Settings.tec_temp

        # Driver State: 
        self.lasing_prev = self.Model.DriverState.laser_on

        self.internal_current_prev = self.Model.DriverState.internal_current_set
        self.internal_enable_prev = self.Model.DriverState.internal_enable
        self.tec_internal_temp_prev = self.Model.DriverState.tec_internal_temp
        self.tec_internal_enable_prev = self.Model.DriverState.tec_internal_enable
        self.ignore_intlck_prev = self.Model.DriverState.ignore_interlock
        self.ignore_ext_ntc_prev = self.Model.DriverState.ignore_ext_ntc

    # calls all refresh methods
    def refreshCycle(self): 
        self.refreshSettings()
        self.refreshState()
        self.refreshPower()

    def refreshPower(self): 
        # update the state of the power with commander if changed 
        lasing = self.Model.DriverState.laser_on
        if lasing != self.lasing_prev: 
            print(f'Lasing: {lasing}')
            if lasing:
                self.Commander.loadState(stateCode=DigitalCodes.LD_START)
            else: 
                self.Commander.loadState(stateCode=DigitalCodes.LD_STOP) 
            self.lasing_prev = lasing 

    def refreshSettings(self): 
        # update the settings with commander if they have changed 
        current = self.Model.Settings.current
        duration = self.Model.Settings.duration
        frequency = self.Model.Settings.frequency
        tec = self.Model.Settings.tec_temp

        if current != self.current_prev: 
            print(f'Current: {current}')
            self.Commander.loadSetting(settingCode=DigitalCodes.WRITE_CURRENT, newValue=current)
            self.current_prev = current

        if duration != self.duration_prev: 
            print(f'Duration: {duration}')
            self.Commander.loadSetting(settingCode=DigitalCodes.WRITE_DURATION, newValue=duration)
            self.duration_prev = duration 
        
        if frequency != self.frequency_prev: 
            print(f'Frequency: {frequency}')
            self.Commander.loadSetting(settingCode=DigitalCodes.WRITE_FREQUENCY, newValue=frequency)
            self.frequency_prev = frequency

        if tec != self.tec_temp_prev: 
            print(f'TEC Temp: {tec}')
            self.Commander.loadSetting(settingCode=DigitalCodes.WRITE_TEC_TEMP, newValue=tec)
            self.tec_temp_prev = tec

    def refreshState(self): 
                
        internal_current = self.Model.DriverState.internal_current_set
        internal_enable = self.Model.DriverState.internal_enable
        tec_internal_temp = self.Model.DriverState.tec_internal_temp
        tec_internal_enable = self.Model.DriverState.tec_internal_enable
        ignore_intlck = self.Model.DriverState.ignore_interlock
        ignore_ext_ntc = self.Model.DriverState.ignore_ext_ntc

        if internal_current != self.internal_current_prev: 
            print(f'Internal Current: {internal_current}')
            if internal_current: 
                self.Commander.loadState(stateCode=DigitalCodes.LD_INTERNAL_CURRENT)
            else: 
                self.Commander.loadState(stateCode=DigitalCodes.LD_EXTERNAL_CURRENT)
            self.internal_current_prev = internal_current

        if internal_enable != self.internal_enable_prev: 
            print(f'Internal Enable {internal_enable}')
            if internal_enable: 
                self.Commander.loadState(stateCode=DigitalCodes.LD_INTERNAL_ENABLE)
            else: 
                self.Commander.loadState(stateCode=DigitalCodes.LD_EXTERNAL_ENABLE)
            self.internal_enable_prev = internal_enable

        if tec_internal_temp != self.tec_internal_temp_prev: 
            print(f'TEC Internal Temp: {tec_internal_temp}')
            if tec_internal_temp: 
                self.Commander.loadState(stateCode=DigitalCodes.TEC_INTERNAL_TEMP)
            else: 
                self.Commander.loadState(stateCode=DigitalCodes.TEC_EXTERNAL_TEMP)
            self.tec_internal_temp_prev = tec_internal_temp

        if tec_internal_enable != self.tec_internal_enable_prev: 
            print(f'TEC Internal Enable: {tec_internal_enable}')
            if tec_internal_enable: 
                self.Commander.loadState(stateCode=DigitalCodes.TEC_INTERNAL_ENABLE)
            else: 
                self.Commander.loadState(stateCode=DigitalCodes.TEC_EXTERNAL_ENABLE)
            self.tec_internal_enable_prev = tec_internal_enable
        
        if ignore_intlck != self.ignore_intlck_prev: 
            print(f'Ignore Intlck: {ignore_intlck}')
            if ignore_intlck: 
                self.Commander.loadState(stateCode=DigitalCodes.INTERLOCK_BLOCK)
            else: 
                self.Commander.loadState(stateCode=DigitalCodes.INTERLOCK_ALLOW)
            self.ignore_intlck_prev = ignore_intlck
        
        if ignore_ext_ntc != self.ignore_ext_ntc_prev: 
            print(f'Ignore Ext NTC: {ignore_ext_ntc}')
            if ignore_ext_ntc: 
                self.Commander.loadState(stateCode=DigitalCodes.NTC_EXT_BLOCK)
            else: 
                self.Commander.loadState(stateCode=DigitalCodes.NTC_EXT_ALLOW)
            self.ignore_ext_ntc_prev = ignore_ext_ntc
