import octoprint.plugin
import tinytuya

class OctoTuyaPlugin(octoprint.plugin.StartupPlugin,
                     octoprint.plugin.AssetPlugin,
                     octoprint.plugin.TemplatePlugin,
		             octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.SimpleApiPlugin):
    def on_after_startup(self):
        self._logger.info("OctoTuya loaded successfully")
        self._logger.info("DEVICE_ID: " + self._settings.get(["DEVICE_ID"]))
        self._logger.info("IP: " + self._settings.get(["IP"]))
        self._logger.info("LOCAL_KEY: " + self._settings.get(["LOCAL_KEY"]))
        self._logger.info("DEVICE STATE: " + str(self._settings.get(["DEVICE_STATE"])))

        #d = tinytuya.OutletDevice(self._settings.get(["DEVICE_ID"]), self._settings.get(["IP"]), self._settings.get(["LOCAL_KEY"]))
        #d.set_version(3.3)

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
        if command == "printer":
            state = "{state}".format(**data)
            if(state=="True" and self._settings.get(["DEVICE_STATE"]) == False):
                self.ToggleDevice()
            if(state == "False" and self._settings.get(["DEVICE_STATE"]) == True):
                self.ToggleDevice()

    
    def ToggleDevice(self):
            d = tinytuya.OutletDevice(str(self._settings.get(["DEVICE_ID"])), str(self._settings.get(["IP"])), str(self._settings.get(["LOCAL_KEY"])))
            d.set_version(3.3)
            data = d.status()
            command = data['dps']['1']

            self._settings.set(["DEVICE_STATE"], command)
            self._logger.info("OLD DEVICE STATE: " + str(self._settings.get(["DEVICE_STATE"])))

            if(self._settings.get(["DEVICE_STATE"]) == True):
                d.turn_off()
            else:
                d.turn_on()

            data = d.status()
            command = data['dps']['1']

            self._settings.set(["DEVICE_STATE"], command)
            self._logger.info("NEW DEVICE STATE: " + str(self._settings.get(["DEVICE_STATE"])))



            # Führen Sie in Python eine Aktion aus, um die LED ein- und auszuschalten



        




__plugin_name__ = "OctoTuya"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = OctoTuyaPlugin()
