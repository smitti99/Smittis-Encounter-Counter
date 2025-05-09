import time
import logging

from src import Enums, scan_screen, settings
from src.hunt_controller import HuntController
from src.poke_tree import PokeTree

logger = logging.getLogger("EncounterCounter")
def run(): # pragma: no cover
   last_enc = Enums.EncounterType.NONE
   num_scans = 0
   logger.info("You can now start hunting")
   while True:
      res = scan_screen.get_encounter()
      logging.log(logging.DEBUG,res[0])
      if last_enc is not res[1]:
         for poke in res[0]:
            hunt_controller.add(poke)
         last_enc = res[1]
      time.sleep(1.5)
      num_scans += 1
      if num_scans % 30 == 0:
         hunt_controller.save()

if __name__ == "__main__": # pragma: no cover

   logging.getLogger('ppocr').setLevel(logging.WARNING)
   logger.setLevel(logging.DEBUG)
   logger.info("Loading Config...")
   settings.load_settings()
   logger.info("Config loaded")
   logger.info("Planting Search-Tree...")
   scan_screen.poke_tree = PokeTree(settings.global_settings["lang"])
   logger.info("Tree planted")
   logger.info("Loading 'wasted-time'-Data...")
   hunt_controller = HuntController()
   logger.info("Previous hunts loaded")
   run()

