import json
import time
import logging

import Enums
import scan_screen
import settings
from hunt_controller import HuntController

def run():
   last_enc = Enums.EncounterType.NONE
   num_scans = 0
   print("Lets Go")
   while True:
      res = scan_screen.get_encounter()
      logging.log(logging.DEBUG,res[0])
      if last_enc is not res[1]:
         hunt_controller.add(res[0],res[1].value)
         last_enc = res[1]
      time.sleep(1.5)
      num_scans += 1
      if num_scans % 30 == 0:
         hunt_controller.save()

if __name__ == "__main__":
   global_settings.load_settings()
   logging.getLogger('ppocr').setLevel(logging.WARNING)
   logging.getLogger("EncounterCounter").setLevel(logging.DEBUG)
   hunt_controller = HuntController()
   run()

