#
# Schedule when to trigger a water pump at specific hours.
# Arguments:
#  - morning_schedule
#  - evening_schedule

import hassapi as hass
import datetime

class Watering(hass.Hass):

    def initialize(self):
        self.log("*** Starting Water Pump Scheduler at [SP time]: %s | [UTC time]: %s ***", datetime.datetime.now(), self.datetime())
    #    self.log("Current time self.datetime() : %s",self.datetime())
        utc_current_datetime = self.datetime()

        
         # Schedule daily watering. Once during the morning and once during the evening.
        morning_water_time = self.parse_datetime(format(self.args["morning_schedule"]))
        utc_morning_water_time = morning_water_time + datetime.timedelta(hours=4)
        utc_morning_water_time_3 = utc_morning_water_time + datetime.timedelta(minutes=3)

        evening_water_time = self.parse_datetime(format(self.args["evening_schedule"]))
        utc_evening_water_time = evening_water_time + datetime.timedelta(hours=4)
        utc_evening_water_time_3 = utc_evening_water_time + datetime.timedelta(minutes=3)

        # Schedule a daily callback that will call run_daily() at 8am and 7pm every day
        handle_morning = self.run_daily(self.daily_water_callback, self.parse_time(format(utc_morning_water_time)))
        handle_evening = self.run_daily(self.daily_water_callback, self.parse_time(format(utc_evening_water_time)))
        
        # Schedule second round daily callback 3 min after the first call
        handle_morning = self.run_daily(self.daily_water_callback, self.parse_time(format(utc_morning_water_time_3)))
        handle_evening = self.run_daily(self.daily_water_callback, self.parse_time(format(utc_evening_water_time_3)))


        self.log("Morning Schedule (UTC). First round: %s",self.parse_time(format(utc_morning_water_time)))
        self.log("Morning Schedule (UTC). Second round: %s",self.parse_time(format(utc_morning_water_time_3)))
        self.log("Evening Schedule (UTC). First round: %s",self.parse_time(format(utc_evening_water_time)))
        self.log("Evening Schedule (UTC). Second round: %s",self.parse_time(format(utc_evening_water_time_3)))

        if utc_morning_water_time < utc_current_datetime:
            self.log("Morning watering was already triggered at: %s", self.parse_time(format(utc_morning_water_time)))  
        elif utc_morning_water_time > utc_current_datetime:
            self.log("Morning watering yet to be triggered at: %s", self.parse_time(format(utc_morning_water_time)))
            message ="As plantas serão regadas às: " + str(self.parse_time(format(morning_water_time)))
            self.notify(message)
            
        if utc_evening_water_time < utc_current_datetime:
            self.log("Evening watering was already triggered at: %s", self.parse_time(format(utc_evening_water_time)))  
        elif utc_evening_water_time > utc_current_datetime:
            self.log("Evening watering yet to be triggered at: %s", self.parse_time(format(utc_evening_water_time)))
            message ="As plantas serão regadas às: " + str(self.parse_time(format(evening_water_time)))
            self.notify(message)
            
        self.log("Water Pump state is currenlty: %s", self.entities.switch.water_pump_controller.state)

    def daily_water_callback(self, kwargs):
    # Call to Home Assistant to turn the porch light on
        self.log("Water Pump current state: %s", self.entities.switch.water_pump_controller.state)
        if "water_pump_switch" in self.args:
            self.turn_on(self.args["water_pump_switch"])
            self.log("Water Pump automation state: %s", self.entities.switch.water_pump_controller.state)
            self.notify("As plantas estão sendo regadas agora") 


