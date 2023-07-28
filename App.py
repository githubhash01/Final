import ViewTk
import Model 
import Commander 
import Controller 
import SerialPort

def runApp(): 
    laserModel = Model.LaserModel() 
    port = SerialPort.Port()
    commander = Commander.LaserCommander(port)
    controller = Controller.LaserController(model=laserModel, commander=commander)
    app = ViewTk.App(Controller=controller)
    app.mainloop()

if __name__ == '__main__': 
    runApp()