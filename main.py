import time
import logging


import scan_screen
if __name__ == "__main__":
   logging.getLogger('ppocr').setLevel(logging.WARNING)
   res = scan_screen.get_encounter()
   name = res[0].rsplit(" ",1)[0]
   encounter_type = res[1].name
   print( name+ " Type: "+ encounter_type)

   for i in range(100):
      res = scan_screen.get_encounter()
      name = res[0]#.rsplit(" ", 1)[0]
      encounter_type = res[1].name
      print(name + " Type: " + encounter_type)
      time.sleep(2.5)


      #
      #  Abra , Absol
      #  { A: {
      #         b: {
      #            r : "Abra",
      #            s : "Absol"
      #         }
      #
      #
      #