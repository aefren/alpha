from copy import deepcopy as DC
from data.classes import Nation
from data.buildings import *
from data.improvements import *
from data.units import *
from data.technologies import *

# Nations.
class Castellum(Nation):
  name = "Castellum"
  nameid = "Castellum"
  actions = ['ai_move']
  commandpoints = 7
  startbasepreference = [1, 2,3]
  starttoppreference = [-1, 0, 1]
  citynames = ["Sutrium", "Nicopolis", "Eburacum", "Lugdunum", "Treveri", 
    "Sirmium", "Teurnia", "Curia", "Alba Fucens", "Luceria", "Arminium"]
  randomname = 0
  
  av_buildings = [armory, aqueduct, barracks, circus, colosseum, colossus, courthouse, forge, granary, library, monument, palace, stable, theater]+defensive_buildings
  av_improvements = improvements_list
  av_units = [accensii, astatii, legatus, medicus, principes, sagittarii, 
    scouts, settler, triarii, trireme, worker, work_boat]
  av_tech = [ancient_era+clasical_era+medieval_era]
  initial_buildings = [palace]
  initial_units = [sagittarii, galley, galley, accensii, accensii, settler]
  researched = [agriculture]


class Natives(Nation):
  name = "Natives"
  nameid = "Natives"
  actions = ['ai_move']
  commandpoints = 7
  startbasepreference = [1, 2]
  starttoppreference = [-1, 0, 1]
  citynames = ['Jauja', "Cusco", "Chupaca"]
  randomname = 0
  
  av_buildings = [aqueduct, forge, granary, great_hall, library, monument, shrine, stable]+defensive_buildings
  av_improvements = improvements_list
  av_tech = ancient_era+clasical_era+medieval_era
  av_units = [druid, hunters, scouts, horse_archers, rangers, warriors, worker, 
    settler, trireme, work_boat]
  initial_buildings = [great_hall]
  initial_units = [worker, worker, scouts, warriors, warriors, warriors, settler]
#   initial_units = [hunters, galley, galley, cataphracts, catapult, scouts, warriors, settler]
  researched = [agriculture]

class Nomads(Nation):
  name = "Nomads"
  nameid = "Nomads"
  actions = ['ai_move']
  startbasepreference = [0, 1, 2, 3, 4]
  starttoppreference = [-1, 0,  1, 2]
  citynames = ['Agars', 'Bali', 'Bitra', 'Hydra', 'Hull', 'Ramea', ]
  randomname = 1
  
  av_buildings = list()
  av_improvements = list()
  av_tech = list()
  av_units = list() 
  initial_buildings = list()
  initial_units = list()
  for r in range(90): initial_units.append(DC(raiders))
  researched = list()


#Nations.
castellum = Castellum()
natives = Natives()
nomads = Nomads()

nations = [natives, nomads, castellum]