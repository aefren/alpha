# -*- encoding: utf-8 -*-
from pdb import Pdb
from data.classes import Tech
# from data.improvements import *
from data.settings import *

#Ancient era.
class Agriculture(Tech):
  name = agriculture_t
  science_cost = 25
  buildings = ['great_hall', 'palace',]
  improvements = ['farm']
  leads = ['animal_husbandry', 'archery ', 'mining', 'pottery']
  units = ['accensii', 'scouts', 'warriors', 'settler', 'worker']

class Animal_Husbandry(Tech):
  name = animal_husbandry_t
  science_cost = 35
  buildings = ['stable']
  leads = ['trapping']
  improvements = ['pasture']
  reveal = ['horses']
  tech_rq = ['agriculture']
  units = ['equites', 'war_elephants']
  

class Archery(Tech):
  name = archery_t
  science_cost = 35
  leads = []
  units = ['archers', 'horse_archers', 'rangers']
  tech_rq = ['agriculture']

class Bronze_Working(Tech):
  name = bronze_working_t
  science_cost = 55
  buildings = ['barracks']
  leads = ['iron_working']
  units =['astatii', 'spearmen']
  reveal = ['iron']
  tech_rq = ['mining']
  clear_jungle = 1

class Calendar(Tech):
  name = calendar_t
  science_cost = 55
  improvements = ['plantation']
  leads = ['philosophy']
  tech_rq = ['pottery']
  reveal = ['wine']

class Masonry(Tech):
  name = masonry_t
  science_cost = 55
  buildings = ['walls']
  improvements = ['quarry']
  leads = ['construction']
  tech_rq = ['mining']

class Mining(Tech):
  name = mining_t
  science_cost = 35
  improvements = ['mine']
  leads = ['bronze_working', 'masonry']
  tech_rq = ['agriculture']
  reveal = ['gold']
  clear_forest = 1

class Pottery(Tech):
  name = pottery_t
  science_cost = 35
  buildings = ['granary', 'shrine']
  leads = ['calendar', 'sailing', 'writing']
  tech_rq = ['agriculture']

class Sailing(Tech):
  name = sailing_t
  science_cost = 55
  improvements = ['fishing_boat']
  leads = ['optics']
  units = ['work_boat', 'galley']
  tech_rq = ['pottery']
  sea_works = 1

class The_Wheel(Tech):
  name = the_wheel_t
  science_cost = 55
  tech_rq = ['horseback_riding']

class Trapping(Tech):
  name = trapping_t
  science_cost = 55
  improvements = ['camp']
  leads = ['horseback_riding']
  units = ['hunters']
  reveal = ['ivory']
  tech_rq = ['animal_husbandry']

class Writing(Tech):
  name = writing_t
  science_cost = 55
  leads = ['philosophy', 'poetry']
  units = ['jarl', 'legatus', 'medicus']
  tech_rq = ['pottery']
  culture = 5

#Clasical era.
class Construction(Tech):
  name = construction_t
  science_cost = 105
  buildings = ['colosseum']
  improvements = ['lumber_mill']
  leads = ['engineering']
  tech_rq = ['masonry', 'the_wheel']
  units = ['composite_bowmen']

class Currency(Tech):
  name = currency_t
  science_cost = 175
#   buildings = ['market', 'mint', 'bazaar']
  leads = ['civil_service', 'guilds']
  tech_rq = ['mathematics']

class Engineering(Tech):
  name = engineering_t
  science_cost = 175
  buildings = ['aqueduct']
  improvements = ['fort']
  leads = ['machinery', 'metal_casting']
  tech_rq = ['construction', 'mathematics']

class Horseback_Riding(Tech):
  name = horseback_riding_t
  science_cost = 105
  buildings =['stable']
  leads = ['the_wheel']
  units = ['camel_archers', 'cataphracts', 'equites', 'horsemen']
  tech_rq = ['trapping']

class Iron_Working(Tech):
  name = iron_working_t
  science_cost = 195
  tech_rq = ['bronze_working']
  buildings = ['colossus']
  leads = ['metal_casting']
  units = ['hirdmen', 'hoplites', 'huskarl', 'immortals', 'principes', 'triarii', 
    'swordmen']

class Mathematics(Tech):
  name = mathematics_t
  science_cost = 105
  buildings = ['courthouse']
  leads = ['currency', 'engineering']
  tech_rq = ['the_wheel']
  units = ['catapult', 'ballista']

class Optics(Tech):
  name = optics_t
  science_cost = 85
  buildings = ['lighthouse']
  leads = ['compass']
  tech_rq = ['sailing']

class Philosophy(Tech):
  name = philosophy_t
  science_cost = 175
  buildings = ['oracle', 'temple']
  leads = ['theology']
  tech_rq = ['calendar', 'writing']
  

class Poetry(Tech):
  name = poetry_t
  science_cost = 175
  tech_rq = ['writing']
  leads = ['civil_service', 'theology']
#Medieval era.
class Chivalry(Tech):
  name = chivalry_t
  science_cost = 485
  buildings = ['castle']
#   leads = ['banking', 'printing_press']
  tech_rq = ['civil_service', 'guilds']
  units = ['knights']

class Civil_Service(Tech):
  name = civil_service_t
  science_cost = 275
  leads = ['education', 'chivalry']
  tech_rq = ['horseback_riding', 'currency', 'poetry']
  units = ['pikemen']

class Compass(Tech):
  
  name = compass_t
  science_cost = 375
  leads = ['astronomy']
  tech_rq = ['optics', 'theology']

class Education(Tech):
  name = education_t
  science_cost = 485
  buildings = ['university']
  leads = ['acoustics', 'banking', 'astronomy']
  tech_rq = ['civil_service', 'theology']

class Guilds(Tech):
  name = guilds_t
  science_cost = 275
  tech_rq = ['currency']

class Machinery(Tech):
  name = machinery_t
  science_cost = 485
#   leads = ['printing_press']
  tech_rq = ['engineering', 'guilds']
  units = ['cross_bowmen', 'long_bowmen']

class Metal_Casting(Tech):
  name = metal_casting_t
  science_cost = 275
  leads = ['physics', 'steel']
  tech_rq = ['engineering', 'iron_working']
  buildings = ['forge', 'workshop']

class Physics(Tech):
  name = physics_t
  science_cost = 485
#   leads = ['gunpowder', 'printing_press']
  tech_rq = ['metal_casting']
  units = ['trebuchet']

class Steel(Tech):
  name = steel_t
  science_cost = 485
#   buildings = ['armory']
#   leads = ['gunpowder']
  tech_rq = ['metal_casting']
  units = ['long_swordmen', 'samurai']
  

class Theology(Tech):
  name = theology_t
  science_cost = 274
  leads = ['education', 'compass']
  tech_rq = ['philosophy']
#Renaissance era.
class Acoustics(Tech):
  name = acoustics_t

class Archytecture(Tech):
  name = architecture_t
class Astronomy(Tech):
  name = astronomy_t
  science_cost = 150
  units = ['trireme']
  tech_rq = ['sailing', 'writing']

class Banking(Tech):
  name = banking_t

#Industrial era.
class Biology(Tech):
  name = biology_t
  science_cost = 2350
  reveal = ['oil']

class Industrialization(Tech):
  name = industrialization_t
  reveal = ['coal']

#Other.
class Electricity(Tech):
  name = electricity_t
  reveal = ['aluminum']

acoustics = Acoustics()
agriculture = Agriculture()
animal_husbandry = Animal_Husbandry()
archery = Archery()
astronomy = Astronomy()
banking = Banking()
biology = Biology()
bronze_working = Bronze_Working()
calendar = Calendar()
civil_service = Civil_Service()
chivalry = Chivalry()
compass = Compass()
construction = Construction()
currency = Currency()
education = Education()
engineering = Engineering()
guilds = Guilds()
horseback_riding = Horseback_Riding()
iron_working = Iron_Working()
mathematics = Mathematics()
machinery = Machinery()
masonry = Masonry()
metal_casting = Metal_Casting()
mining = Mining()
optics = Optics()
philosophy = Philosophy()
physics = Physics()
poetry = Poetry()
pottery = Pottery()
sailing = Sailing()
steel = Steel()
theology = Theology()
the_wheel = The_Wheel()
trapping = Trapping()
writing = Writing()

ancient_era = [agriculture, animal_husbandry, archery, bronze_working, 
  calendar, masonry, mining, pottery, sailing, the_wheel, trapping, writing]

clasical_era = [construction, currency, engineering, horseback_riding, iron_working, poetry, mathematics, optics, philosophy]

medieval_era = [chivalry, civil_service, compass, education, guilds, machinery, metal_casting, physics, steel, theology]

tech_tree = ancient_era+clasical_era+medieval_era
print('{} tecnologias'.format(len(tech_tree)))