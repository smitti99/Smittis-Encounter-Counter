import json
import logging


class HuntController:
    hunt_data = {}
    hunt_name = ""
    full_data = {}
    logger = logging.getLogger("EncounterCounter")
    in_encounter = False

    def __init__(self, name ="Default" ):
        self.hunt_name = name
        with open('../data/encounter_data.json') as f:
            self.full_data = json.load(f)
            if name in self.full_data:
                self.hunt_data = self.full_data[name]

    def add(self,name,count):
        if self.in_encounter:
            return
        self.in_encounter = True
        if name in self.hunt_data:
            self.hunt_data[name] += count
        else:
            self.hunt_data.update({name:count})
        self.logger.debug(name+ " "+ str(count))

    def save(self):
        with open('../data/encounter_data.json', "w") as f:
            self.full_data.update({self.hunt_name:self.hunt_data})
            json.dump(self.full_data,f)