# Library Imports 
import tkinter
import tkinter.messagebox
from typing import Optional, Tuple, Union
import customtkinter
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Dark"
customtkinter.set_default_color_theme("green")

# Importing Calibration and Model files 
import threading 
import time 
import yaml 
with open('CalibrationFile.yaml', 'r') as file: 
    calibration = yaml.safe_load(file)


ON_COLOR = "#d62222"
OFF_COLOR = "#717171"
LIGHT_GREY = "#e6e3e3"
GREY = "#717171"
DARK_GREY = "#212121"
BUTTON_GREY = "#5e5d5c"
RED = "#8c0900"
GREEN = "#095c10"
WHITE = "#fcfafa"


# Sidebar contains the logo, buttons, and scaling option menu
class Sidebar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # LOGO
        self.logo_label = customtkinter.CTkLabel(self, text="SOMPAS LASER", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 0))


# Contains slider for changing current and duration
class Settings(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs): 
        super().__init__(master, **kwargs)

        current_min = calibration['Limits']['current_min']
        current_max = calibration['Limits']['current_max']
        self.current_precision = calibration['Precision']['current']

        duration_min = calibration['Limits']['duration_min']
        duration_max = calibration['Limits']['duration_max']
        self.duration_precision = calibration['Precision']['duration']

        frequency_min = calibration['Limits']['frequency_min']
        frequency_max = calibration['Limits']['frequency_max']
        self.frequency_precision = calibration['Precision']['frequency']


        tec_min = calibration['Limits']['tec_min']
        tec_max = calibration['Limits']['tec_max']
        self.tec_precision = calibration['Precision']['tec']
        
        self.current = Setting(self, 30, 'Current', 'mA', current_min, current_max, self.current_precision)
        self.tec_temp = Setting(self, 190,  'TEC Temp', 'C', tec_min, tec_max, self.tec_precision)
        
        self.frequency = Setting(self, 350, 'Frequency', 'Hz', frequency_min, frequency_max, self.frequency_precision)
        self.duration = Setting(self, 510,  'Duration', 'ms', duration_min, duration_max, self.duration_precision)
    
    def getCurrent(self):
        current = int(self.current.getSettingValue() * (1/self.current_precision)) 
        return current

    def getDuration(self):
        duration = int(self.duration.getSettingValue() * (1/self.duration_precision)) 
        return duration 

    def getFrequency(self):
        frequency = int(self.frequency.getSettingValue() * (1/self.frequency_precision)) 
        return frequency 

    def getTEC(self):
        tec_temp = int(self.tec_temp.getSettingValue() * (1/self.tec_precision)) 
        return tec_temp
    
# Setting Bar  
class Setting(customtkinter.CTkFrame):
    def __init__(self, parent, y_pos, settingName, settingUnit, limit_lower, limit_upper, precision): 
        super().__init__(master=parent, fg_color="transparent")
        
        self.settingVal = limit_lower

        self.grid(row=0, column=0, sticky='nsew', padx=(10, 10), pady=(y_pos, 20))

        self.settingUnit = settingUnit
        self.limit_lower = limit_lower
        self.limit = limit_upper
        self.settingName = settingName
        self.precision = precision
        self.roundValue = str(self.precision).count('0')
        


        self.setting_title = customtkinter.CTkButton(self, 
                                                     text=self.settingName, 
                                                     hover=False, 
                                                     fg_color=GREY,
                                                     text_color_disabled=WHITE,
                                                     font=customtkinter.CTkFont(size=20, weight="bold"),
                                                     state="disabled") 
        
        self.setting_title.grid(row=0, column=0, padx=(0, 0), pady=(15, 10))
        
        self.minus_button = customtkinter.CTkButton(self, text="-", width=60, font=customtkinter.CTkFont(size=15, weight="bold"), text_color_disabled=WHITE, hover=False, fg_color=GREY, command=self.minus_button_event)
        self.minus_button.grid(row=0, column=1, padx=(0, 0), pady=(15, 10),)
        
        self.setting_button = customtkinter.CTkButton(self, width=80, font=customtkinter.CTkFont(size=15, weight="bold"),  text=str(self.limit_lower) + str(self.settingUnit), text_color_disabled=WHITE, hover=False, fg_color=GREY, state="disabled")
        self.setting_button.grid(row=0, column=2, padx=(0, 0), pady=(15, 10))
        
        self.plus_button = customtkinter.CTkButton(self, text="+", width=60, hover=False, fg_color=GREY, command=self.plus_button_event)
        self.plus_button.grid(row=0, column=3, padx=(0, 0), pady=(15, 10),)
        
        self.setting_slider = customtkinter.CTkSlider(self, from_=self.limit_lower,
                                                      to=self.limit, 
                                                      command=self.slider_event,
                                                      width=460, 
                                                      height=30,
                                                      fg_color=DARK_GREY,
                                                      progress_color=GREEN,
                                                      button_color=GREY,
                                                      button_hover_color=GREY,
                                                      orientation="horizontal",
                                                      hover='False')
        self.setting_slider.set(self.limit_lower)
        self.setting_slider.grid(row=1,column=0, columnspan=4, padx=(10, 10), pady=(10, 20))

    def getSettingValue(self):
        return self.settingVal
        
    def minus_button_event(self):
        if self.settingVal > self.limit_lower:
            self.settingVal = round(self.settingVal - self.precision, self.roundValue)
            # updates the slider position
            self.setting_slider.set(self.settingVal) 

        self.setting_button.configure(text=str(self.settingVal) + self.settingUnit)
        
    def plus_button_event(self):
        if self.settingVal < self.limit:
            self.settingVal += self.precision
            self.settingVal = round(self.settingVal, self.roundValue)
            self.setting_slider.set(self.settingVal) 

        self.setting_button.configure(text=str(self.settingVal) + self.settingUnit)
    
    def slider_event(self, value):
        self.settingVal = round(value, self.roundValue)
        if self.roundValue == 0: 
            self.settingVal = int(self.settingVal) 
        self.setting_button.configure(text=str(self.settingVal) + self.settingUnit)
            
    def updateSettingValue(self, value):
        self.settingVal = value
        self.setting_button.configure(text=str(self.settingVal) + self.settingUnit)
        self.setting_slider.set(self.settingVal)
       
# Port Settings
class PortSettings(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.add("PORT SETTINGS")
        
        self.combobox = customtkinter.CTkComboBox(master=self,
                                     values=["COM5", "COM6"]) 
        
        self.combobox.grid(row=3, column=0, padx=20, pady=(0, 0))
        
# TabView contains the tabs for the different states of the laser driver and TEC 
class DriverState(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("DRIVER STATE")

        # Laser Driver tab
        self.internalCurrent = customtkinter.CTkSwitch(master=self.tab("DRIVER STATE"),
                                                       progress_color=GREEN, 
                                                    text="LD: Set Internal Current  ",
                                                    )
        self.internalCurrent.grid(row=0, column=0, padx=20, pady=(15, 0)) 

        self.internalEnable = customtkinter.CTkSwitch(master=self.tab("DRIVER STATE"),
                                                      progress_color=GREEN, 
                                                    text="LD: Set Internal Enable   ")
        self.internalEnable.grid(row=1, column=0, padx=20, pady=(10, 0))
            
        self.tecInternalTemp = customtkinter.CTkSwitch(master=self.tab("DRIVER STATE"),
                                                       progress_color=GREEN, 
                                                    text="TEC: Set Internal Temp  ")
        self.tecInternalTemp.grid(row=2, column=0, padx=20, pady=(10, 0))

        self.tecInternalEnable = customtkinter.CTkSwitch(master=self.tab("DRIVER STATE"),
                                                    text="TEC: Set Internal Enable",
                                                    progress_color=GREEN)  
        self.tecInternalEnable.grid(row=3, column=0, padx=20, pady=(10,0))
        
        self.ignoreInterlock = customtkinter.CTkSwitch(master=self.tab("DRIVER STATE"),
                                                       progress_color=GREEN, 
                                                    text="LCK: Ignore Interlock      ")
        self.ignoreInterlock.grid(row=4, column=0, padx=20, pady=(10, 0))

        self.ignoreExternalNTC = customtkinter.CTkSwitch(master=self.tab("DRIVER STATE"),
                                                         progress_color=GREEN,
                                                    text="LCK: Ignore Ext. NTC      ")
        self.ignoreExternalNTC.grid(row=5, column=0, padx=20, pady=(10, 0))
        
        # Buttons to Reset and Load Settings

        self.resetLDButton = customtkinter.CTkButton(master=self.tab("DRIVER STATE"),
                                                    width=200,
                                                    border_spacing=0,
                                                    fg_color=GREY,
                                                    text="Reset",
                                                    corner_radius=12,
                                                    hover_color=BUTTON_GREY, 
                                                    command=self.resetLaserDriver)
        self.resetLDButton.grid(row=6, column=0, padx=40, pady=(20, 0))


        self.loadLDStateButton = customtkinter.CTkButton(master=self.tab("DRIVER STATE"),
                                                    width=200, 
                                                    border_spacing=0,
                                                    fg_color=GREY,
                                                    text="Load State", 
                                                    corner_radius=12, 
                                                    hover_color=BUTTON_GREY,
                                                    command=self.master.loadLaserState)
        self.loadLDStateButton.grid(row=7, column=0, padx=40, pady=(20, 0))

    def resetLaserDriver(self):
        # sets all switchs to off
        self.internalCurrent.deselect()
        self.internalEnable.deselect()
        self.tecInternalTemp.deselect()
        self.tecInternalEnable.deselect()
        self.ignoreInterlock.deselect()
        self.ignoreExternalNTC.deselect()

    def getInternalCurrent(self):
        return self.internalCurrent.get()

    def getInternalEnable(self):
        return self.internalEnable.get()
    
    def getTECInternalTemp(self):
        return self.tecInternalTemp.get()
    
    def getTECInternalEnable(self):
        return self.tecInternalEnable.get()
    
    def getIgnoreInterlock(self):
        return self.ignoreInterlock.get()
    
    def getIgnoreExternalNTC(self):
        return self.ignoreExternalNTC.get()

# App Class   
class App(customtkinter.CTk):

    def __init__(self, Controller):
        super().__init__()

        self.Controller = Controller

        # App Window
        self.title("ELoDiz Laser Control Software")
        self.geometry(f"{1100}x{650}")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Sidebar
        self.sidebar_frame = Sidebar(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Settings Bar Frame 
        self.settings_frame = Settings(self, width=100, height=10, corner_radius=0)
        self.settings_frame.grid(row=0, column=1, rowspan=4, padx=(20, 20), pady=(0, 0), sticky="nsew")

        # Driver Settings View
        self.driver_state = DriverState(master=self, segmented_button_fg_color=GREEN, segmented_button_selected_color=GREEN, segmented_button_selected_hover_color=GREEN, corner_radius=12) 
        self.driver_state.grid(row=0, column=2, rowspan=1,  padx=(0, 20), pady=(15, 0), sticky="nsew")
        
        # Buttons for Loading Laser Settings and turning Laser ON 
        
    
        self.toggle_laser_btn = customtkinter.CTkButton(master=self,
                                                    width=240, 
                                                    height=50,
                                                    text="Laser: OFF", 
                                                    hover=False, 
                                                    fg_color=RED, 
                                                    corner_radius=40,
                                                    font=customtkinter.CTkFont(size=15, weight="bold"), 
                                                    command=self.toggleLaser)
        self.toggle_laser_btn.grid(row=1, column=2, padx=(0,20), pady=(140, 0))

        # Start the background thread
        self.background_thread = threading.Thread(target=self.refresh)
        self.background_thread.daemon = True
        self.background_thread.start()
        
    # BUTTON COMMANDS

    # sends laser power state to the Model 
    def toggleLaser(self):
        OFF = self.toggle_laser_btn.cget("text") == "Laser: OFF"
        ON = not OFF

        # COMMANDED CALLED
        if OFF:
            self.Controller.Model.DriverState.laser_on = True 
            self.toggle_laser_btn.configure(text="Laser: ON", hover = False, fg_color=GREEN)
        elif ON:  
            self.Controller.Model.DriverState.laser_on = False 
            self.toggle_laser_btn.configure(text="Laser: OFF", hover = False, fg_color=RED)
        
    # gets the state of the laser to Model 
    def loadLaserState(self):
        # gets all the values from the driver state
        self.Controller.Model.DriverState.internal_current_set = self.driver_state.getInternalCurrent()
        self.Controller.Model.DriverState.internal_enable = self.driver_state.getInternalEnable()

        self.Controller.Model.DriverState.ignore_interlock = self.driver_state.getIgnoreInterlock()
        self.Controller.Model.DriverState.ignore_ext_ntc = self.driver_state.getIgnoreExternalNTC()

        self.Controller.Model.DriverState.tec_internal_temp = self.driver_state.getTECInternalTemp()
        self.Controller.Model.DriverState.tec_internal_enable = self.driver_state.getTECInternalEnable()
    
    # gets all the settings and writes these settings to the Modle 
    def loadLaserSettings(self): 
        # gets the values for current, frequecy, and duration from the settings bar
        self.Controller.Model.Settings.current = self.settings_frame.getCurrent()
        self.Controller.Model.Settings.frequency = self.settings_frame.getFrequency()
        self.Controller.Model.Settings.duration = self.settings_frame.getDuration()
        self.Controller.Model.Settings.tec_temp = self.settings_frame.getTEC()

    def refresh(self): 
        while True:
            # Constantly checks the laser settings are up to date
            # Refreshes the LD Driver and LD Settings and Power 
            time.sleep(0.1)
            self.loadLaserSettings() 
            self.Controller.refreshCycle() 
            #print("Data updated!")  # Call a method to update the tkinter label
