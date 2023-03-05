/*
 * View model for OctoTuya
 *
 * Author: Lukas
 * License: AGPLv3
 */
$(function() {
    function OctotuyaViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.


        toggle = function() {
            $.ajax({
                url:         "/api/plugin/OctoTuya",
                type:        "POST",
                contentType: "application/json",
                dataType:    "json",
                headers:     {"X-Api-Key": UI_API_KEY},
                data:        JSON.stringify({"command": "TuyaLight", "state":true}),
                complete: function () {
                }
            });
            log.info("OCTOTUYA");
            return true;
        };

        self.disconnectPrinter = function() {
            $.ajax({
                url:         "/api/plugin/OctoTuya",
                type:        "POST",
                contentType: "application/json",
                dataType:    "json",
                headers:     {"X-Api-Key": UI_API_KEY},
                data:        JSON.stringify({"command": "printer", "state":false}),
                complete: function () {
                }
            });
            log.info("CPrinter");
            return true;
		}

		self.connectPrinter = function() {
            $.ajax({
                url:         "/api/plugin/OctoTuya",
                type:        "POST",
                contentType: "application/json",
                dataType:    "json",
                headers:     {"X-Api-Key": UI_API_KEY},
                data:        JSON.stringify({"command": "printer", "state":true}),
                complete: function () {
                }
            });
            log.info("CPrinter");
            return true;
		}

            


    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
        OCTOPRINT_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        OctotuyaViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        ["settingsViewModel"],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        ["#tab_plugin_OctoTuya"]
    ]);
    });
