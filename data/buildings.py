# -*- encoding: utf-8 -*-
from data.classes import Building
from data.improvements import *
from data.settings import *
from data.technologies import *

class Armory(Building):
  name = armory_t
  production_cost = 160
  tech_rq = [steel]

class Aqueduct(Building):
  name = aqueduct_t
  production_cost = 100
  maintenance = 1
  tech_rq = ['engineering']
  happiness = 1
  food = 1
  

class Barracks(Building):
  name = barracks_t
  production_cost = 75
  maintenance = 1
  tech_rq = [bronze_working]
  units = ['hirdmen', 'hoplites', 'immortals', 'huskarl', 'jarl', 'legatus', 'principes', 'spearmen', 'triarii']

class Castle(Building):
  name = castle_t

class Circus(Building):
  name = circus_t
  production_cost = 75
  res_rq = [horses, ivory]
  happiness = 2

class Colosseum(Building):
  name = colosseum_t
  production_cost = 100
  maintenance = 1
  tech_rq = [construction]
  happiness = 2
  
  

class Colossus(Building):
  name = colosus_t
  tech_rq = [iron_working]

class Courthouse(Building):
  name = courthouse_t
  production_cost = 100
  maintenance = 4
  tech_rq = [mathematics]
  unappiness = -2
  

class Curia(Building):
  name = curia_t
  production_cost = 120
  cost = 120
  maintenance = 2
  stack = 2
  happiness = 3
  culture = 10
  science = 4
  units = ['legatus']

class Granary(Building):
  name = granary_t
  production_cost = 60
  cost = 60
  maintenance = 1
  tech_rq = [pottery]
  resource1 = [bananas, deer, wheat]
  food = 1
  def setself(self, player, city):
    for owns in city.owns:
      if owns.resource in self.resource1:
        owns.c_food += 1

class Great_Hall(Building):
  name = great_hall_t
  production_cost = 80
  cost = 100
  stack = 2 
  happiness = 5
  culture = 5
  science = 2
  food = 2
  production = 1
  gold = 2

class Forge(Building):
  name = forge_t
  production_cost = 120
  maintenance = 1
  tech_rq = [metal_casting]
  res_rq = [iron]
  resource1 = [iron]
  def setself(self, player, city):
    for owns in city.owns:
      if owns.resource in self.resource1:
        owns.c_production = 1 
      

class Library(Building):
  name = library_t
  production_cost = 75
  maintenance = 1
  tech_rq = [writing]
  def setself(self, player, city):
    city.science += city.population//2

class Lighthouse(Building):
  name = lighthouse_t

class Monument(Building):
  name = monument_t
  production_cost = 40
  maintenance = 1
  tech_rq = [agriculture]
  culture = 2 

class Oracle(Building):
  name = oracle_t

class Palace(Building):
  name = palace_t
  production_cost = 140
  cost = 140
  tech_rq = [agriculture]
  stack = 2
  happiness = 4
  culture = 5
  science = 2
  food = 2
  production = 2
  gold = 3

class Shrine(Building):
  name = shrine_t
  production_cost = 40
  maintenance = 1
  tech_rq = [pottery]
  units = ['druid']
  culture = 5
  heal = 10
  happiness = 2

class Stable(Building):
  name = stable_t
  production_cost = 100
  maintenance = 1
  tech_rq = [animal_husbandry]
  improvements = [pasture]
  resource1 = [cattle, horses, sheep]
  def setself(self, player, city):
    for owns in city.owns:
      if owns.resource in self.resource1:
        owns.c_production += 1

class Temple(Building):
  name = temple_t
  
class Theater(Building):
  name = theater_t
  production_cost = 80
  maintenance = 2
  culture = 5
  science = 5
  happiness = 2

class Thingvellir(Building):
  name = thingvellir_t
  production_cost = 100
  tech_rq = [agriculture]
  units = ['hirdmen', 'huskarl', 'jarl']
  stack = 2
  happiness = 4
  culture = 5
  science = 2
  food = 2
  production = 2
  gold = 4

class University(Building):
  name = university_t

class Walls(Building):
  name = walls_t
  production_cost = 75
  maintenance = 1
  defense = 10

class Workshop(Building):
  name = workshop_t
  production_cost = 120
  maintenance = 2
  tech_rq = [metal_casting]
  production = 2

armory = Armory()
aqueduct = Aqueduct()
barracks = Barracks()
castle = Castle()
circus = Circus()
colosseum = Colosseum()
colossus = Colossus()
courthouse = Courthouse()
curia = Curia
forge = Forge()
granary = Granary()
great_hall = Great_Hall()
library = Library()
lighthouse = Lighthouse()
monument = Monument()
oracle = Oracle()
palace = Palace()
shrine = Shrine()
stable = Stable()
temple = Temple()
theater = Theater()
thingvellir = Thingvellir()
university = University()
walls = Walls()
workshop = Workshop()

buildings_list = [armory, aqueduct, barracks, castle, circus, colosseum,  
  colossus, curia, forge, granary, great_hall, library, lighthouse, monument,  
  oracle, palace, shrine, stable, temple, theater, thingvellir] 

defensive_buildings = [walls]
buildings_list += defensive_buildings
print('{} edificios.'.format(len(buildings_list)))