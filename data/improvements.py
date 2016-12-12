# -*- encoding: utf-8 -*-
from pdb import Pdb
from data.classes import Improvement, Resource
from data.settings import *
from data.technologies import *

#Resources.
class Aluminum(Resource):
  name = aluminum_t
  terrain = [0, 1, 3]
  hill = [1]
  production = 3

class Bananas(Resource):
  name = bananas_t
  visible = 1
  enabled = 1
  subterrain = [1]
  hill = [0]
  food = 1

class Camel(Resource):
  name = camel_t
  terrain = [0]
  subterrain = [-1]
  hill = [0, 1]
  food = 1
  

class Cattle(Resource):
  name = cattle_t
  visible = 1
  enabled = 1
  soundeffects = ['cow1', 'cow2', 'cow3', 'cow4', 'cow5', 'bull1', 'bull2', 
    'bull3', 'bull4', 'bull5', 'bull6']
  terrain = [2]
  subterrain = [-1]
  hill = [0]
  food = 1

class Cocoa(Resource):
  name = cocoa_t
  visible = 1
  enabled = 1
  subterrain = [1]
  hill = [0]
  food = 1
  gold = 1

class Coffe(Resource):
  name = coffe_t
  visible = 1
  enabled = 1
  subterrain = [1]
  hill = [0]
  food = 1
  gold = 1 

class Coal(Resource):
  name = coal_t
  terrain = [1, 2]
  subterrain = [-1, 0, 1]
  production = 1

class Copper(Resource):
  name = copper_t
  visible = 1
  enabled = 1
  terrain = [0, 1, 2, 3, 4]
  gold = 2

class Crab(Resource):
  name = crab_t
  visible = 1
  enabled = 1
  terrain = [6]
  food = 1
  gold = 1

class Cotton(Resource):
  name = cotton_t
  visible = 1
  enabled = 1
  terrain = [0, 1, 2]
  subterrain = [0, 1, 2]
  hill = [0]
  gold = 2

class Deer(Resource):
  name = deer_t
  visible = 1
  enabled = 1
  terrain = [3]
  hill = [0]
  food = 1

class Dyes(Resource):
  name = dyes_t
  visible = 1
  enabled = 1
  terrain = [0, 1, 2, 3]
  subterrain = [-1, 0, 1]
  hill = [0]
  gold = 2

class Fish(Resource):
  name = fish_t
  visible = 1
  enabled = 1
  terrain = [6]
  food = 1

class Gems(Resource):
  name = gems_t
  visible = 1
  enabled = 1
  terrain = [0, 1, 2]
  hill = [1]
  gold = 3

class Gold(Resource):
  name = gold_t
  terrain = [0, 1, 2, 3]
  gold = 5

class Horses(Resource):
  name = horses_t
  terrain = [1, 2, 3]
  subterrain = [-1, 0]
  hill = [0]
  production = 1

class Incense(Resource):
  name = incense_t
  visible = 1
  enabled = 1
  terrain = [0, 1, 2]
  subterrain = [-1, 0]
  hill = [0]
  terrain = [1, 2]
  gold = 2

class Iron(Resource):
  name = iron_t
  terrain = [0, 1, 2, 3, 4]
  subterrain = [-1, 0]
  hill = [0, 1]
  production = 1

class Ivory(Resource):
  name = ivory_t
  visible = 1
  enabled = 1
  terrain = [0, 1, 2]
  subterrain = [-1, 0]
  hill = [0]
  gold = 2

class Marble(Resource):
  name = marble_t
  visible = 1
  enabled = 1
  terrain = [0, 1, 3, 4]
  subterrain = [-1]
  hill = [1]
  production = 2

class Oil(Resource):
  name = oil_t
  terrain = [0, 1, 3, 4, 6]
  subterrain = [-1, 0, 1, 2]
  production = 1

class Pearl(Resource):
  name = pearl_t
  visible = 1
  enabled = 1
  terrain = [6]
  gold = 2

class Salt(Resource):
  name = salt_t
  visible = 1
  enabled = 1
  terrain = [0, 1, 3]
  food = 1
  gold = 1

class Silver(Resource):
  name = silver_t
  visible = 1
  enabled = 1
  terrain = [0, 1, 3]
  hill = [1]
  gold = 2

class Sheep(Resource):
  name = sheep_t
  visible = 1
  enabled = 1
  terrain = [0, 1]
  hill = [1]
  food = 1

class Shugar(Resource):
  name = shugar_t
  visible = 1
  enabled = 1
  terrain = [1, 2]
  subterrain = [-1, 1, 2]
  hill = [0]
  gold = 2

class Stone(Resource):
  name = stone_t
  visible = 1
  enabled = 1
  terrain = [0,  1, 2, 3, 4]
  hill = [1]
  production = 1

class Uranium(Resource):
  name = uranium_t
  visible = 0
  terrain = [0, 1, 3, 4]

class Whales(Resource):
  name = whales_t
  visible = 1
  enabled = 1
  terrain = [6]
  food = 1
  gold = 1

class Wheat(Resource):
  name = wheat_t
  visible = 1
  enabled = 1
  terrain = [0, 1, 2]
  subterrain = [-1, 1]
  hill = [0]
  food = 1

class Wine(Resource):
  name = wine_t
  terrain = [1, 2]
  subterrain = [-1]
  hill = [0]
  gold = 2


aluminum = Aluminum()
bananas = Bananas()
camel = Camel()
cattle = Cattle()
cocoa = Cocoa()
coffe = Coffe()
coal = Coal()
crab = Crab()
cotton = Cotton()
copper = Copper()
deer = Deer()
dyes = Dyes()
fish = Fish()
gems = Gems()
gold = Gold()
horses = Horses()
incense = Incense()
iron = Iron()
ivory = Ivory()
marble = Marble()
oil = Oil()
pearl = Pearl()
salt = Salt()
silver = Silver()
sheep = Sheep()
shugar = Shugar()
stone = Stone()
uranium = Uranium()
whales = Whales()
wheat = Wheat()
wine = Wine()


# Improvemments.
class Camp(Improvement):
  name = camp_t
  turns = 3
  tech_rq = [trapping]
  resource1 = [deer]
  resource2 = [ivory,]
  def setself(self, pos):
    if pos.resource in self.resource1:
      self.production = 1
    if pos.resource in self.resource2:
      self.gold = 1
 
class Farm(Improvement):
  name = farm_t
  turns = 3
  tech_rq = [agriculture]
  sound = ["cow1", "cow2", "cow3"]
  terrain = [0, 1, 2]
  subterrain = [-1]
  hill = [0]
  tile_owned = [0]
  freeresources = 1
  resource1 = [wheat]
  food = 1

class Fort(Improvement):
  name = fort_t
  turns = 10
  tech_rq = [engineering]
  terrain = [0, 1, 2, 3, 4]
  subterrain = [-1, 0, 1]
  in_friend = 1
  in_neutral = 1
  freeresources = 1
  defense = 25
 
class Fishing_boat(Improvement):
  name = fishing_boat_t
  turns = 2
  tech_rq = [sailing]
  terrain = [6]
  resource1 = [crab, fish, pearl, whales]
  food = 1
 
class Mine(Improvement):
  name = mine_t
  turns = 4
  tech_rq =[mining]
  terrain = [0, 1, 2, 3, 4]
  subterrain = [-1]
  hill = [0, 1]
  freeresources = 1
  resource1 = [gold, silver]
  resource2 = [salt]
  resource3 = [aluminum, coal, copper, iron, ]
  def setself(self, pos):
    if pos.resource in self.resource2:
      self.food = 1
      self.production = 2
    else:
      self.production = 1
 
class Lumber_Mill(Improvement):
  name = lumber_mill_t
  turns = 3
  tech_rq =[construction]
  subterrain = [1]
  production = 1
 
class Offshore_Platform(Improvement):
  name = offshore_platform_t
  turns = 8
  tech_rq = [biology]
  resource1 = [oil]
  production = 3
 
class Oil_Weel(Improvement):
  name = oil_weel_t
  turns = 8
  tech_rq =[biology]
  resource1 = [oil]
  production = 3

class Pasture(Improvement):
  name = pasture_t
  turns = 2
  tech_rq = [animal_husbandry]
  resource1 = [cattle, horses]
  resource2 = [camel, sheep]
  def setself(self, pos):
    if pos.resource in self.resource1:
      self.production = 1
    if pos.resource in self.resource2:
      self.food = 1

class Plantation(Improvement):
  name = plantation_t
  turns = 4
  tech_rq = [calendar]
  terrain =[0, 1, 2]
  subterrain = -1
  resource1 = [bananas]
  resource2 = [cocoa, coffe, cotton, dyes, incense, shugar, wine]
  def setself(self, pos):
    if pos.resource in self.resource1:
      self.food = 2
      self.production = -1
    if pos.resource in self.resource2:
      self.gold = 1

class Quarry(Improvement):
  name = quarry_t
  turns = 4
  tech_rq = [masonry]
  resource1 = [stone, marble]
  production = 1
  gold = 1

class Trading_Post(Improvement):
  name = trading_post_t
  turns = 6
  tech_rq = [guilds]
  
  terrain = [0, 1, 2, 3]
  subterrain = [-1, 0, 1]
  gold = 1

# Improvemments vars.
camp = Camp()
farm = Farm()
fishing_boat = Fishing_boat() 
fort = Fort()
mine = Mine()
lumber_mill = Lumber_Mill()
offshore_platform = Offshore_Platform()
oil_weel = Oil_Weel()
pasture = Pasture()
plantation = Plantation()
quarry = Quarry() 
trading_post = Trading_Post()

bonuses = [bananas, cattle, deer, fish, sheep, whales, wheat]
luxury = [cocoa, crab, coffe, cotton, dyes, gems, gold, incense, ivory, marble, 
  pearl, salt, silver, shugar, wine]
strategic = [aluminum, coal, copper, iron, horses, oil, stone, uranium]
resource_list = bonuses+luxury+strategic
for res in resource_list:
  if res in bonuses: res.type = 2
  if res in luxury: res.type = 1
  if res in strategic: res.type = 0

land_improvements = [camp, farm, fort, mine, lumber_mill, pasture]
land_improvements += [plantation, quarry, trading_post]
water_improvements = [fishing_boat, offshore_platform, oil_weel]
improvements_list = land_improvements+water_improvements

print('{} recursos'.format(len(resource_list)))