from pdb import Pdb
from data.classes import (Civil, Commander, Unit, Land_Human_Unit, Melee, 
  Mounted, Ranged, Sea_Unit)
from data.buildings import *
from data.improvements import *
from data.technologies import *
from data.settings import *

# Military units.
class Accensii(Melee, Land_Human_Unit):
  name = accensii_t
  production_cost = 30
  maintenance = 1
  precision = 6
  strength = 30
  defense = 5

class Archers(Ranged, Land_Human_Unit):
  name = archers_t
  production_cost = 16
  maintenance = 1
  tech_rq = [archery]
  upgrade = ['cross_bowmen']
  corange = 5
  precision = 6
  strength = 20
  defense = 4

class Astatii(Melee, Land_Human_Unit):
  name = astatii_t
  production_cost = 36
  maintenance = 1
  tech_rq = [bronze_working]
  resources = [copper]
  precision = 7
  strength = 20
  defense = 5
  protection = 5

class Ballista(Ranged, Land_Human_Unit):
  name = ballista_t
  production_cost = 80
  maintenance = 2
  tech_rq = [mathematics]
  hits = ['catp_hit1', 'catp_hit2']
  selected = ['catp_select1', 'catp_select2']
  sh = ['catp_sh1', 'catp_sh2']
  steps = ['walk_catp1', 'walk_catp2', 'walk_catp3']

class Druid(Civil, Land_Human_Unit):
  name = druid_t
  production_cost = 24
  maintenance = 1
  building = [shrine]
  is_forest = 1
  is_jungle = 1  
  heal = 10
  moves = 2

class Camel_Archers(Mounted, Ranged, Land_Human_Unit):
  name = camel_archers_t
  production_cost = 42
  maintenance = 1
  food_cost = 0.5
  
  tech_rq = [archery, horseback_riding]
  sh = ["Arch_sh1", "Arch_sh2", "Arch_sh3"]
  hits = ["Arch_hits1", "Arch_hits2", "Arch_hits3", "Arch_hits4", "Arch_hits5",
    "Arch_hits6", "Arch_hits7", "Arch_hits8", "Arch_hits9"]
  resources = [camel]
  corange = 4
  precision = 6
  strength = 30
  defense = 5

class Cataphracts(Mounted, Melee, Land_Human_Unit):
  name = cataphracts_t
  production_cost = 90
  maintenance = 4
  food_cost = 1
  
  tech_rq = [horseback_riding]
  can_charge = 1
  bonus_ranged = 30
  resourses = [horses, iron]
  moves = 2
  precision = 8
  strength = 40
  defense = 4
  protection = 10

class Catapult(Ranged, Land_Human_Unit):
  name = catapult_t
  production_cost = 80
  maintenance = 2
  tech_rq = [mathematics]
  hits = ['catp_hit1', 'catp_hit2']
  selected = ['catp_select1', 'catp_select2']
  sh = ['catp_sh1', 'catp_sh2']
  steps = ['walk_catp1', 'walk_catp2', 'walk_catp3']
  
  marange = 1
  ranged_attacks = 1
  hitpoint = 100
  moves = 2
  precision = 3
  strength = 20
  defense = 1

class Composite_Bowmen(Ranged, Land_Human_Unit):
  name = composite_bowmen_t
  production_cost = 40
  maintenance = 1
  tech_rq = [construction]
  upgrade = ['cross_bowmen']
  corange = 7
  precision = 6
  strength = 20
  defense = 3

class Cross_Bowmen(Ranged, Land_Human_Unit):
  name = cross_bowmen_t
  production_cost = 58
  maintenance = 1
  tech_rq = [machinery]
  corange = 3
  precision = 8
  strength = 30
  defense = 2 

class Equites(Mounted, Melee, Land_Human_Unit):
  name = equites_t
  production_cost = 70
  maintenance = 3
  food_cost = 1
  
  tech_rq = [horseback_riding]
  can_charge = 1
  bonus_ranged = 10
  resources = [horses, copper]
  precision = 8
  strength = 40
  defense = 4
  protection = 5

class Galley(Sea_Unit):
  name = galley_t
  production_cost = 50
  maintenance = 2
  tech_rq = [sailing]
  is_mechanical = 1
  can_combat = 1
  can_pillage = 1
  can_transport = 1
  stack = 2
  
  moves = 3
  hitpoint = 100
  precision = 9
  strength = 240

class Horsemen(Mounted, Melee, Land_Human_Unit):
  name = horsemen_t
  production_cost = 60
  maintenance = 2
  food_cost = 1
  
  tech_rq = [horseback_riding]
  resources = [copper, horses]
  can_charge = 1
  moves = 3
  precision = 7
  strength = 30
  defense = 5

class Horse_Archers(Mounted, Ranged, Land_Human_Unit):
  name = horsearchers_t
  production_cost = 58
  maintenance = 2
  food_cost = 1
  
  tech_rq = [archery, horseback_riding]
  sh = ["Arch_sh1", "Arch_sh2", "Arch_sh3"]
  hits = ["Arch_hits1", "Arch_hits2", "Arch_hits3", "Arch_hits4", "Arch_hits5",
    "Arch_hits6", "Arch_hits7", "Arch_hits8", "Arch_hits9"]
  resources = [horses]
  corange = 5
  precision = 6
  strength = 20
  defense = 6

class Hirdmen(Melee, Land_Human_Unit):
  name = hirdmen_t
  production_cost = 30
  maintenance = 1
  building = [thingvellir]
  tech_rq = [iron_working]
  bonus_ranged = 10
  resources = [copper]
  precision = 8
  strength = 30
  defense = 6
  protection = 15

class Hoplites(Melee, Land_Human_Unit):
  name = hoplites_t
  production_cost = 50
  maintenance = 3
  building = [barracks]
  tech_rq =[iron_working]
  bonus_mounted = 20
  bonus_ranged = 30
  resources = [iron]
  precision = 9
  strength = 40
  defense = 6
  protection = 10

class Hunters(Ranged, Land_Human_Unit):
  name = hunters_t
  production_cost = 14
  maintenance = 1
  tech_rq = [trapping]
  die = ["hum_diemaleb1", "hum_diemaleb2", "hum_diemaleb3"]
  is_jungle = 1
  is_ranger = 1
  night_vision = 1
  corange = 3
  precision = 6
  strength = 20
  defense = 7

class Huskarl(Melee, Land_Human_Unit):
  name = huskarl_t
  production_cost = 55
  maintenance = 2
  building = [thingvellir]
  tech_rq = [iron_working]
  bonus_ranged = 20
  bonus_mounted = 10
  resources = [iron]
  precision = 8
  strength = 40
  defense = 6
  protection = 15

class Immortals(Melee, Land_Human_Unit):
  name = immortals_t
  production_cost = 66
  maintenance = 3
  building = [barracks]
  tech_rq = [iron_working]
  bonus_ranged = 20
  resources = [iron]
  precision = 9
  strength = 36
  defense =3
  protection = 5

class Jarl(Commander, Land_Human_Unit):
  name = jarl_t
  production_cost = 50
  maintenance = 2
  building = [thingvellir]
  tech_rq = [writing]
  compoints = 2

class Knights(Mounted, Melee, Land_Human_Unit):
  name = knights_t

class Lasbogar(Archers):
  name = lasbogar_t
  production_cost = 20
  maintenance = 1
  tech_rq = [archery]
  upgrade = ['cross_bowmen']
  corange = 5
  precision = 6
  strength = 20
  defense = 4

class Legatus(Commander, Land_Human_Unit):
  name = legatus_t
  production_cost = 55
  maintenance = 3
  building = [barracks]
  tech_rq = [writing]
  compoints = 3

class Long_Bowmen(Ranged, Land_Human_Unit):
  name = long_bowmen_t
  production_cost = 42
  tech_rq = [machinery]
  upgrade = ['cross_bowmen']
  maintenance = 1
  tech_rq = [archery]
  corange = 8
  precision = 6
  strength = 20
  defense = 3

class Long_Swordmen(Melee, Land_Human_Unit):
  name = longswordmen_t

class Medicus(Civil, Land_Human_Unit):
  name = medicus_t
  production_cost = 30
  maintenance = 1
  tech_rq = [writing]
  heal = 20

class Pikemen(Melee, Land_Human_Unit):
  name = pikemen_t
  production_xost = 40
  maintenance = 2
  building = [barracks]
  tech_rq = [civil_service]
  bonus_mounted = 30
  resources = [iron]
  precision = 6
  strength = 40
  defense = 2
  protection = 10

class Principes(Melee, Land_Human_Unit):
  name = principes_t
  production_cost = 45
  maintenance = 3
  building = [barracks]
  tech_rq = [iron_working]
  bonus_ranged = 20
  bonus_mounted = 10
  resources = [iron]
  precision = 9
  strength = 30
  defense = 4
  protection = 15

class Raiders(Melee, Land_Human_Unit):
  name = raiders_t
  production_cost = 16
  maintenance = 1
  can_captureunit = 0
  is_ranger = 1
  is_jungle = 1
  night_vision = 1
  precision = 6
  strength = 20
  defense = 3

class Rangers(Ranged, Land_Human_Unit):
  name = rangers_t
  production_cost = 22
  maintenance = 1
  tech_rq = [archery]
  is_ranger = 1
  is_jungle = 1
  night_vision = 1
  corange = 6
  precision =6
  strength = 20
  defense = 6
  protection = 5

class Samurai(Melee, Land_Human_Unit):
  name = samurai_t

class Sagittarii(Ranged, Land_Human_Unit):
  name = sagittarii_t
  production_cost = 25
  maintenance = 1
  tech_rq = [archery]
  corange = 5
  precision = 6
  strength = 20
  defense = 3

class Settler(Civil, Land_Human_Unit):
  name = settler_t
  production_cost = 60
  maintenance = 1
  food_cost = 0.5
  actions = ["Start City"]
  
  
  tech_rq = [agriculture]
  is_settler = 1

class Scouts(Civil, Land_Human_Unit):
  name = scouts_t
  production_cost = 10
  maintenance = 1
  moves = 2
  is_jungle = 1
  is_ranger = 1

class Skutilsveinr(Mounted, Melee, Land_Human_Unit):
  name = skutilsveinr_t
  production_cost = 60
  maintenance = 2
  tech_rq = [horseback_riding]
  can_charge = 1
  bonus_ranged = 30
  resources = [horses, copper]
  precision = 8
  strength = 40
  defense = 4
  protection = 10

class Spearmen(Melee, Land_Human_Unit):
  name = spearmen_t
  production_cost = 36
  maintenance = 2
  tech_rq =[bronze_working] 
  bonus_mounted = 10
  resources = [copper]
  precision = 7
  strength = 40
  defense = 6
  protection = 10

class Swordmen(Melee, Land_Human_Unit):
  name = swordmen_t
  production_cost = 42
  maintenance = 1
  tech_rq =[iron_working]
  bonus_ranged = 30
  resources = [iron]
  precision = 7
  strength = 30
  defense = 5
  protection = 5

class Trebuchet(Ranged, Land_Human_Unit):
  name = trebuchet_t
  production_cost = 120
  maintenance = 2
  tech_rq = [physics]
  hits = ['catp_hit1', 'catp_hit2']
  selected = ['catp_select1', 'catp_select2']
  sh = ['catp_sh1', 'catp_sh2']
  steps = ['walk_catp1', 'walk_catp2', 'walk_catp3']
  marange = 1
  ranged_attacks = 1
  hitpoint = 100
  moves = 2
  precision = 3
  strength = 40
  defense = 1

class Triarii(Melee, Land_Human_Unit):
  name = triarii_t
  production_cost = 49
  maintenance = 3
  building = [barracks]
  tech_rq =[civil_service]
  bonus_mounted = 40
  bonus_ranged = 30
  resources = [iron]
  precision = 9
  strength = 60
  defense = 6
  protection = 15

class Warriors(Melee, Land_Human_Unit):
  name = warriors_t
  production_cost = 16
  maintenance = 1
  food_cost = 0.5
  
  is_ranger = 1
  is_jungle = 1
  night_vision = 1
  moves = 2
  precision = 8
  strength = 20
  defense = 4

class War_Elephants(Mounted, Land_Human_Unit):
  name = war_elephants_t
  production_cost = 90
  maintenance = 3
  tech_rq =[horseback_riding]
  can_combat = 1
  can_charge = 1
  resources =[iron, ivory]
  hitpoint = 120
  moves = 2
  precision = 8
  strength = 50
  defense = 3
  protection = 10

#Civil Units.
class Worker(Civil, Land_Human_Unit):
  name = worker_t
  production_cost = 45
  maintenance = 1
  improvements = [camp, farm, fort, fishing_boat, mine, lumber_mill, 
    offshore_platform, oil_weel, pasture, plantation, quarry, trading_post, ]
  tech_rq = [agriculture]
  can_combat = 0
  is_worker = 1
  moves = 2

# Naval units.
class Work_Boat(Sea_Unit):
  name = work_boat_t
  production_cost = 45
  maintenance = 1
  is_mechanical = 1
  tech_rq = ['sailing']
  
  moves = 2
  hitpoint = 60


class Trireme(Sea_Unit):
  name = trireme_t
  production_cost = 60
  maintenance = 2
  is_mechanical = 1
  can_combat = 1
  sail_level = 1
  is_ranged = 1
  
  corange = 5
  moves = 3
  moves_m = 3
  hitpoint = 150
  hitpoint_m = 150
  precision = 7
  strength = 60

# Units vars.
accensii = Accensii()
archers = Archers()
astatii = Astatii()
ballista = Ballista()
camel_archers = Camel_Archers()
cataphracts = Cataphracts()
catapult = Catapult()
composite_bowmen = Composite_Bowmen()
cross_bowmen = Cross_Bowmen()
druid = Druid()
equites = Equites()
galley = Galley()
hirdmen = Hirdmen()
hoplites = Hoplites()
horsemen = Horsemen()
horse_archers = Horse_Archers()
hunters = Hunters()
huskarl = Huskarl()
immortals = Immortals()
jarl = Jarl()
knights = Knights()
lasbogar = Lasbogar()
legatus = Legatus()
long_bowmen = Long_Bowmen()
long_swordmen = Long_Swordmen()
medicus = Medicus()
pikemen = Pikemen()
principes = Principes()
raiders = Raiders()
rangers = Rangers()
samurai = Samurai()
sagittarii = Sagittarii()
scouts = Scouts()
settler = Settler()
skutilsveinr = Skutilsveinr()
spearmen = Spearmen()
swordmen = Swordmen()
trebuchet = Trebuchet()
triarii = Triarii()
trireme = Trireme()
warriors = Warriors()
war_elephants = War_Elephants()
work_boat = Work_Boat()
worker = Worker()

landunits = [accensii, astatii, archers, ballista, druid, camel_archers,     
  cataphracts, catapult, composite_bowmen, cross_bowmen, equites, horsemen,     
  horse_archers, hirdmen, hoplites, huskarl, hunters, immortals, jarl,       
  lasbogar, legatus, long_bowmen, long_swordmen, medicus, pikemen, principes,      
  rangers, sagittarii, scouts, settler, skutilsveinr, spearmen, swordmen,  
  trebuchet, triarii, warriors, war_elephants, worker,]

seaunits = [galley, trireme, work_boat]

unitslist = landunits+seaunits
print('{} unidades'.format(len(unitslist)))
# Pdb().set_trace()