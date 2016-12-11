# -*- encoding: utf-8 -*-
from pdb import Pdb
from languages.english import *


class Action:
  name = str()
  turns = 0
  maintenance = 0
  terrain = []
  subterrain = []
  hill = []
  in_friend = 0
  in_hostile = 0
  in_neutral = 0
  resource1 = []
  resource2 = []
  resource3 = []  
  
  food = 0
  production = 0
  gold = 0
  defense = 0
  b_commandpoints = 0
  
  def counter(self, position):
    count = 0
    for unit in position.civil+position.military:
      if unit.is_working: count += 1
      self.turns // count
  
  def done(self, position):
    position.food = self.food
    position.production = self.production
    position.gold = self.gold
    position.defense = self.defense
    position.b_commandpoints = self.b_commandpoints
    for unit in position.military+position.civil:
      if unit.is_working: unit.is_working = 0
    
  def start(self, position):
    if position.improvement == list():
      position.improvement = DC()
  def progress(self, position):
    for unit in position.military+position.civil:
      if unit.is_working: self.turns -= 1
      if self.turns < 0: self.turns = 0
  
class Building:
  is_building = 1
  name = None
  production_cost = 0
  cost = 0
  maintenance = 0
  heal = 0
  defense = 0
  stack = 0
  building_rq = list()
  buildings = list()
  improvements = list()
  units = list()
  leads = list()
  res_rq = list()
  tech_rq = list()
  obsolete_building = list()
  resource1 = list()
  resource2 = list()
  resource3 = list()
  
  science = 0
  culture = 0
  happiness = 0
  
  food = 0
  production = 0
  gold = 0
  def __init__(self):
    self.resources = self.resource1+self.resource2+self.resource3
  def requirements(self, player, city):
    blocked = 0
    needs = list()
    for res in self.res_rq:
      if res not in city.resources:
        needs.append(res)
        blocked = 1
    for improvement in self.improvements:
      if improvement not in city.improvements:
        needs.append(improvement)
        blocked = 1
    return blocked, needs
  
  def setself(self, player, city):
    pass

class City:
  name= None
  capital = 0
  coastalcity = 0
  location = None
  
  buildings = list()
  improvements = list()
  owns = list()
  
  culture = 0
  food = 0 
  gold = 0
  happiness = 0
  heal = 0
  is_working = 0
  nextpop = 20
  popgrowth = 0
  population = 1
  production = 0
  science = 0
  unhappiness = 0


class Improvement:
  name = None
  turns = 0
  maintenance = 0
  tech_rq = list()
  working = 0
  sound = ["buildconstruct1"]
  soundeffects = list()
  turns_m = turns
  in_progress = 1
  hitpoint = 100
  tech_rq = list()
  terrain = [0, 1, 2, 3, 4, 5, 6, 7, 8]
  subterrain = [-1, 0, 1, 2]
  hill = [0, 1]
  in_owns = 1
  in_friend = 0
  in_neutral = 0
  in_hostile = 0
  freeresources = 0
  resource1 = list()
  resource2 = list()
  resource3 = list()
  resources = list()
  resource = None
  food = 0
  production = 0
  gold = 0
  defense = 0
  def __init__(self):
    self.turns_m = self.turns
    self.resources = self.resource1+self.resource2+self.resource3
    if self.freeresources: self.resources.append(None)
  def addresource(self, player, pos):
    if pos.resource: self.resource = pos.resource
  def setself(self, pos):
    pass

class Event:
  name = ''
  turns = 0
  delete_unit = 0
  action = None

class Nation:
  name = None
  nameid = None
  commandpoints = 0
  plural = None
  actions = list()
  citynames = []
  initial_units = list()
  units = list()
  initial_buildings = list()
  buildings = list()

class Player():
  position = None
  ai = 0
  jobs = 0
  nomads = 0
  cities = list()
  enemies = list()
  friends = list()
  actions = list()
  seen = list()
  lastposition = list()
  nation = None
  player = None
  
  clear_forest = 0
  clear_jungle = 0
  sea_works = 0
  revealed = list()
  av_buildings = list()
  av_improvements = list()
  av_units = list()
  av_tech = list()
  initial_buildings = list()
  initial_units = list()
  improvements = list()
  units = list()
  researched = list()
  defense_bonus = 0
  heal_bonus = 0
  sizecap = 7
  pillage = 10
  ship_movemment = 0
  land_movemment = 0
  air_movemment = 0
  population = 0
  culture = 0
  culture_bonus = 0
  science = 0
  science_bonus = 0
  happiness = 0
  happiness_bonus = 0
  food = 0
  food_bonus = 0
  production = 0
  production_bonus = 0
  gold = 25
  income = 0
  outcome  = 0
  total = 0

class Resource:
  name = list()
  visible = 0
  enabled = 0
  soundeffects = list()
  terrain = [0, 1, 2, 3, 4, 5, 6, 7, 8]
  subterrain = [-1, 0, 1, 2]
  hill = [0, 1]
  food = 0
  production = 0
  gold = 0
  culture = 0
  happiness = 0

class Terrain:
  player = None
  name = None
  starter = 1
  sight = 0
  terrain = 7
  subterrain = -1
  hill = 0
  city = None
  improvement = None
  is_working = 0
  civil = list()
  military = list()
  resource = None
  
  culture = 0
  c_culture = 0
  total_culture = 0
  
  heal = 0
  s_heal = 0
  c_heal = 0
  h_heal = 0
  r_heal = 0
  u_heal = 0
  
  food = 0
  c_food = 0
  s_food = 0
  h_food = 0
  r_food = 0
  
  production = 0
  c_production = 0
  s_production = 0
  h_production = 0
  r_production = 0
  
  gold = 0
  c_gold = 0
  s_gold = 0
  h_gold = 0
  r_gold = 0
  
  defense = 0
  c_defense = 0
  s_defense = 0
  h_defense = 0
  r_defense = 0
  u_defense = 0
  
  stack = 2
  c_stack = 0
  s_stack = 0
  h_stack = 0
  r_stack = 0
  u_stack = 0
  
  tags = list()
  events = list()

class Tech:
  name = None
  visible = 0
  science_cost = 0
  maintenance = 0
  tech_rq = list()
  building_rq = list()
  buildings = list()
  improvements = list()
  leads = list()
  reveal = list()
  units = list()
  
  clear_forest = 0
  clear_jungle = 0
  sea_works = 0
  
  culture = 0
  science = 0
  happiness = 0
  food = 0
  production = 0
  gold = 0
  
  defense = 0
  compoints = 0
  heal = 0
  stack = 0
  
  def setself(self, player):
    for res in self.reveal: 
      res.visible = 1
    player.revealed += self.reveal
    if player.clear_jungle == 0 and self.clear_jungle == 1:
      player.clear_jungle = 1
    if player.clear_forest == 0 and self.clear_forest == 1:
      player.clear_forest = 1
    if player.sea_works == 0 and self.sea_works == 1:
      player.sea_works = 1

class Unit:
  name = None
  player = None
  ai = 0
  wait = 0
  
  production_cost = 0
  cost = 0
  food = 0 # food produced.
  food_cost = 0 # food needed.
  maintenance = 0 # can be upkeep.
  resources = list()
  number = 0
  level = 1
  xp = 0
  max_xp = 100
  
  actions = list()
  building = list()
  enemies = list()
  friends = list()
  improvements = list()
  tags = list()
  tech_rq = list()
  units = list
  upgrade = None
  
  can_captureunit = 0
  can_capturecity = 0
  can_combat = 0
  can_charge = 0
  charge = 0
  can_enslave = 0
  can_heal = 0
  heal_rate = 0
  can_fly = 0
  can_pillage = 0
  loot = 0
  can_sail = 0
  visible = 1
  stealth_rate = 0
  seen = 1
  sail_level = 0
  can_transport = 0
  commandpoints = 0
  b_commandpoints = 0
  can_walk = 0
  night_vision = 0

  is_building = 0  
  is_commander = 0
  is_ethereal = 0
  is_human = 0
  is_jungle = 0
  is_marsh = 0
  is_mechanical = 0
  is_mounted = 0
  is_ranged = 0
  is_ranger = 0
  is_settler = 0
  is_undead = 0
  is_unit = 1
  is_worker = 0
  is_working = 0
  
  bonus_ethereal = 0
  bonus_human = 0
  bonus_mechanical = 0
  bonus_mounted = 0
  bonus_ranged = 0
  bonus_undead = 0
  
  marange = 0
  corange = 0
  ranged_attacks = 0
  moves = 0
  hitpoint = 0
  heal_infriend = 0
  heal_inneutral = 0
  heal_inhostile = 0
  pre_precision = 0
  pre_strength = 0
  precision = 0
  strength= 0
  defense = 0
  protection = 0
  def __init__(self):
    if self.actions == list(): self.actions = list()
    self.building = list()
    if self.enemies == list(): self.enemies = list()
    self.explored = list()
    if self.friends == list(): self.friends = list()
    if self.improvements == list(): self.improvements = list()
    self.notes = list()
    self.moveto = list()
    self.moved = list()
    if self.tags == list(): self.tags = list()
    if self.tech_rq == list(): self.tech_rq = list()
    self.units = list()
    
    if self.can_sail:
      toadd = '{} {}'.format(sea_t, unit_t)
      self.notes.append(toadd)
    if self.can_walk:
      toadd = '{} {}'.format(land_t, unit_t) 
      self.notes.append(toadd)
    if self.is_human: self.notes.append(human_t)
    if self.is_ethereal: self.notes.append(ethereal_t)
    if self.is_mechanical: self.notes.append(mechanical_t)
    if self.is_mounted: self.notes.append(mounted_t)
    if self.can_charge: self.notes.append(can_charge_t)
    if self.is_undead: self.notes.append(undead_t)
    if self.can_combat and self.is_ranged == 0:
      self.notes.append(melee_t)
    if self.can_combat and self.is_ranged:
      self.notes.append(ranged_t)
    if self.can_combat == 0: self.notes.append(civil_t)
    if self.is_commander: self.notes.append(commander_t)
    
    if self.is_jungle: self.notes.append(jungle_t)
    if self.is_ranger: self.notes.append(ranger_t)
    if self.night_vision: self.notes.append(night_vision_t)
    
    if self.can_pillage: self.notes.append(pillage_t)
    if self.can_captureunit: self.notes.append(str(can_capture_t+' '+unit_t))
    if self.can_capturecity:
      toadd = '{} {} {}.'.format(can_t, capture_t, city_t) 
      self.notes.append(toadd)
    if self.is_settler:
      self.notes.append(settler_t)
    if self.is_worker:
      self.notes.append(worker_t)
    
    self.moves_m = self.moves 
    self.hitpoint_m = self.hitpoint
    self.delete = 0

class Civil(Unit):
  commandpoints = 0
  selected = ['generic_select1', 'generic_select2']
  sh = ['working1', 'working2', 'working3', 'working4', 'working5']
  hits = ["Melee_hits1", "Melee_hits2", "Melee_hits3"]
  block = ["Blk_wood1", "Blk_wood2", "Blk_wood3", "Blk_wood4", "Blk_wood5"]
  working = ['working1', 'working2', 'working3', 'working4', 'working5', 
    'working6', 'working7', 'working8', 'working9', 'working10', 'working11', 
    'working12', 'working13', 'working14', 'working15', 'working16', 'working17']

class Commander(Unit):
  is_commander = 1

class Land_Human_Unit(Unit):
  is_human = 1
  can_walk = 1
  commandpoints = 3 #Showld be deleted.
  selected = ['generic_select1', 'generic_select2']
  steps = ['walk_ft1']
  die = ["hum_diemalea1", "hum_diemalea2", "hum_diemalea3", "hum_diemalea4"]
  
  hitpoint = 100
  heal_infriend = 20
  heal_inhostile = 10
  heal_inneutral = 15
  moves = 2
  sight = 1

class Melee(Unit):
  can_combat = 1
  can_pillage = 1
  can_captureunit = 1
  can_capturecity = 1
  block = ["Blk_wood1", "Blk_wood2", "Blk_wood3", "Blk_wood4", "Blk_wood5"]
  hits = ["Melee_hits1", "Melee_hits2", "Melee_hits3"]
  sh = ["Melee_flesh_sh1", "Melee_flesh_sh2", "Melee_flesh_sh3"]

class Mounted(Unit):
  is_mounted = 1
  commandpoints = 4
  sh = ["Melee_flesh_sh1", "Melee_flesh_sh2", "Melee_flesh_sh3"]
  steps = ['walk_mt1', 'walk_mt2', 'walk_mt3', 'walk_mt4', 'walk_mt5']
  block = ["Blk_wood1", "Blk_wood2", "Blk_wood3", "Blk_wood4", "Blk_wood5"]
  hits = ["Melee_hits1", "Melee_hits2", "Melee_hits3"]
  hits_charge = ['melee_charge1', 'melee_charge2', 'melee_charge3']
  moves = 3

class Ranged(Unit):
  can_combat = 1
  can_pillage = 1
  can_captureunit = 1
  can_capturecity = 1
  is_ranged = 1
  corange = 2
  selected = ['rang_select1', 'rang_select2']
  sh = ["Arch_sh1", "Arch_sh2", "Arch_sh3"]
  hits = ["Arch_hits1", "Arch_hits2", "Arch_hits3", "Arch_hits4", "Arch_hits5",
    "Arch_hits6", "Arch_hits7", "Arch_hits8", "Arch_hits9"]
  block = ["Blk_wood1", "Blk_wood2", "Blk_wood3", "Blk_wood4", "Blk_wood5"]

class Sea_Unit(Unit):
  can_sail = 1
  sail_level = 0
  selected = ['generic_select1', 'generic_select2']
   
  die = ["hum_diemalea1", "hum_diemalea2", "hum_diemalea3", "hum_diemalea4"]
  steps = ["Mov1", "Mov2", "Mov3", "Mov4", "Mov5", "Mov6"]
  sh = ["Arch_sh1", "Arch_sh2", "Arch_sh3"]
  hits = ["Arch_hits1", "Arch_hits2", "Arch_hits3", "Arch_hits4", "Arch_hits5",
    "Arch_hits6", "Arch_hits7", "Arch_hits8", "Arch_hits9"]
  block = ["Blk_wood1", "Blk_wood2", "Blk_wood3", "Blk_wood4", "Blk_wood5"]

# Pdb().set_trace()