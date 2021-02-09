from modules import cbpi
from modules.core.controller import KettleController
from modules.core.props import Property

#This plugin is a revered logic of the built-in "hyseresis" logic for kettle control

@cbpi.controller
class IceBankHysteresis(KettleController):

    # Custom Properties

    on = Property.Number("Offset On", True, 0, description="Offset above target temp when the ice-bank / glycol chiller should switched on. Should be bigger then Offset Off")
    off = Property.Number("Offset Off", True, 0, description="Offset above target temp when ice-bank / glycol chiller should switched off. Should be smaller then Offset Off")

    def stop(self):
        '''
        Invoked when the automatic is stopped.
        Normally you switch off the actors and clean up everything
        :return: None
        '''
        super(KettleController, self).stop()
        self.heater_off()




    def run(self):
        '''
        Each controller is exectuted in its own thread. The run method is the entry point
        :return: 
        '''
        while self.is_running():

            if self.get_temp() > self.get_target_temp() - float(self.on):
                self.heater_on(100)
            elif self.get_temp() <= self.get_target_temp() - float(self.off):
                self.heater_off()
            self.sleep(1)

