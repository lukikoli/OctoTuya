import octoprint.plugin
import tinytuya
from octoprint.events import Events

class OctoTuyaPlugin(octoprint.plugin.StartupPlugin,
                     octoprint.plugin.AssetPlugin,
                     octoprint.plugin.TemplatePlugin,
		             octoprint.plugin.SettingsPlugin,
                     octoprint.plugin.SimpleApiPlugin,
                     octoprint.plugin.EventHandlerPlugin):
    
    
    def on_after_startup(self):
        self._logger.info("OctoTuya loaded successfully")
        self._logger.info("DEVICE_ID: " + self._settings.get(["DEVICE_ID"]))
        self._logger.info("IP: " + self._settings.get(["IP"]))
        self._logger.info("LOCAL_KEY: " + self._settings.get(["LOCAL_KEY"]))
        self._logger.info("DEVICE_STATE: " + str(self._settings.get(["DEVICE_STATE"])))
        self._logger.info("Version: 0.0.1")
        self.CreateDeviceInstance()


    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=True),
            dict(type="settings", custom_bindings=False)
        ]

    def get_assets(self):
        return dict(
            js=["js/OctoTuya.js"]
        )
    
    def get_settings_defaults(self):
        return dict(DEVICE_ID="12345678", IP="X.X.X.X", LOCAL_KEY="123456789", DEVICE_STATE = False)

    def get_api_commands(self):
        return dict(TuyaLight=["state"])


    def on_api_command(self, command, data):
        if command == "TuyaLight":
            #bOn = "{state}".format(**data)
            self.ToggleDevice()

    def CreateDeviceInstance(self):
        self._logger.info("Creating Instance")
        global dev
        dev = tinytuya.OutletDevice(str(self._settings.get(["DEVICE_ID"])), str(self._settings.get(["IP"])), str(self._settings.get(["LOCAL_KEY"])))
        dev.set_version(3.3)
    

    def ToggleDevice(self):
            self.CheckDevState()
            self._logger.info("OLD DEVICE STATE: " + str(self._settings.get(["DEVICE_STATE"])))

            if(self._settings.get(["DEVICE_STATE"]) == True):
                dev.turn_off()
            else:
                dev.turn_on()

            self.CheckDevState()
            self._logger.info("NEW DEVICE STATE: " + str(self._settings.get(["DEVICE_STATE"])))



    def CheckDevState(self):
            data = dev.status()
            command = data['dps']['1']
            self._settings.set(["DEVICE_STATE"], command)


    #EVENTHANDLER PLUGIN
    def on_event(self, event, payload):
        if event == Events.CONNECTING and self._settings.get(["DEVICE_STATE"]) == False:
            dev.turn_on()
            self._logger.info("Turning ON Device Because of Device State Event")
            printer_profile = self._printer_profile_manager.get_default()
            profile = printer_profile["id"] if "id" in printer_profile else "_default"
            self._printer.connect(port="AUTO", baudrate=250000, profile=profile)

        if event == Events.PRINT_DONE:
             dev.turn_off
             self._logger.info("Turning OFF Device Because Print is done")

        if event == Events.DISCONNECTING:
            dev.turn_off()

__plugin_name__ = "OctoTuya"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = OctoTuyaPlugin()
