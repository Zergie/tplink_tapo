import logging
from PyP100 import PyP110

class TPLinkTapo:
    def __init__(self, config) -> None:
        self.printer = config.get_printer()
        # Setup plug
        self.plug = PyP110.P110(config.get("address"), config.get("user"), config.get("password"))
        # Register commands
        plug_name = config.get_name().split()[1]
        gcode = self.printer.lookup_object('gcode')
        gcode.register_mux_command('QUERY_PLUG', 'PLUG', plug_name,
                                   self.cmd_QUERY_PLUG,
                                   desc=self.cmd_QUERY_PLUG_help)
        gcode.register_mux_command('TURN_OFF_PLUG', 'PLUG', plug_name,
                                   self.cmd_TURN_OFF_PLUG,
                                   desc=self.cmd_TURN_OFF_PLUG_help)
        gcode.register_mux_command('TURN_ON_PLUG', 'PLUG', plug_name,
                                   self.cmd_TURN_ON_PLUG,
                                   desc=self.cmd_TURN_ON_PLUG_help)

    @property
    def _plug(self):
        self.plug.handshake()
        self.plug.login()
        return self.plug

    cmd_QUERY_PLUG_help = "Queries a given TP-Link tapo plug"
    def cmd_QUERY_PLUG(self, gcmd):
        plug = self._plug
        plugName = plug.getDeviceName()
        gcmd.respond_raw("== %s ==" % (plugName,))
        energyUsage = plug.getEnergyUsage()["result"]
        gcmd.respond_raw("Local Time: %s" % (energyUsage["local_time"]))
        gcmd.respond_raw("Runtime Today: %s min" % (energyUsage["today_runtime"]))
        gcmd.respond_raw("Runtime Month: %s min" % (energyUsage["month_runtime"]))
        gcmd.respond_raw("Energy Usage Today: %s kWh" % (energyUsage["today_energy"]/1000))
        gcmd.respond_raw("Energy Usage Month: %s kWh" % (energyUsage["month_energy"]/1000))
        gcmd.respond_raw("Current Energy Usage: %s W" % (energyUsage["current_power"]/1000,))

    cmd_TURN_OFF_PLUG_help = "Turns off a given TP-Link tapo plug"
    def cmd_TURN_OFF_PLUG(self, gcmd):
        delay = gcmd.get_float('DELAY', None)
        if delay is None:
            self._plug.turnOff()
        else:
            self._plug.turnOffWithDelay(delay)

    cmd_TURN_ON_PLUG_help = "Turns on a given TP-Link tapo plug"
    def cmd_TURN_ON_PLUG(self, gcmd):
        delay = gcmd.get_float('DELAY', None)
        if delay is None:
            self._plug.turnOn()
        else:
            self._plug.turnOnWithDelay(delay)


def load_config_prefix(config):
    return TPLinkTapo(config)
