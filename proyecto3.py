# -*- encoding: utf-8 -*-
from copy import deepcopy as DC
from datetime import datetime
from decimal import *
from glob import glob
import logging
from math import ceil, floor
from operator import itemgetter, attrgetter
import os
from pdb import Pdb
from pickle import dump, dumps, load, loads
import pickle
from random import choice, randint, uniform, shuffle
import sys
from time import sleep

import pygame
from pygame.time import get_ticks as ticks

import accessible_output2 as ao2

exec('from data.classes import Player, Terrain, City')
exec('from data.nations import *')
exec('from data.settings import *')

for i in ao2.get_output_classes():
  if i.name == speaker: sp = i()

pygame.display.set_mode((800, 600))
pygame.mixer.pre_init(44100, -16, 2, 300)
pygame.init()
pygame.mixer.set_num_channels(60)

pickle.DEFAULT_VERSION = 4
getcontext().prec = 5
sounds = os.getcwd()+str("/sounds/")
wav = ".wav"
ogg = ".ogg"
mp3 = ".mp3"
mixer = pygame.mixer
Load = mixer.Sound

explorekeys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]

infokeys = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t,
  pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_z, 
  pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_KP5, pygame.K_HOME, 
  pygame.K_END, pygame.K_PAGEUP, pygame.K_PAGEDOWN] 


menukeys = [pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, 
  pygame.K_F10]

movementkeys = [pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, pygame.K_KP4,
  pygame.K_KP6, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3] 

shiftkeys = [pygame.K_LSHIFT, pygame.K_RSHIFT]

builderkeys = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t,
  pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g,
  pygame.K_z, pygame.K_x, pygame.K_y]

waterkeys = [pygame.K_z, pygame.K_x, pygame.K_y]

landkeys = builderkeys
landkeys = [i for i in landkeys if i not in waterkeys]

citytime1 = ticks()
citytime2 = ticks()
city_count1 = 2000
city_count2 = 2000
generictime = ticks()
genericcount = 1000
resbase = ticks()
rescount = 2000
unitbase = ticks()
unitcount = 0
windtime1 = ticks()
wind_count1 = randint(1000, 10000)
windtime2 = ticks()
wind_count2 = randint(1000, 10000)

terrains = [desert_t, plains_t, grassland_t, tundra_t, snow_t, mountain_t,
  coast_t, ocean_t, ice_t]

subterrains  = [forest_t, jungle_t, marsh_t]

land = [0, 1, 2, 3, 4, 5, 8]
water = [6, 7, 8]


# Channels.
ch1 = pygame.mixer.Channel(1) # errn1
ch2 = pygame.mixer.Channel(2) # errn2
ch3 = pygame.mixer.Channel(3) # tile owner.
ch4 = pygame.mixer.Channel(4) # tile units  
ch5 = pygame.mixer.Channel(5) # Reserved.
ch10 = pygame.mixer.Channel(10)
ch11 = pygame.mixer.Channel(11)
ch12 = pygame.mixer.Channel(12)
ch13 = pygame.mixer.Channel(13)
ch14 = pygame.mixer.Channel(14)
ch15 = pygame.mixer.Channel(15)
ch16 = pygame.mixer.Channel(16)
ch19 = pygame.mixer.Channel(19) #Fog.

ch20 = pygame.mixer.Channel(20) # Desert.
ch21 = pygame.mixer.Channel(21) # Plains.
ch22 = pygame.mixer.Channel(22) # Grassland.
ch23 = pygame.mixer.Channel(23) # Tundra.
ch24 = pygame.mixer.Channel(24) # Snow.
ch25 = pygame.mixer.Channel(25) # Mountain.
ch26 = pygame.mixer.Channel(26) # Coast.
ch27 = pygame.mixer.Channel(27) # Mountain.
ch28 = pygame.mixer.Channel(28) # Ice.

ch30 = pygame.mixer.Channel(30) # Forest.
ch31 = pygame.mixer.Channel(31) # Jungle.
ch32 = pygame.mixer.Channel(32) # Marsh.
ch39 = pygame.mixer.Channel(39) # generic effects.

ch40 = pygame.mixer.Channel(40) # Unit.
ch41 = pygame.mixer.Channel(41) # Resource.
ch45 = pygame.mixer.Channel(45) # Wind effect1.
ch46 = pygame.mixer.Channel(46) # Wind effect2.

ch50 = pygame.mixer.Channel(50) # City.
ch51 = pygame.mixer.Channel(51) # City effect 1.
ch52 = pygame.mixer.Channel(51) # City effect 2.
channels1 = [ch20, ch21, ch22, ch23, ch24, ch25, ch26, ch27, ch28]
channels2 = [ch30, ch31, ch32]
channels3 = [ch39, ch40, ch41, ch45, ch46, ch50, ch51, ch52]
channels = channels1+channels2+channels3


def add_city(player, position):
  position.city = City()
  square = setplace(position, value=1, action='return')
  for sq in square:
    if sq.terrain in [6, 7, 8]:
      position.city.coastalcity = 1
  city = position.city
  position.culture = 100
  
  city.location = wmap.index(player.position)
  city.buildings = list()
  city.improvements = list()
  city.owns = list()
  city.queue = list()
  city.resources = list()
  capital = 1
  if player.cities:
    for ct in player.cities:
      if ct.capital: capital = 0
  city.capital = capital
  city.name = player.citynames.pop(0)
  position.name = position.city.name
  position.player = player.player
  city.player = player.player
  player.cities.append(city)
  
  if capital:
    for i in player.initial_buildings:
      city.buildings.append(i)    
  
  cityholdings = setplace(player.position, value=1, action="return")
  for i in cityholdings:
    city.owns.append(i)
    i.name = city.name
    i.player = player.player

def add_improvement(improvement, position):
  position.improvement = DC(improvement)
  position.improvement.setself(position)

def add_omad(pos, unit):
  unit.ai = 1
  unit.player = 'Nomads'
  unit.friend = ['Nomads']
  unit.location = wmap.index(pos)
  pos.military.append(DC(unit))

def add_unit(player, position, unit):
  toadd = DC(unit)
  if toadd.can_transport: 
    toadd.units= list()
  
  toadd.player = player.player
  toadd.ai = player.ai
  toadd.friends = player.friends
  toadd.enemies = player.enemies
  toadd.location = wmap.index(position)
  if unit.can_sail == 0 and unit.is_mechanical == 0: 
    if unit.can_combat: 
      position.military.append(toadd)
    elif unit.can_combat == 0: 
      position.civil.append(toadd)
    units = position.civil+position.military
  if position.terrain in water and unit.can_sail and unit.is_mechanical:
    if toadd.can_combat: position.military.append(toadd)
    if toadd.can_combat == 0: position.civil.append(toadd) 
    position.civil.append(toadd)
  if position.terrain not in water and unit.can_sail and unit.is_mechanical:
    position.civil.append(toadd)
  player.units.append(toadd)

def start_improvement(improvement, position, unit):
  unit.is_working = 1
  loadsound(choice(improvement.sound))
  loadsound(choice(unit.working))
  add_improvement(improvement, position) 

def ai_move():
  global checknext, players, position, tipo, tomove
  player = players[num]
  checknext = None
  for unit in player.units:
    # If movement orders.
    if unit.moveto:
      limit = ticks()
      tomove = unit
      while tomove.moves > 0 and tomove.moveto:
        if ticks() > limit+20000:
          sp.speak('agotado')
          Pdb().set_trace()
        
        set_movement()
    
    # If no movement orders.
    
    if unit.ai:
      sp.speak('solo ai')
      limit = ticks()
      tomove = unit
      while tomove.moves > 0 and tomove.wait == 0:
        if ticks() > limit+100:
          sp.speak('agotado')
          Pdb().set_trace()
        
        position = wmap[unit.location]
        if unit.moves and unit.can_pillage:
          set_pillage(player, unit)
        if unit.hitpoint*unit.hitpoint_max//100 < 50:
          break
        if unit.moves:
          square = setplace(position, value=1, action='return')
          square = [sq for sq in square if sq not in unit.explored]
  #         sp.speak(len(square))
  #         sleep(0.3)
          if unit.can_sail == 0:
            square = [sq for sq in square if sq.terrain not in [6, 7, 8]]
          if unit.can_fly == 0:
            square = [sq for sq in square if sq.terrain != 5]
          
          shuffle(square)
          populated = [sq for sq in square if sq.player]
          if populated:
            sp.speak('hay populated')
            checknext = choice(populated)
          if populated == list() and square:
            sp.speak('no hay populated') 
            checknext = choice(square)
          if populated == list() and square == list():
            sp.speak('no hay nada')
            unit.explored = list()
          
          if checknext:
            sp.speak('hay checknext')
            tomove = unit
            tipo = position.military
            setmove()

def ai_move1():
  global checknext, players, position, tipo, tomove
  player = players[num]
  for unit in player.units:
    position = wmap[unit.location]
    if unit.moves and unit.can_pillage:
      if position.player not in player.friends and position.improvement and position.improvement.turns == 0:
        set_pillage(player, unit)
        
    if unit.moves:
      square = setplace(position, value=1, action='return')
      if unit.can_sail == 0:
        square = [sq for sq in square if sq.terrain not in [6, 7, 8]]
      if unit.can_fly == 0:
        square = [sq for sq in square if sq.terrain != 5]
      checknext = choice(square)
      tomove = unit
      tipo = position.military
      setmove()

def asking(warning, sound=1):
  loadsound('back3')
  if sound == 0: 
    for i in channels: i.fadeout(300)
  tospeak = [no_t, yes_t]
  say=1
  x=0
  sleep(0.5)
  sp.speak(warning,1)
  sleep(0.2)
  while True:
    sleep(0.2)
    if sound: playsound(position)
    if say:
      say = 0
      sp.speak(tospeak[x])
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        x = selector(tospeak, x, go="up")
        say = 1
      if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        x = selector(tospeak, x, go="down")
        say = 1  
        
      if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        loadsound('back1')
        return x
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        x = 0
        loadsound('back1')
        return x
        

def get_attrition(pos, player):
  units = list()
  food_cost = 0
  food = 0
  for unit in pos.military+pos.civil:
    if unit.player == player.player:
      food_cost += unit.food_cost
      food += unit.food
  
  attr = (food_cost-food)*100//pos.food
  if attr < 0: attr = 0
  return attr

def set_attrition(attrition, player, pos):
#   sp.speak(attr)
  if attrition > 100 and attrition < 125:
#     sp.speak('primero')
    for unit in pos.military:
      if unit.player == player.player: 
        unit.hitpoint -= randint(5, 15)
  if attrition >= 125 and attrition < 150:
#     sp.speak('segundo')
    for unit in pos.military:
      if unit.player == player.player:
        unit.hitpoint -= randint(15, 25)
  if attrition >= 150 and attrition < 175:
#     sp.speak('tercero')
    for unit in pos.military:
      if unit.player == player.player: 
        unit.hitpoint -= randint(25, 35)
  if attrition >= 175 and attrition < 200:
    #     sp.speak('tercero')
    for unit in pos.military:
      if unit.player == player.player: 
        unit.hitpoint -= randint(35, 45)
  if attrition >= 200:
    #     sp.speak('tercero')
    for unit in pos.military:
      if unit.player == player.player: 
        unit.hitpoint -= randint(45, 55)
  
  for unit in pos.military:
    if unit.hitpoint <= 0:
      removeunit(unit, pos)

def capturecity(player, city):
  city.player = player.player
  for own in city.owns:
    own.player = player.player
  city.capital = 0
  players[num].cities.append(city)
  set_city(players[num])
  # Remove city.
  for pl in players:
    pl.cities = [city for city in pl.cities if city.player == pl.player]

def captureunit(player, unit):
  unit.player = player.player
  player.units.append(unit)
  for pl in players:
    pl.units = [unit for unit in pl.units if unit.player == pl.player]
  sp.speak('{} {}.'.format(unit.name, captured_t))

def check_enemy():
  global player
  enemies = 0
  friends = 0
  for t in wmap:
    if t.sight:
      for unit in t.military:
        if unit.player not in player.friends: enemies += 1
        if unit.player in player.friends: friends += 1
  
  sp.speak('{} {}, {} {}.'.format(enemies, enemies_t, friends, friends_t),1)

def check_improvement_rq(improvement, player, position):
  blocked = 0
  playername = player.player
  in_owned = 0
  # NOTE to pas next tree vars to 0.
  in_resource = 1
  in_terrain = 0
  in_subterrain = 0
  
  if position.player ==playername and 0 in improvement.tile_owned:
    in_owned = 1
  if position.player in player.friends and 1 in improvement.tile_owned:
    in_owned = 1
  if position.player ==None and 2 in improvement.tile_owned:
    in_owned = 1
  if (position.player != playername and position.player not in player.friends
      and position.player != None and 3 in improvement.tile_owned):
    in_owned = 1
  
  if position.terrain in improvement.terrain: in_terrain = 1
  if position.subterrain in improvement.subterrain: in_subterrain = 1
  
  blocklist = [in_owned, in_resource, in_terrain, in_subterrain]
  for i in blocklist:
    if i == 0: 
      blocked = 1
  
  return blocked  


def check_improvement_rq1(item, player, position):
  blocked = 1
  playername = player.player
  if item.in_owns and position.player == playername:
    blocked = 0
  elif item.in_owns and position.player != playername:
    loadsound('errn1')
    sp.speak('no tuyo')
    return blocked
  
  if item.in_friend and position.player in player.friends:
    blocked = 0
  elif item.in_friend and position.player not in player.friends:
    loadsound('errn1')
    sp.speak('no amigo')
    return blocked
  
  if item.in_neutral and position.player == None:
    blocked = 0
  elif item.in_neutral and position.player != None:
    loadsound('errn1')
    sp.speak('no neutral')
    return blocked
  
  if item.in_hostile and (position.player != None 
    and position.player not in player.friends):
    blocked = 0
  elif item.in_hostile and (position.player == None 
    or position.player in player.friends):
    loadsound('errn1')
    sp.speak('no enemigo')
    return blocked
  
  
  if position.terrain not in item.terrain:
    sp.speak('no terrain')
    return blocked
  if position.subterrain not in item.subterrain:
    sp.speak('no en subterrain')
    return blocked
  if position.hill not in item.hill:
    sp.speak('no en hill')
    return blocked
  
  
  if position.resource and position.resource.visible == 0: res = None
  elif position.resource and position.resource.visible: res = position.resource
  elif position.resource == None: res = None
  if res not in item.resources:
    sp.speak('no en recurso')
    return blocked

def check_works():
  for t in wmap:
    for unit in t.civil+t.military:
      if unit.is_working and t.improvement.turns > 0:
        t.improvement.turns -= 1
        if t.improvement.turns < 0: 
          t.improvement.turns = 0
          add_improvement()
      if unit.is_working and t.improvement.turns <= 0: unit.is_working = 0
  
  
        
    
      
      
      

def combat(defensor, attacker, pos, auto=1):
  units = [defensor, attacker]
  units = sorted(units, key=attrgetter('is_ranged'), reverse=True)
  unit = 0
  wait1 = 500
  wait2 = 500
  end = 0
  say = 1
  if auto: say = 0
  defensor.range = attacker.corange
  defensor.range -= defensor.corange
  if defensor.range < 0: defensor.range = 0
  attacker.range = defensor.corange
  attacker.range -= attacker.corange
  if attacker.range < 0: attacker.range = 0
  if defensor.can_charge: defensor.charge = 1
  if attacker.can_charge: attacker.charge = 1
  mapparameters()
  terrain_defense = pos.totaldefense
  turn = 15
  time = ticks()
  timec = 0
  while turn:
    sleep(0.01)
    playsound(pos)
    if say and auto == 0:
      say = 0
      time, timec = ticks(), 1000
      sp.speak('{} {} {}. {} {} {}.'.format(defensor.name, hitpoint_t, 
        defensor.hitpoint, attacker.name, hitpoint_t, attacker.hitpoint),1)
    
    if ticks() > time+timec:
      focus = units[unit]
      
      f_defense = focus.defense
      f_hitpoint = focus.hitpoint
      f_precision = focus.precision
      f_protection = focus.protection
      f_strength = (f_hitpoint*100//focus.hitpoint_max)*focus.strength//100
      sp.speak('damage {} of {}.'.format(f_strength, focus.strength))
      f_strength = focus.strength
      if unit == 0: 
        target = units[1]
      if unit == 1: 
        target = units[0]
        f_strength -= terrain_defense*f_strength//100
      
      if day == 0 and focus.night_vision == 0:
        if focus.is_ranged:
          f_precision -= 2
          sp.speak('ranged night blind')
          sleep(0.3)
        if focus.is_ranged == 0:
          f_precision -= 1
          sp.speak('melee night blind')
          sleep(0.3)
      if focus.bonus_ethereal and attacker.is_ethereal:
        f_strength += focus.bonus_ethereal
        sp.speak('ethereal')
      if focus.bonus_human and attacker.is_human:
        f_strength += focus.bonus_human
        sp.speak('human')
      if focus.bonus_mechanical and attacker.is_mechanical:
        f_strength += focus.bonus_mechanical
        sp.speak('mechanical')
      if focus.bonus_mounted and target.is_mounted:
        f_strength += focus.bonus_mounted
        sp.speak('mounted')
      if focus.bonus_ranged and attacker.is_ranged:
        f_strength += focus.bonus_ranged
#         sp.speak('ranged')
      if focus.bonus_undead and attacker.is_undead:
        f_strength += focus.bonus_undead
        sp.speak('undead')
      
      if focus.hitpoint > 0:
        if focus.range <= 0:
          ch10.set_volume(1.0, 0.7)
          ch12.set_volume(0.7, 1.0)
        if focus.range > 0:
          if focus.is_mounted == 0: focus.range -= 1
          if focus.is_mounted == 1: focus.range -= 2
          unit += 1
          if unit == 2: unit = 0
          ch10.set_volume(0.5, 1.0)
          ch12.set_volume(1.0, 0.5)
          
          if unit == 0:
            if auto == 0:
              wait = loadsound(choice(focus.steps), ch10)
              sleep(wait)
          if unit == 1:
            if auto == 0:
              wait = loadsound(choice(focus.steps), ch12)
              sleep(wait)
          continue
        
        if auto == 0: 
          sp.speak('{} {}.'.format(focus.name, attack_t))
          sleep(0.3)
        if unit == 0:
          if focus.charge:
            if auto == 0:
              wait = loadsound(choice(focus.steps), ch10)/2
              sleep(wait)
          if focus.charge == 0:
            if auto == 0:
              wait = loadsound(choice(focus.sh), ch10)
              sleep(wait)
        if unit == 1:
          if focus.charge:
            if auto == 0:
              wait = loadsound(choice(focus.steps), ch12)/2
              sleep(wait)
          if focus.charge == 0:
            if auto == 0:
              wait = loadsound(choice(focus.sh), ch12)
              sleep(wait)
        if focus.charge:
          f_precision += 1
          f_strength = int(f_strength*1.5)
          if target.bonus_mounted:
            sp.speak('anula carga')
            focus.charge = 0
            f_precision -= 4
            f_strength = f_strength//2 
        if randint(0, 10) <= f_precision:
          # si acierta.
          if randint(0, 10) <= target.defense:
            #si es bloqueado.
            if auto == 0: time, timec = ticks(), 500
            if unit == 0:
              if focus.charge == 0:
                if auto == 0:
                  wait = loadsound(choice(target.block), ch12)/1.7
                  sleep(wait)
              if focus.charge:
                focus.charge = 0
                if auto == 0:
                  wait = loadsound(choice(target.block), ch12)/1.7
                  sleep(wait)
            if unit == 1:
              if focus.charge == 0:
                if auto == 0:
                  wait = loadsound(choice(target.block), ch10)
                  sleep(wait)
              if focus.charge:
                focus.charge = 0
                if auto == 0:
                  wait = loadsound(choice(target.block), ch10)
                  sleep(wait)
          elif randint(0, 10) > target.defense:
            # si no es bloqueado.
            if unit == 0:
              if focus.charge == 0:
                if auto == 0: 
                  wait = loadsound(choice(focus.hits), ch12)
                  sleep(wait)
              if focus.charge:
                focus.charge = 0
                if auto == 0:
                  wait = loadsound(choice(focus.hits_charge), ch12)
                  sleep(wait)
            if unit == 1:
              if focus.charge == 0:
                if auto == 0: 
                  wait = loadsound(choice(focus.hits), ch10)
                  sleep(wait)
              if focus.charge:
                focus.charge = 0
                if auto == 0:
                  wait = loadsound(choice(focus.hits_charge), ch10)
                  sleep(wait)
            
            damage = f_strength-target.protection
            if damage <= 0:
              damage = 0
            if randint(1, 100) <= 10:
              if focus.ai == 0: sp.speak('luck!')
              sleep(0.3) 
              damage += randint(1, f_strength)
            target.hitpoint -= damage
            say = 1
            
            if target.hitpoint <= 0:
              if unit == 0:
                if defensor.ai == 0 or attacker.ai == 0:
                  wait = loadsound(choice(target.die), ch12)
                  sleep(wait//2)
              if unit == 1:
                if defensor.ai == 0 or attacker.ai == 0:
                  wait = loadsound(choice(target.die), ch10)
                  sleep(wait//2)
      
      unit += 1
      if unit == 2: 
        unit = 0
        turn -= 1
      
      if turn == 0:
        end = 1
        sp.speak('{} {} {}. {} {} {}.'.format(defensor.name, hitpoint_t, 
          defensor.hitpoint, attacker.name, hitpoint_t, attacker.hitpoint),1)
        attacker.moves -= 1
        for unit in units:
          if unit.ai: unit.wait = 1
        
      if focus.hitpoint  <= 0 or target.hitpoint <= 0:
        end = 1
        if defensor.ai == 0 or attacker.ai == 0:
          end = 0
          sp.speak('{} {} {}. {} {} {}.'.format(defensor.name, hitpoint_t, 
            defensor.hitpoint, attacker.name, hitpoint_t, attacker.hitpoint),1)
          
      if end or turn == 0:
        while True: 
          for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN :
              sp.speak('{} {} {}. {} {} {}.'.format(defensor.name, hitpoint_t, 
                defensor.hitpoint, attacker.name, hitpoint_t, attacker.hitpoint),1)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
              sleep(loadsound('back4'))
              return defensor, attacker

def combat1(defensor, precisioner):
  turn = 10
  attrange = precisioner.corange
  debonus = checknext.totaldefense
  defrange = defensor.corange
  sp.speak(debonus)
  say = 0
  wait1 = 0.5
  if defrange  and precisioner.is_ranged:
    defrange = 0
  if defensor.is_ranged and precisioner.is_ranged:
    defrange += 1
    attrange = 0
  while turn:
    sleep(0.1)
    playsound(checknext)
    turn -= 1
    
    # Attacker precision.
    failed = 0
    if defrange == 0:
      ch10.set_volume(0.6, 1)
      loadsound(choice(precisioner.sh), ch10)
      sleep(0.1)
      if randint(0, 10) > precisioner.precision:
        failed = 1
      
      if  failed == 0 and  randint(0, 10) > defensor.defense:
        ch11.set_volume(1.0, 0.5)
        wait = loadsound(choice(precisioner.hits), ch11)
        sleep(wait)
        say = 1
        damage = precisioner.strength - defensor.protection
        damage -= debonus*damage//100
        if damage < 0: damage = 0
        sp.speak(damage)
        sleep(0.3) 
        defensor.hitpoint -= damage
      elif failed == 0 and randint(0, 10) <= defensor.defense:
        ch11.set_volume(1.0, 0.5) 
        wait = loadsound(choice(defensor.block), ch11)
        sleep(wait)

    if defrange:
      defrange -= 1
      left = 0.5
      right = 1.0
      ch12.set_volume(left, right)
      for i in range(3):
        left += 0.1
        ch12.set_volume(left, right)
        loadsound(choice(precisioner.steps), ch12)
        sleep(0.4)
    
    if defensor.hitpoint <= 0:
      ch15.set_volume(1, 0.5)
      wait = loadsound(choice(defensor.die), ch15)
      sleep(wait)
    playsound(checknext)
    
    sleep(wait1)
    
    # defensor counterprecision.
    failed = 0
    if defensor.hitpoint > 0:
      if attrange == 0:
        ch13.set_volume(1.0, 0.7)
        loadsound(choice(defensor.sh), ch13)
        sleep(0.1)
        if randint(0, 10) > defensor.precision:
          failed = 1
        
        if  failed == 0 and  randint(0, 10) > precisioner.defense:
          ch14.set_volume(0.8, 1.0)
          wait = loadsound(choice(defensor.hits), ch14)
          say = 1
          damage = defensor.strength - precisioner.protection
          if damage < 0: damage = 0 
          sp.speak("{}.".format(damage))
          sleep(wait)
          precisioner.hitpoint -= damage
        elif failed == 0 and randint(0, 10) <= precisioner.defense: 
          ch14.set_volume(0.6, 1.0)
          wait = loadsound(choice(precisioner.block), ch14)
          sleep(wait)
    
    if attrange:
        attrange -= 1
        left = 1.0
        right = 0.5
        ch15.set_volume(left, right)
        for i in range(3):
          right += 0.2
          ch15.set_volume(left, right)
          loadsound(choice(defensor.steps), ch15)
          sleep(0.4)
    
    if precisioner.hitpoint <= 0:
      ch15.set_volume(0.6, 1)
      wait = loadsound(choice(precisioner.die), ch15)
      sleep(wait)
    playsound(checknext)  
    
    if precisioner.hitpoint < 0:
      sp.speak('ataquer') 
      precisioner.hitpoint = 0
    
    if defensor.hitpoint < 0:
      sp.speak('defensor') 
      defensor.hitpoint = 0
    
    if say == 0: sleep(1)
    
    if say:
      say = 0
      speak1 = "{} {}, {} {}.".format(defensor_t, defensor.name, 
        defensor.hitpoint, hitpoint_t)
      speak2 = "{} {}, {} {}.".format(precisioner_t, precisioner.name, 
        precisioner.hitpoint, hitpoint_t)
      sp.speak("{} {}".format(speak1, speak2))
      sleep(len(speak1 + speak2)/30)
    
    playsound(checknext)
    
    if turn == 0 and defensor.hitpoint >0 and precisioner.hitpoint > 0:
      left = 1.0
      right = 1.0
      for i in range(4):
        left -= 0.1
        ch12.set_volume(left, right)
        loadsound(choice(precisioner.steps), ch12)
        sleep(0.3)
      return defensor, precisioner
    
    if defensor.hitpoint <= 0 or precisioner.hitpoint <= 0:
      return defensor, precisioner

def creatingmap():
  global wmap, width, height, east, west, maxplayers
  global builder, name, globales
  
  builder = 1
  
  # width * height.
  size1 = [30, 22]
  width = size1[0]
  height = size1[1]
  maxplayers = 4  
  
  sp.speak("se creara")
  tile = Terrain()
  wmap = [DC(tile) for i in range(width * height)]
  for i in wmap:
    i.civil = list()
    i.military = list()
    i.events = list()
    i.tags = list()
  
  east = wmap[width-1:len(wmap):width]
  west =      wmap[0:len(wmap):width]  
  
  sp.speak("mapa creado")
  starting = 0
  ending= width
  num = 1
  x = height
  while starting < len(wmap):
    y = 1
    for i in wmap[starting:ending]:
      i.x = x
      i.y = y
      y += 1
    starting += width
    num += 1
    ending *= num
    x -= 1
  
  
  globales = [wmap, height, width, east, west, maxplayers]
#   location = os.path
  mapname= setplacename()
  ext = ".cvm"
  name = os.path.join("maps//")+mapname+ext 
  
#   sp.speak("se guardara")
#   file = open(os.path.join("maps//")+name+ext, "wb")
#   file.write(dumps(globales))
#   file.close()
#   sp.speak("mapa guardado")

def definitions():
  global tech_tree, buildings_list, unitlist, resource_list, nations
  
  for t in wmap:
    if t.resource:
      for res in resource_list:
        if res.name == t.resource.name:
          t.resource = res
  
  for buildings in buildings_list:
#     buildings.buildings = [eval(item) for item in buildings.buildings]
#     buildings.building_rq = [eval(item) for item in buildings.building_rq]
    buildings.obsolete = [eval(item) for item in buildings.obsolete_building]
    buildings.units = [eval(item) for item in buildings.units]
#     buildings.tech_rq = [eval(item) for item in buildings.tech_rq]
  
  for nt in nations:
    nt.actions = [eval(item) for item in nt.actions] 
#   for unit in unitslist:
#     unit.building = [eval(item) for item in unit.building]
#     unit.resources = [eval(item) for item in unit.resources]
#     unit.tech_rq = [eval(item) for item in unit.tech_rq]
#     unit.upgrade = [eval(item) for item in unit.upgrade if item != None]
  
  for tech in tech_tree:
    tech.buildings = [eval(item) for item in tech.buildings]
    tech.improvements = [eval(item) for item in tech.improvements]
    tech.leads = [eval(item) for item in tech.leads]
    tech.reveal = [eval(item) for item in tech.reveal]
    tech.units = [eval(item) for item in tech.units]
    tech.tech_rq = [eval(item) for item in tech.tech_rq]

def defineheal(pos):
  heal = pos.heal+pos.s_heal+pos.h_heal+pos.r_heal+pos.u_heal+pos.c_heal
  return heal

def definestack(pos):
  player = players[num]
  stack = pos.totalstack
  return stack

def descriveimprovement(improvement):
  if improvement.turns > 0 and improvement.in_progress:
    sp.speak('{} {} {} {}.'.format(improvement.name, in_t, improvement.turns, 
      turns_t))
  if improvement.turns > 0 and improvement.in_progress == 0:
    sp.speak('{} {}.'.format(improvement.name, incomplete_t))
  if improvement.turns == 0:
    sp.speak('{}.'.format(improvement.name))

def describeunit(unit, sound=1):
  ch1.set_volume(0.5)
  if sound: loadsound(choice(unit.selected), ch1)
  sp.speak('{} {}.'.format(unit.player, unit.name),1)
  if unit.is_commander:
    sp.speak('{} {}.'.format(compoints_t, unit.compoints))
  sp.speak('{} {} {}.'.format(unit.moves, of_t, unit.moves_max))
  if unit.is_ranged == 0 and unit.can_combat: sp.speak(melee_t)
  if unit.is_ranged == 0 and unit.can_combat == 0: sp.speak(civil_t)
  if unit.is_ranged == 1: sp.speak(ranged_t)
  if unit.is_working: sp.speak("{}.".format(isworking_t))
  if unit.can_heal:
    sp.speak(medic_t) 
    sp.speak('{} {}.'.format(heal_rate_t, unit.heal_rate))
  if unit.can_transport: 
    sp.speak(transport_t)
    if len(unit.units): sp.speak("{} {}.".format(len(unit.units), units_t))

def explore_map(event):
  global info, wmap, position, x1, x2
  info = 1
  x1= 0
  x2= 0
  sp.speak(",",1)
  if event.key == pygame.K_LEFT: 
    if position not in west:
      if cityview:
        npos = wmap[wmap.index(position)-1] 
        enable = explore_map_check(city, npos)
        if enable == 0:
          loadsound("errn1")
          return
      position = wmap[wmap.index(position)-1]
       
    else:
      loadsound("errn1")
      pygame.time.wait(200)
      pygame.event.clear()
  if event.key == pygame.K_RIGHT:
    if position not in east:
      if cityview:
        npos = wmap[wmap.index(position)+1] 
        enable = explore_map_check(city, npos)
        if enable == 0:
          loadsound("errn1")
          return
      position = wmap[wmap.index(position)+1]
    else:
      loadsound("errn1")
      pygame.time.delay(300)
      pygame.event.clear()
  if event.key == pygame.K_UP: 
    if position not in wmap[:width]:
      if cityview:
        npos = wmap[wmap.index(position)-width] 
        enable = explore_map_check(city, npos)
        if enable == 0:
          loadsound("errn1")
          return
      position = wmap[wmap.index(position)-width]
    else:
      loadsound("errn1")
      pygame.time.delay(300)
      pygame.event.clear()
  if event.key == pygame.K_DOWN:
    if position not in wmap[len(wmap)-width:]:
      if cityview:
        npos = wmap[wmap.index(position)+width] 
        enable = explore_map_check(city, npos)
        if enable == 0:
          loadsound("errn1")
          return
      position = wmap[wmap.index(position)+width]
    else:
      loadsound("errn1")
      pygame.time.delay(300)
      pygame.event.clear()
  
  #sounds.
  if position.player == player.player:
    ch3.set_volume(0.5)
    loadsound("back5", ch3)
  elif position.player == None:
    ch3.set_volume(0.5) 
    loadsound("arch_hits6", ch3)
  elif position.player not in [None, player.player]:
    ch3.set_volume(0.5)
    loadsound("melee_metal_sh1", channel=ch3)


def explore_map_check(city, position):
  enabled = 0
  square = setplace(position, value=1, action="return")
  for i in square:
    if i in city.owns: enabled = 1
  
#   Pdb().set_trace()
  return enabled 

def get_action(player, position, unit):
  global info
  say = 1
  x = 0
  if unit.is_settler:
    ask = asking(warning1_t)
    if ask:
      get_city(player, position, unit)
      return
    elif ask == 0:
      loadsound('back2')
      return
  while True:
    if say:
      say = 0
      sp.speak('{}'.format(unit.actions[x].name), 1)
    
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        playsound('back1')
        unit.actions[x]()
        return unit.actions[x]
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        playsound('back1')
        return None

def get_city(player, position, unit):
  global info
  addcity(player, position)
  set_city(player)
  set_science(player)
  if player.ai == 0: 
    info = 1
    loadsound('back1')
  unit.hitpoint = 0

def get_items(player, toget, unit):
  technames = []
  for tech in player.researched: technames.append(tech.name)
  if toget == "improvement":
    items = list()
    for imp in unit.improvements:
      blocked = 0
      for tech in imp.tech_rq:
        if tech.name not in technames: 
          blocked = 1
      if blocked == 0:
        items.append(DC(imp))
        
    return items

def get_move(tomove):
  global position, player
  destiny = tomove.moveto[0]
  square = setplace(position, value=1, action="return")
  shuffle(square)
  if tomove.can_sail == 0:
    square = [sq for sq in square if sq.terrain not in [6, 7, 8]]
  if tomove.can_fly == 0:
    square = [sq for sq in square if sq.terrain != 5]
  
  if destiny.x < position.x:
    square = [sq for sq in square if sq.x <= position.x]
  if destiny.x > position.x:
    square = [sq for sq in square if sq.x >= position.x]
  if destiny.y < position.y:
    square = [sq for sq in square if sq.y <= position.x]
  if destiny.y > position.y:
    square = [sq for sq in square if sq.x >= position.x]
  
  square = sorted(square, key=attrgetter("subterrain", "hill"))
  Pdb().set_trace()
  checknext = square[0]
  return checknext

def get_units(position):
  global tileunits
  tileunits = list()
  for unit in position.military+position.civil:
    if unit.seen:
      tileunits.append(unit)

def healunit(unit):
  global players
  mapupdate()
  player = players[num] 
  pos = wmap[unit.location]
  heal = pos.heal
  if unit.can_heal and unit.hitpoint < unit.hitpoint_max:
    if pos.player in unit.friends:
      heal_rate = unit.heal_infriend+heal
      unit.hitpoint += heal_rate*unit.hitpoint_max//100
    if pos.player == None:
      heal_rate = unit.heal_inneutral+heal
      unit.hitpoint += heal_rate*unit.hitpoint_max//100
    if pos.player not in unit.friends and pos.player != None:
      heal_rate = unit.heal_inhostile+heal
      unit.hitpoint += heal_rate*unit.hitpoint_max//100
      
    if unit.hitpoint > unit.hitpoint_max: 
      unit.hitpoint = unit.hitpoint_max

def info_city(event, position):
  if event.key == pygame.K_c:
    sp.speak('{} {}.'.format(city.culture, culture_t),1)
  if event.key == pygame.K_d:
    sp.speak('{} {}.'.format(wmap[city.location].c_defense, defense_t),1)
  if event.key == pygame.K_e:
    sp.speak('{} {}.'.format(city.gold, gold_t),1)
  if event.key == pygame.K_q:
    sp.speak('{} {}.'.format(city.food, food_t),1)
  if event.key == pygame.K_s:
    sp.speak("{} {}, {} {}, {} {}, {} {}.".format(position.totalfood, food_t, position.totalproduction, production_t, position.totalgold, gold_t, position.culture, culture_t))
  if event.key == pygame.K_w:
    sp.speak('{} {}.'.format(city.production, production_t),1)

def info_tile(event, position):
  if event.key == pygame.K_a:
    attr = get_attrition(position, player)
    sp.speak('{} {}%.'.format(attrition_t, attr),1)
  if event.key == pygame.K_c:
    sp.speak('{} {}.'.format(culture_t, position.culture),1)
  if event.key == pygame.K_d:
    sp.speak('{} {}%.'.format(defense_t, position.totaldefense),1)
  if event.key == pygame.K_e:
    sp.speak('{} {}.'.format(gold_t, position.totalgold),1)
  if event.key == pygame.K_q:
    sp.speak('{} {}.'.format(food_t, position.totalfood),1)
  if event.key == pygame.K_r:
    if position.resource:
      res = position.resource
      tospeak = '{} {}, {} {}, {} {}.'.format(food_t, res.food, production_t,
        res.production, gold_t, res.gold)
      sp.speak('{}. {}'.format(res.name, tospeak), 1)
  if event.key == pygame.K_s:
    info = 1
  if event.key == pygame.K_w:
    sp.speak('{} {}.'.format(production_t, position.totalproduction),1)

def info_unit(event, position):
  if event.key == pygame.K_a:
    sp.speak('{} {}, {} {}.'.format(strength_t, tomove.strength, precision_t, tomove.precision),1)
  if event.key == pygame.K_d:
    sp.speak('{} {}, {} {}.'.format(protection_t, tomove.protection, defense_t, tomove.defense), 1)
  if event.key == pygame.K_e:
    sp.speak('{} {}.'.format(maintenance_t, tomove.maintenance), 1)
    sp.speak('{} {}.'.format(food_t, tomove.food_cost))
  if event.key == pygame.K_q:
    sp.speak('{} {} {} {}.'.format(hitpoint_t, tomove.hitpoint, of_t, tomove.hitpoint_max),1)
  if event.key == pygame.K_r:
    for notes in tomove.notes:
      if notes == tomove.notes[-1]:
        sp.speak('{}.'.format(notes))
      else:
        sp.speak('{},'.format(notes))
  if event.key == pygame.K_s:
    describeunit(tomove)
  if event.key == pygame.K_w:
    sp.speak('{} {} {} {}.'.format(moves_t, tomove.moves, of_t, tomove.moves_max),1)


def item_selection(city, item, player, position, toget, unit):
  global wmap
  def temporal():    
    if toget == 'queue':
      item = list()
      for it in city.queue: item.append(it)
      return item
    
    if toget == 'show':
      item = list()
      for it in city.buildings: item.append(it)
      return item
    
    if toget == "buildings":
      sp.speak(buildings_t)
      item = list()
      for building in player.av_buildings:
        blocked = 0
        for tech in building.tech_rq:
          if tech not in player.researched: blocked = 1
        if blocked == 0 and building not in city.buildings: 
            item.append(building)
#       for tech in player.researched:
#         for building in tech.buildings:
#           if building not in city.buildings and building in player.av_buildings:
#             item.append(building)

      return item
  
    
    if toget == "technologies":
      sp.speak(research_t, 1)
      set_city(player)
      setscience(player)
      sp.speak('{} {}.'.format(science_t, player.science))
      if player.researching:
        time = ceil(player.researching[0].science_cost/player.science)
        sp.speak('{} {} {} {} {}.'.format(researching_t, player.researching[0].name, in_t, time, turns_t))
      item = list()
      for tech in player.av_tech:
#         Pdb().set_trace()
        blocked = 0
        for tech_rq in tech.tech_rq:
          if tech_rq not in player.researched: blocked = 1
        if blocked == 0: item.append(tech)
      return item
     
    
    if toget == "units":
      sp.speak(units_t, 1)
      item = list()
      for unit in player.av_units:
        blocked = 0
        for tech in unit.tech_rq:
          if tech not in player.researched: blocked = 1
        for building in unit.building:
          if building not in city.buildings: blocked = 1
        if blocked == 0: item.append(unit)
        
#       for tech in player.researched:
#         for unit in tech.units:
#           if unit in player.av_units:
#             item.append(unit)        
      
      for building in city.buildings:
        for unit in building.units:
          if unit in player.av_units:
            item.append(unit)
      
      return item
  
  sort = 1
  x = 0 
  say = 1
  while True:
    sleep(0.05)
    playsound(position)
    if toget == "buildings":
      item = sorted(item, key=attrgetter("production_cost"))
      item = [i for i in item if i not in city.queue]
      item = [i for i in item if i not in city.buildings]
    elif toget == 'units':
      item = sorted(item, key=attrgetter("production_cost"))
    elif toget == 'technologies' and sort == 1:
      item = [i for i in item if i not in player.researching]
      item = [i for i in item if i not in player.researched]
      item = sorted(item, key=attrgetter("science_cost"))
    
    if say and item:
      say = 0
      if toget == 'improvements':
        sp.speak('{} {} {} {}.'.format(item[x].name, in_t, item[x].turns, 
          turns_t))
      if toget == 'show':
        sp.speak('{}.'.format(item[x].name),1)
      if toget == 'units' or toget == 'buildings' or toget == 'queue':
        cost = item[x].production_cost
        sp.speak("{}. {} {}. {} {}.".format(item[x].name, production_t, cost,
          ceil(cost/city.production), turns_t))
      if toget == 'technologies':
        cost = item[x].science_cost
        sp.speak("{}.{} {}.".format(item[x].name, science_t, cost))
        if player.science> 0:
          sp.speak('{} {}.'.format(ceil(cost/player.science), turns_t))
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
        sp.speak(enabled_t)
        Pdb().set_trace()
        sp.speak(disabled_t)
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        x = selector(item, x, go="up", sound="improvement_selection")
        say = 1
      if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        x = selector(item, x, go="down", sound="improvement_selection")
        say = 1
      if toget == 'technologies':
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
          item = sortitem()
          sort = 1
          x = 0
          say = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
          sp.speak('{}.'.format(researched_t),1)
          item = player.researched
          sort = 0
          x = 0
          say = 1
      
      if (item and toget in   
        ['buildings', 'improvements', 'queue', 'show', 'technologies']):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
          sp.speak('{} {}.'.format(food_t, item[x].food), 1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
          sp.speak('{} {}.'.format(production_t, item[x].production), 1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
          sp.speak('{} {}.'.format(gold_t, item[x].gold), 1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
          if toget == 'improvements': continue
          sp.speak('{} {}.'.format(happiness_t, item[x].happiness), 1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
          if toget == 'improvements': continue
          sp.speak('{} {}.'.format(science_t, item[x].science), 1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
          if toget == 'improvements': continue
          sp.speak('{} {}.'.format(defense_t, item[x].defense), 1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
          if toget == 'improvements': continue
          sp.speak('{} {}.'.format(culture_t, item[x].culture), 1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
          if toget == 'improvements': continue
          sp.speak('{} {}.'.format(heal_rate_t, item[x].heal), 1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
          if toget == 'improvements': continue
          sp.speak('{} {}.'.format(stack_t, item[x].stack), 1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
          if toget == 'improvements': continue
          sp.speak(buildings_t, 1)
          if item:
            for building in item[x].buildings:
              if building in player.av_buildings: 
                sp.speak(building.name)
                
      
      if (item and toget in  
        ['buildings', 'improvements', 'queue', 'show', 'units']):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
          sp.speak('{} {}.'.format(maintenance_t, item[x].maintenance), 1)
      
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
        if toget == 'technologies' and item:
          sp.speak(resources_t, 1)
          for res in item[x].reveal:
            sp.speak(res.name)
      
        if toget == "units" and item:
          if item[x].is_ranged == 0: sp.speak("{} {}.".format(attacktype_t, melee_t))
          if item[x].is_ranged: 
            sp.speak("{} {}.".format(attacktype_t, ranged_t))
            if item[x].marange: sp.speak("{} {}.".format(marange_t, 
              item[x].marange))
            sp.speak("{} {}.".format(corange_t, item[x].corange)) 
          sp.speak("{} {}, {} {}.".format(precision_t, item[x].precision, 
            strength_t, item[x].strength))
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
        if toget == "technologies" and item:
          sp.speak(tech_rq_t)
          for tech_rq in item[x].tech_rq:
            if tech_rq in player.av_tech: 
              sp.speak(tech_rq.name)
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_f: 
        if toget == "units" and item:
          sp.speak("{} {} {} {}, {} {}, {} {}.".format(hitpoint_t, 
            item[x].hitpoint, of_t, item[x].hitpoint_max, defense_t, 
            item[x].defense, protection_t, item[x].protection))
      
#         if toget == "technologies" and item:
#           sp.speak(buildings_t, 1)
#           for building in item[x].buildings:
#             if building in player.av_buildings: 
#               sp.speak(building.name)
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
        for it in item[x].notes:
          if it == item[x].notes[-1]:
            sp.speak('{}.'.format(it))
          else:
                  sp.speak('{},'.format(it))
        
      if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
        if toget in ['buildings', 'show', 'queue']:
          sp.speak(tech_rq_t, 1)
          if item:
            for tech_rq in item[x].tech_rq:
              if  tech_rq in player.av_tech:
                sp.speak(tech_rq.name)
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
        if toget == "technologies" and item:
          sp.speak(leads_t, 1)
          for leads in item[x].leads:
            if leads in player.av_tech: 
              sp.speak(leads.name)
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
        if toget in ['buildings', 'show', 'queue', 'technologies']:
          sp.speak(units_t, 1)
          if item:
            for unit in item[x].units:
              if unit in player.av_units: 
                sp.speak(unit.name)
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
        if toget == 'technologies' and item:
          sp.speak(improvement_t, 1)
          for imp in item[x].improvements:
            if imp in player.av_improvements:
              sp.speak(imp.name)
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
        if toget == 'queue' and item:
          item.remove(item[x])
          loadsound("melee_flesh_sh1")
          sleep(0.5)
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        if toget not in ['show', 'queue']:
          if item and toget == "technologies" and item[x] not in player.researching:
            player.researching.append(DC(item[x]))
            sp.speak("{} {}.".format(item[x].name, added_t), 1)
            loadsound("back5")
          if item and toget == 'improvements':
            blocked = check_improvement_rq(item[x], player, position)
            if blocked:
              loadsound("errn1")
              continue
            
            start_improvement(item[x], position, unit)
            return
          if item and toget == 'units':
            blocked = 0
            for res in item[x].resources:
              if res not in player.resources:
                sp.speak('{} {}.'.format(needs_t, res.name),1)
                blocked = 1
            if blocked:
              continue
            loadsound(choice(item[x].sh))
            city.queue.append(DC(item[x]))
            sp.speak("{} {}.".format(item[x].name, added_t), 1)
          if item and toget == 'buildings':
            blocked, needs = item[x].requirements(player, city)
            if blocked:
              sp.speak('{}: '.format(needs_t),1)
              for it in needs:
                sp.speak(it.name) 
              continue
            loadsound('buildconstruct1')
            city.queue.append(DC(item[x]))
            sp.speak("{} {}.".format(item[x].name, added_t), 1)
            loadsound("back5")
          sleep(0.5)
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        loadsound("back1")
        return

def loadingmap(location, filext, saved=0):
  global globales, wmap, height, width, east, west, name
  global maxplayers, playnum, players, position
  x1 = 0
  say = 1
  loop = 1
  maps = glob(os.path.join(location+filext))
  while loop:
    sleep(0.01)
    if say:
      say = 0
      if maps:
        sp.speak(maps[x1][int(maps[0].rfind('\\'))+1:-4], 1)
      else:
        sp.speak(notmap_t, 1)
        
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        x1 = selector(maps, x1, go="up")
        say = 1
      if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        x1 = selector(maps, x1, go="down")
        say = 1
      if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        if maps and saved:
          sp.speak(loading_t, 1)
          file = open(maps[x1], "rw")
          globales = loads(file.read())
          
          wmap = globales[0]
          heght = globales[2]
          width = globales[1]
          east = globales[3]
          west = globales[4]
          maxplayers = globales[5]
          playnum = globales[6]
          players = globales[7]
          position = globales[8]
          
          return
        elif maps and saved == 0:
          
          file = open(maps[x1], "rb")
          name = maps[x1]
          globales = loads(file.read())
          
          wmap = globales[0]
          height = globales[1]
          width = globales[2]
          east = globales[3]
          west = globales[4]
          maxplayers = globales[5]
          
          return  
        else:
          sp.speak(notmap_t, 1)
          loadsound("errn1")
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        back1.play()
        return

def loadsound(soundfile, channel=0, path=sounds,  extention=wav):
  if channel == 0:
    mixer.Sound(path+soundfile+extention).play()
    return mixer.Sound(path+soundfile+extention).get_length()
  if channel:
    mixer.Sound(path+soundfile+extention)
    vol = channel.get_volume()
    type(vol)
    print(vol)
    print(type(vol))
    channel.play(mixer.Sound(path+soundfile+extention))
    return mixer.Sound(path+soundfile+extention).get_length()

def mapupdate():
  global wmap, player
  player = players[num]
  sight1(player)
  sight2(player)
  for tile in wmap:
    tile.totalfood = tile.food+tile.c_food+tile.s_food+tile.h_food+tile.r_food
    tile.totalproduction = (tile.production+tile.c_production+tile.s_production+
      tile.h_production+tile.r_production)
    tile.totalgold = tile.gold+tile.c_gold+tile.s_gold+tile.h_gold+tile.r_gold
    tile.totaldefense = (tile.defense+tile.c_defense+tile.s_defense+
      tile.h_defense+tile.r_defense)
    if tile.civil+tile.military:
      tile.u_stack = max(tile.civil+tile.military, 
        key=attrgetter('commandpoints')).b_commandpoints
      tile.u_heal = max(tile.civil+tile.military, key=attrgetter('can_heal')).can_heal
    
    tile.totalstack = (tile.stack+tile.c_stack+tile.s_stack+tile.h_stack+
      tile.r_stack+tile.u_stack)
    tile.totalheal = (tile.heal+tile.c_heal+tile.s_heal+tile.h_heal+
      tile.r_heal+tile.u_heal)
    
    if tile.resource and tile.resource.enabled:
      tile.totalfood += tile.resource.food
      tile.totalproduction += tile.resource.production
      tile.totalgold += tile.resource.gold
    
    if tile.improvement and tile.improvement.turns == 0:
      tile.totalfood += tile.improvement.food
      tile.totalproduction += tile.improvement.production
      tile.totalgold += tile.improvement.gold
  

def moving():
  global wmap, position, checknext, player, players, tomove, civil, ship
  city = checknext.city
  moves = tomove.moves
  terrain = checknext.terrain
  stack = definestack(checknext)
  
  sp.speak("", 1)
  if tomove.can_walk: 
    if terrain not in land:
      ships = checknext.military+checknext.civil
      ships = sorted(ships, key=attrgetter('units'))
      blocked = 1
      for unit in ships:
        blocked = 2
        if unit.can_transport and len(unit.units) < unit.stack:
          unit.units.append(tomove)
          unit.number = len(unit.units)
          tomove.location = unit.location
          tomove.moves -= 1
          tipo.remove(tomove)
          sp.speak("{} {} {}.".format(moved_t, to_t, unit.name), 1)
          if tomove.ai == 0: loadsound(choice(tomove.steps))
          return
      if blocked == 2:
        sp.speak(warning6_t, 1)
        return
      if blocked == 1:
        sp.speak(warning7_t, 1)
        if tomove.ai == 0: loadsound("errn2")
        sleep(1)
        return
  
  if tomove.can_sail:
    whitelist = [6, 7, 8]
    level2 = [8]
    if tomove.is_mechanical and terrain not in whitelist:
      if city == None:
        sp.speak(warning4_t, 1)
        if tomove.ai == 0:loadsound("errn2")
        return
      if city.player not in tomove.friends:
        sp.speak(warning5_t, 1)
        if tomove.ai == 0: loadsound("errn2")
        return
    if tomove.sail_level == 0 and terrain == 7:
      sp.speak(warning3_t, 1)
      if tomove.ai == 0: loadsound("errn2")
      return
    if tomove.sail_level <= 1 and terrain == 8:
      sp.speak(warning3_t, 1)
      if tomove.ai == 0: loadsound("errn2")
      return
  
  if tomove.can_fly == 0 and checknext.terrain == 5:
    sp.speak('no vuela')
    if tomove.ai == 0: loadsound("errn2")
    return
  if tomove.is_working:
    ask = asking(warning2_t)
    if ask == 0:
      if tomove.ai == 0: loadsound("errn2")
      return
    if ask:
      tomove.is_working = 0 
      position.improvement.in_progress = 0
  
  if tomove.can_sail:
    sp.speak('es ship')
    water = [6,7,8]
    for unit in checknext.military:
      if unit.player not in tomove.friends:
        if unit.can_combat:
          unit, tomove = combat(unit, tomove, checknext)
          
          if unit.hitpoint < 1:
            removeunit(unit, checknext)
          
          if tomove.hitpoint < 1:
            removeunit(tomove, position)
            if tomove.ai == 0: loadsound("defeat1")
          break
        
        if unit.can_combat == 0:
          removeunit(unit, checknext) 
    
    for unit in checknext.military:
      if unit.player not in tomove.friends:
        sp.speak('amigos')
        return
    
    if terrain not in water:
      if tomove.ai == 0: 
        wait = loadsound(choice(tomove.steps))
        sleep(wait//2)
      tomove.location = wmap.index(checknext)
      checknext.civil.append(tomove)
      tipo.remove(tomove)
      players[num].position = wmap[wmap.index(checknext)]
      tomove.moves -= 1
      for i in tomove.units: i.location = wmap.index(checknext)
      return
    if terrain in water:
      if tomove.can_combat:
        if tomove.ai == 0: 
          wait = loadsound(choice(tomove.steps))
          sleep(wait//2)
        tomove.location = wmap.index(checknext)
        checknext.military.append(tomove)
        if position.terrain not in water: position.civil.remove(tomove)
        if position.terrain in water: position.military.remove(tomove)
        players[num].position = wmap[wmap.index(checknext)]
        tomove.moves -= 1
        for i in tomove.units: i.location = wmap.index(checknext)
        return
      if tomove.can_combat == 0:
        if tomove.ai == 0: 
          wait = loadsound(choice(tomove.steps))
          sleep(wait//2)
        tomove.location = wmap.index(checknext)
        checknext.civil.append(tomove)
        position.civil.remove(tomove)
        players[num].position = wmap[wmap.index(checknext)]
        tomove.moves -= 1
        for i in tomove.units: i.location = wmap.index(checknext)
        return
  
  if tomove.is_human:
#     sp.speak('es humano')
    if checknext.hill:
      moves -= 2
    elif checknext.hill == 0 and checknext.subterrain == -1:
      moves -= 1
    elif checknext.hill == 0 and checknext.subterrain > -1:
      if checknext.subterrain == 0 and tomove.is_ranger:
        moves -= 1
      elif checknext.subterrain == 0 and tomove.is_ranger == 0:
        moves -= 2
      
      if checknext.subterrain == 1 and tomove.is_jungle:
        moves -= 1
      elif checknext.subterrain == 1 and tomove.is_jungle== 0:
        moves -= 2
      
      if checknext.subterrain == 2 and tomove.is_marsh:
        moves -= 1
      elif checknext.subterrain == 2 and tomove.is_marsh == 0:
        moves -= 2
    
    if moves < 0:
      if tomove.ai == 0: loadsound("errn2")
      if tomove.ai: tomove.wait = 1
      return
    
    
    # If military.
    for u in checknext.military:
      if u.player not in tomove.friends and u.can_combat:
        if tomove.can_combat == 0:
          if tomove.ai == 0: loadsound("errn2")
          return
        elif tomove.can_combat:
          u, tomove = combat(u, tomove, checknext)
          
          if u.hitpoint < 1:
            removeunit(u, checknext)
          
          if tomove.hitpoint < 1:
            removeunit(tomove, position)
            if tomove.ai == 0: loadsound("defeat1")
            return
          break
        
      
    #after combat.
    for u in checknext.military:
      if u.player not in tomove.friends:
        if tomove.ai == 0:sp.speak('retorna')
        if tomove.ai: tomove.wait = 1
        return
    
    # If civil.
    for unit in checknext.civil: 
      if tomove and unit.player not in tomove.friends:
        if tomove.can_captureunit:
          captureunit(player, unit)
        elif tomove.can_captureunit == 0 and tomove.can_combat:
          removeunit(unit, checknext)
          sp.speak("civilians killed")
  
    if tomove.ai == 0: 
      wait = loadsound(choice(tomove.steps))
      sleep(wait/1.5)
    
    if city and city.player not in  tomove.friends and tomove.can_capturecity:
      sp.speak('captura')
      capturecity(player, city)
      sp.speak('{} {}.'.format(city.name, captured_t),1)
    
    tomove.location = wmap.index(checknext)
#     if checknext.player and checknext.player not in player.friends:
#       if checknext.is_working: 
#         sp.speak('casilla blockeada')
#         sleep(0.5)
#         blocktile(checknext.player, checknext.name, checknext)
    if tomove in position.civil: position.civil.remove(tomove)
    elif tomove in position.military: position.military.remove(tomove)
    if tomove.can_combat== 0: 
      checknext.civil.append(tomove)
    if tomove.can_combat: 
      checknext.military.append(tomove)
    position = wmap[wmap.index(checknext)]
    player.lastposition = wmap[wmap.index(checknext)]
    tomove.moves = moves
    if tomove.can_combat: civil = 0
    if tomove.can_combat == 0: civil = 1
    if ship: ship.number = len(ship.military)
    tomove.explored.append(checknext)

def nextturn():
  global civil, cityoptions, info, newturn, num, player, players, tomove
  global turn, x1, x2, x3
  sp.speak(' ',1)
  for i in channels: i.fadeout(400)
  cityoptions = 0
  civil = 0
  info = 1
  x1 = -1
  x2 = -1
  player.auto = 1
  tomove = list()
  
  if player.ai == 0: loadsound("endturn1")
  newturn = 1
  num += 1
  
  if num == len(players):
    num = 0
    
    turn += 1
    player = players[num]
    for pl in players:
      for unit in pl.units:
        if len(unit.explored) >= 3:  unit.explored = list()
        if unit.wait == 1: unit.wait = 0
    [startturn(pl) for pl in players]
#     for tile in wmap:
#       if tile.military:
#         attrition = get_attrition(tile, player)
#         set_attrition(attrition, player, tile)

def playsound(pos):
  global windtime1, windtime2, wind_count1, wind_count2
  global citytime1, citytime2, city_count1, city_count2
  global generictime, genericcount
  global resbase, rescount  
  global unitbase, unitcount
  
  ch_winds = [ch45, ch46]
  dogs1 = ["dog1", "dog2", "dog3", 'dog4', 'dog5', 'dog6', 'dog7', 'dog8', 
    'dog9', 'dog10', 'dog11', 'dog12', 'dog13', 'dog14', 'dog15', 'dog16', 
    'dog17', 'dog18']
  birds1 = ['birds_beach1', 'birds_beach2', 'birds_beach3', 'birds_beach4', 'birds_beach5']
  citybackground1 = ['city_amb1', 'city_amb2']
  cityspech1 = ['city_spech1']
  coast_ambients = ["Coast_fx1", "Coast_fx2"]
  deserts = ["Desert1", "Desert2"]
  grasslands = ["grass1", 'grass2', 'grass3']
  forests = ["Forest1", "Forest2", "Forest3", 'forest4', 'forest5']
  forestwinds = ["Amb_fwind1", "Amb_fwind2", "Amb_fwind3", "Amb_fwind4", "Amb_fwind5", 
    "Amb_fwind6", "Amb_fwind7"]
  jungles = "Jungle1", "Jungle2", "Jungle3", "Jungle4", "Jungle5" 
  ices = ["Ice1", "Ice2"]
  icewinds = ["Amb_iwind1", "Amb_iwind2", "Amb_iwind3"]
  marshes1 = ["Marsh1", "Marsh2"]
  marshes2 = ["Marsh3", "Marsh4"]
  mountains = ["Mountain1", "Mountain2"]
  plains = ["plains1", 'plains2']
  plainsambient = ["Amb_pwind1", "Amb_pwind2", "Amb_pwind3", "Amb_pwind4"]
  oceans = ["Ocean1", "Ocean2"]
  tundras = ["Tundra1", "Tundra2"]
  tundrawinds = ["Amb_twind1", "Amb_twind2", "Amb_twind3", "Amb_twind4", "Amb_twind5", 
    "Amb_twind6"]
  water = [6, 7]
  
  # Resources.
  if pos.resource and pos.resource.visible and ch41.get_busy() == False:
    if ticks() > resbase+rescount and pos.resource.soundeffects and pos.sight:
      ch41.set_volume(uniform(0.01, 0.3), uniform(0.01, 0.3))
      loadsound(choice(pos.resource.soundeffects), ch41)
      resbase = ticks()
      rescount = randint(10000, 15000)
    
  # Units.
  if pos.military+pos.civil and ch40.get_busy() == False:
    if ticks() > unitbase+unitcount and pos.sight:
      unit = choice(pos.civil+pos.military)
      if unit.is_working: 
        ch40.set_volume(0.5)
        loadsound(choice(unit.working), ch40)
        unitbase = ticks()
        unitcount = randint(3000, 10000)
  
  #Generic.
  if (pos.terrain in [0, 1, 2, 3, 4, 8] and pos.sight 
      and ch39.get_busy() == False and ticks() > generictime+genericcount):
    generic = list()
    square = setplace(pos, value=1, action='return')
    for sq in square:
      if sq.terrain == 6:
        generic += birds1
    ch39.set_volume(uniform(0.01, 0.04), uniform(0.01, 0.04))
    if generic: 
      loadsound(choice(generic), ch39)
      generictime = ticks()
      genericcount = randint(10000, 30000)
  
  # City.
  if pos.city and pos.sight:
    if ch50.get_busy() == False:
      ch50.set_volume(0.6)
      loadsound(choice(citybackground1), ch50)
    if ticks() >= citytime1+city_count1 and ch51.get_busy() == False:
      cityambient = dogs1+cityspech1
      ch51.set_volume(uniform(0.01, 0.06), uniform(0.01, 0.06))
      loadsound(choice(cityambient), ch51)
      citytime1 = ticks()
      city_count1 = randint(10000, 20000)
#     if ticks() >= citytime2+city_count2 and ch52.get_busy() == False:
#       ch52.set_volume(uniform(0.01, 0.2), uniform(0.01, 0.2))
#       loadsound(choice(cityambient), ch52)
#       citytime2 = ticks()
#       city_count2 = randint(15000, 30000)
  if pos.city == None:
    ch50.fadeout(200)
    ch51.fadeout(200)
    
    # Fog.
    if pos.sight == 0 and ch19.get_busy() == False:
      ch19.set_volume(0.2)
      loadsound('fog1', ch19)
      for ch in channels1+channels2: ch.fadeout(200)
    if pos.sight and ch19.get_busy():
      ch19.fadeout(200)
    
  # Forest.
  if pos.subterrain == 0 and pos.sight:
    if ticks() >= windtime1+wind_count1 and ch45.get_busy() == False:
      ch45.set_volume(uniform(0.1, 1.0), uniform(0.1, 1.0))
      loadsound(choice(forestwinds), ch45)
      windtime1 = ticks()
      wind_count1 = randint(5000, 15000)
    if ticks() >= windtime2+wind_count2 and ch46.get_busy() == False:
      ch46.set_volume(uniform(0.1, 1.0), uniform(0.1, 1.0))
      loadsound(choice(forestwinds), ch46)
      windtime2 = ticks()
      wind_count2 = randint(5000, 15000)
    if ch30.get_busy() == False:
      loadsound(choice(forests), ch30)
  if pos.subterrain != 0 and ch30.get_busy():
    ch30.fadeout(200)
    ch45.fadeout(200)
    ch46.fadeout(200)

  #Jungle.
  if pos.subterrain == 1 and pos.sight:
    if ticks() >= windtime1+wind_count1 and ch45.get_busy() == False:
      ch45.set_volume(uniform(0.1, 1.0), uniform(0.1, 1.0))
      loadsound(choice(forestwinds), ch45)
      windtime1 = ticks()
      wind_count1 = randint(5000, 15000)
    if ticks() >= windtime2+wind_count2 and ch46.get_busy() == False:
      ch46.set_volume(uniform(0.1, 1.0), uniform(0.1, 1.0))
      loadsound(choice(forestwinds), ch46)
      windtime2 = ticks()
      wind_count2 = randint(5000, 15000)
    if ch31.get_busy() == False:
      loadsound(choice(jungles), ch31)
      loadsound(choice(jungles), ch31)
  if pos.subterrain != 1 and ch31.get_busy():
    ch31.fadeout(200)
    ch45.fadeout(200)
    ch46.fadeout(200)
  
  # Marsh.
  if pos.subterrain == 2 and pos.sight:
    if ticks() >= windtime1+wind_count1 and ch45.get_busy() == False:
      ch45.set_volume(uniform(0.1, 1.0), uniform(0.1, 1.0))
      loadsound(choice(forestwinds), ch45)
      windtime1 = ticks()
      wind_count1 = randint(5000, 15000)
    if ticks() >= windtime2+wind_count2 and ch46.get_busy() == False:
      ch46.set_volume(uniform(0.1, 1.0), uniform(0.1, 1.0))
      loadsound(choice(forestwinds), ch46)
      windtime2 = ticks()
      wind_count2 = randint(5000, 15000)
    if ch32.get_busy() == False:
      if position.terrain == 3:
        loadsound("marsh2", ch32)
      if position.terrain == 1:
        loadsound("marsh3", ch32)
      if position.terrain == 2:
        loadsound("marsh4", ch32)
  if pos.subterrain != 2 and ch32.get_busy():
    ch32.fadeout(200)
    ch45.fadeout(200)
    ch46.fadeout(200)
  
  # Desert.
  if pos.terrain == 0 and pos.sight:
    if pygame.time.get_ticks() >= windtime1+wind_count1:
      pass 
    if ch20.get_busy() == False:
      loadsound(choice(deserts), ch20)
  if pos.terrain != 0 and ch20.get_busy():
    ch20.fadeout(200)
    ch45.fadeout(200)
    ch46.fadeout(200)
  
  # Plains.
  if pos.terrain == 1 and pos.sight:
    if ticks() >= windtime1+wind_count1 and ch45.get_busy() == False:
      ch45.set_volume(uniform(0.1, 0.5), uniform(0.1, 0.5))
      loadsound(choice(plainsambient), ch45)
      windtime1 = ticks()
      wind_count1 = randint(5000, 15000)
    if ticks() >= windtime2+wind_count2 and ch46.get_busy() == False:
      ch46.set_volume(uniform(0.1, 0.5), uniform(0.1, 0.5))
      loadsound(choice(plainsambient), ch46)
      windtime2 = ticks()
      wind_count2 = randint(5000, 15000)
    if ch21.get_busy() == False:
      loadsound(choice(plains), ch21)
  if pos.terrain != 1 and ch21.get_busy():
    ch21.fadeout(200)
    ch45.fadeout(200)
    ch46.fadeout(200)
  
  # Grassland.
  if pos.terrain == 2 and pos.sight:
    if ticks() >= windtime1+wind_count1 and ch45.get_busy() == False:
      ch45.set_volume(uniform(0.1, 0.5), uniform(0.1, 0.5))
      loadsound(choice(plainsambient), ch45)
      windtime1 = ticks()
      wind_count1 = randint(5000, 15000)
    if ticks() >= windtime2+wind_count2 and ch46.get_busy() == False:
      ch46.set_volume(uniform(0.1, 0.5), uniform(0.1, 0.5))
      loadsound(choice(plainsambient), ch46)
      windtime2 = ticks()
      wind_count2 = randint(5000, 15000) 
    if ch22.get_busy() == False:
      ch22.set_volume(0.7)
      loadsound("grass1", ch22)
  if pos.terrain != 2 and ch22.get_busy():
    ch22.fadeout(200)
    ch45.fadeout(200)
    ch46.fadeout(200)
  
  # Tundra.
  if pos.terrain == 3 and pos.sight:
    if ticks() >= windtime1+wind_count1 and ch45.get_busy() == False:
      ch45.set_volume(uniform(0.1, 0.5), uniform(0.1, 0.5))
      loadsound(choice(tundrawinds), ch45)
      windtime1 = ticks()
      wind_count1 = randint(5000, 15000)
    if ticks() >= windtime2+wind_count2 and ch46.get_busy() == False:
      ch46.set_volume(uniform(0.1, 0.5), uniform(0.1, 0.5))
      loadsound(choice(tundrawinds), ch46)
      windtime2 = ticks()
      wind_count2 = randint(5000, 15000) 
    if ch23.get_busy() == False:
      loadsound(choice(tundras), ch23)
  if pos.terrain != 3 and ch23.get_busy():
    ch23.fadeout(200)
    ch45.fadeout(200)
    ch46.fadeout(200)
  
  # Snow.
  if pos.terrain == 4 and pos.sight:
    if ticks() >= windtime1+wind_count1 and ch45.get_busy() == False:
      ch45.set_volume(uniform(0.1, 0.7), uniform(0.1, 0.7))
      loadsound(choice(icewinds), ch45)
      windtime1 = ticks()
      wind_count1 = randint(5000, 15000)
    if ticks() >= windtime2+wind_count2 and ch46.get_busy() == False:
      ch46.set_volume(uniform(0.1, 0.7), uniform(0.1, 0.7))
      loadsound(choice(icewinds), ch46)
      windtime2 = ticks()
      wind_count2 = randint(5000, 15000)
    if ch24.get_busy() == False:
      loadsound(choice(tundras), ch24)
  if pos.terrain != 4 and ch24.get_busy():
    ch24.fadeout(200)
    ch45.fadeout(200)
    ch46.fadeout(200)
  
  # Ice.
  if pos.terrain == 8 and pos.sight:
    if ticks() >= windtime1+wind_count1 and ch45.get_busy() == False:
      ch45.set_volume(uniform(0.1, 0.5), uniform(0.1, 0.5))
      loadsound(choice(icewinds), ch45)
      windtime1 = ticks()
      wind_count1 = randint(5000, 15000)
    if ticks() >= windtime2+wind_count2 and ch46.get_busy() == False:
      ch46.set_volume(uniform(0.1, 0.5), uniform(0.1, 0.5))
      loadsound(choice(icewinds), ch46)
      windtime2 = ticks()
      wind_count2 = randint(5000, 15000)
    if ch28.get_busy() == False:
      loadsound(choice(ices), ch28)
  if pos.terrain != 8 and ch28.get_busy():
    ch28.fadeout(200)
    ch45.fadeout(200)
    ch46.fadeout(200)
  
  # Mountain.
  if pos.terrain == 5 and pos.sight:
    if pygame.time.get_ticks() >= windtime1+wind_count1:
      pass 
    if ch25.get_busy() == False:
      ch25.set_volume(0.3)
      loadsound(choice(mountains), ch25)
  if pos.terrain != 5 and ch25.get_busy():
    ch25.fadeout(200)

#   Coast.
  if pos.terrain == 6 and pos.sight: 
    ch26.set_volume(0.2)
    if pygame.time.get_ticks() >= windtime1+wind_count1:
      pass
    if ch26.get_busy() == False:
      loadsound(choice(oceans), ch26)
  if pos.terrain != 6 and ch26.get_busy():
    ch26.fadeout(200)
  
  # Ocean.
  if pos.terrain == 7 and pos.sight:
    ch27.set_volume(0.4)
    if ch27.get_busy() == False:
      loadsound(choice(oceans), ch27)
  elif pos.terrain != 7 and ch27.get_busy():
    ch27.fadeout(200)

def preaction(player, pos):
  global checknext, tomove
  
  playername = player.player
  item = list()
  for tech in player.researched:
    for imp in tech.improvements:
      for tech_rq in imp.tech.rq:
        if tech_rq in player.researched:
          item.append(imp)
  
  x = 0
  say = 1
  sp.speak("Select an improvement", 1)
  sleep(0.5)
  while True:
    sleep(0.1)
    if say:
      say = 0
      sp.speak(item[x].name, 1)
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
        sp.speak(enabled_t)
        Pdb().set_trace()
        sp.speak(disabled_t)
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        x = selector(item, x, go="up")
        say = 1
      if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        x = selector(item, x, go="down")
        say = 1
        
      if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        pass
        
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        loadsound("back1")
        sleep(0.5)
        return

    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        x = selector(tospeak, x, go="up")
        say = 1
      if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        x = selector(tospeak, x, go="down")
        say = 1
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        wait = loadsound("selected1")
        sleep(wait)
        return x
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        wait = loadsound("selected1")
        sleep(wait)
        return x

def quiting():
  global cityviewer, cityview, ct, info, loop, rangattack, rangunit, square
  global tomove
  if cityview:
    loadsound("cityviewer1")
    players[num].position = wmap[city.location]
    ct = 0
    cityview = 0
    info = 1
    return
  if builder:
    indice = asking(asksave_t, sound=0)
    if indice == 0:
      exit()
    if indice == 1:
      file = open(name, "wb")
      file.write(dumps(globales))
      file.close()
      sp.speak(mapsaved_t)
      sleep(0.5)
      exit()
    else:
      return
  if cityview == 0:
    if rangattack:
      rangattack = 0
      rangunit = list()
      square = list()
      loadsound('back1')
      return
    if tomove:
      tomove= list()
      loadsound('back1') 
      return
    if tomove == list():
      ask = asking(warning8_t, sound=0)
      if ask == 0: 
        return
      if ask == 1:
        sp.speak("saliendo.")
        sleep(0.5)
        loop = 0

def remove_unit():
  global wmap
  for tile in wmap:
    for unit in tile.military+tile.civil:
      unit.units = [u for u in unit.units if u.hitpoint > 0]
  
  for tile in wmap:
    tile.civil = [unit for unit in tile.civil if unit.hitpoint > 0]
    tile.military = [unit for unit in tile.military if unit.hitpoint > 0]
  
  for pl in players:
    pl.units = [unit for unit in pl.units if unit.hitpoint > 0]

def savinggame():
  pass

def sayitemattr(attr):
  sp.speak(attr)

def selector(item, x, go='', wrap=0, sound="s1", snd=1):
  
  if go == 'up':
    if x == 0 and wrap == 1:
      x = len(item) - 1
      if snd: loadsound(sound)
      return x
    
    if x == 0 and wrap == 0:
      loadsound("errn1")
      return x
    else:
      x -= 1
      if snd: loadsound(sound)
      return x
  
  if go == 'down':
    if x == len(item) - 1  and wrap:
      x = 0
      if snd: loadsound(sound)
      return x
    
    if x == len(item) - 1  and wrap == 0: 
      loadsound("errn1")
      return x
    else:
      x += 1
      if snd: loadsound(sound)
      return x

def set_actions(event, position, unit):
  if unit.is_worker:
    if position.city == None:
      items = get_items(player, "improvement", unit)
      item_selection(city, items, player, position, "improvements", unit)
    if position.city:
      loadsound('errn1')
  
  if unit.is_settler and unit.moves > 0:
    ask = asking(warning1_t)
    if ask == 0: return
    loadsound('buildconstruct1')
    add_city(player, position)
    set_city(player)
    set_science(player)
    unit.hitpoint = -1
    remove_unit()
    tomove = list()
    get_units(position)
    set_units(can_combat)

def set_city(player):
  global players
  for city in player.cities:
    pos = wmap[city.location]
    
    city.culture = 0
    city.food = pos.totalfood
    city.gold = pos.totalgold
    city.happiness = 0
    city.heal = 0
    city.production = pos.totalproduction
    city.science = city.population
    city.resources = list()
    city.unhappiness = city.population
    
    city.gold+= city.population
    
    pos.c_defense = 0
    pos.c_food = 0
    pos.c_gold = 0
    pos.c_heal = 0
    pos.c_production = 0
    pos.c_stack = 0
    
    for o in city.owns:
      o.c_defense = 0
      o.c_food = 0
      o.c_gold = 0
      o.c_heal = 0
      o.c_production = 0
      o.c_stack = 0
    
    for b in city.buildings:
      b.setself(player, city)
      city.culture += b.culture
      city.food += b.food
      city.happiness += b.happiness
      city.heal += b.heal
      city.gold += b.gold
      city.production += b.production
      city.science += b.science
      
      pos.c_defense += b.defense
      pos.c_heal += b.heal
      pos.c_stack += b.stack
    
    if city.happiness-city.unhappiness < 0:
      city.gold += city.happiness-city.unhappiness
    
    #blocking tiles.    
    for o in city.owns:
      blocked = 0
      for unit in o.military:
        if unit.player not in player.friends:
          blocked = 1
        if blocked == 1:
          if o.is_working:
            o.is_working = 0
            city.is_working -= 1
            
      if blocked == 0:
        if o.is_working:
          city.food += o.totalfood
          city.gold += o.totalgold
          city.production += o.totalproduction
        #Adding resources to city.
        if (o.improvement and o.improvement.resource 
          and o.improvement.resource not in city.resources):
          city.resources.append(o.improvement.resource)
        #Adding improvement to city.
        if o.improvement and o.improvement not in city.improvements:
          city.improvements.append(o.improvement)

def set_info(event, position):
  global can_combat, info, tomove, x1, x2
  if event.key == pygame.K_t and cityview == 0:
    get_units(position)
    x1 = 0
    if can_combat: 
      can_combat = 0
      sp.speak('{} {}.'.format(civil_t, len(position.civil)))
      set_units(can_combat)
    elif can_combat == 0: 
      can_combat = 1
      sp.speak('{} {}.'.format(military_t, len(position.military)))
      set_units(can_combat)
  
  
  if (event.key == pygame.K_PAGEUP and cityview == 0 and position.sight 
    or position.player in player.seen ):
    if allunits:
      x1 = selector(allunits, x1, go='up')
      tomove = allunits[x1]
      describeunit(tomove)
  if (event.key == pygame.K_PAGEDOWN and cityview == 0 and position.sight
    or position.player in player.seen ):
    if allunits:
      x1 = selector(allunits, x1, go='down')
      tomove = allunits[x1]
      describeunit(tomove)
  
  
  if cityview == 0 and tomove == []:
    info_tile(event, position)
  if cityview:
    info_city(event, position)
  if tomove:
    info_unit(event, position)
  

def set_move(event, position):
  global checknext
  if event.key == movementkeys[0]:
    if position not in west and position not in wmap[0:width-1] and tomove:
      checknext = wmap[wmap.index(position)-width-1]
    else:
      loadsound("errn2")
  if event.key == movementkeys[1]:
    if position not in wmap[0:width-1]:
      checknext = wmap[wmap.index(position)-width]
    else:
      loadsound("errn2")
  if event.key == movementkeys[2]:
    if position not in east and position not in wmap[0:width-1]:
      checknext = wmap[wmap.index(position)-width+1]
    else:
      loadsound("errn2")
  if event.key == movementkeys[3]:
    if position not in west:
      checknext = wmap[wmap.index(position)-1]
    else:
      loadsound("errn2")
  if event.key == movementkeys[4]:
    if position not in east:
      checknext = wmap[wmap.index(position)+1]
    else:
      loadsound("errn2")
  if event.key == movementkeys[5]:
    if position not in west and position not in wmap[len(wmap)-width:]:
      checknext = wmap[wmap.index(position)+width-1]
    else:
      loadsound("errn2")
  if event.key == movementkeys[6]:
    if position not in wmap[len(wmap)-width:]:
      checknext = wmap[wmap.index(position)+width]
    else:
      loadsound("errn2")
  if event.key == movementkeys[7]:
    if position not in east and position not in wmap[len(wmap)-width:]:
      checknext = wmap[wmap.index(position)+width+1]
    else:
      loadsound("errn2")

def set_movement():
  global checknext, position, player, tomove
  position = wmap[tomove.location]
  square = setplace(position, value=1, action='return')
  if tomove.moveto[0] in square:
    sp.speak('esta cerca')
    sleep(1)
    checknext = tomove.moveto[0]
    tomove.moveto = list()
    setmove()
    return
  if tomove.moveto[0] not in square:
    sp.speak('se revisara')
    checknext = get_move(tomove)
    tomove.moved.append(wmap.index(checknext))
    setmove()

def set_pillage(player, tomove):
  global position
  if (tomove and tomove.player == player.player and tomove.moves   
    and tomove.can_pillage and position.improvement  
    and position.player not in player.friends): 
    
    if  position.improvement.turns == 0: 
      tomove.moves -= 1
      position.improvement.turns += position.improvement.turns_m//2
      loot = position.totalfood+position.totalproduction
      if position.totalgold: loot *= position.totalgold
      loot += tomove.loot
      player.gold += loot
      sp.speak('{} {}.'.format(loot, pillaged_t),1)
      if position.improvement.turns >= position.improvement.turns_m:
        sp.speak('{} {}.'.format(position.improvement.name, destroyed),1)
        position.improvement = None
        return
    
    if  position.improvement.turns:
      sp.speak('{} {}.'.format(position.improvement.name, destroyed),1)
      tomove.moves -= 1
      position.improvement = None
      return

def setplace(position, value=0, action=""):
  global wmap
  count = 0
  r = position.y
  l = position.y
  items1 = [position.y]
  
  # For right.
  while count < value:
    if r < width and count < value:
      r+= 1
      items1.append(r)
      count += 1
    if r == width:
      items1.append(r)
      count = value
  
  # For left.
  count = 0
  while count < value:
    if l > 1 and  count < value:
      l -= 1
      items1.append(l)
      count += 1
    if l == 1 and count < value:
      items1.append(l)
      count = value
  
  items2 = list()
  for i in wmap:
    if i.x >= position.x-value and i.x <= position.x+value and i.y in items1:
      items2.append(i)      
    
  for i in items2:
    if action == "return":
      return items2
    if action == "block":
      i.starter = 0

def setplacename():
  say = 1
  name = str()
  loadsound("s1")
  sp.speak('type a name')
  pygame.time.wait(200)
  while True:
    if say:
      sp.speak(name)
      say = 0
      
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key != pygame.K_BACKSPACE:
        name += event.unicode
        say = 1
      if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
        if len(name) >0:
          name = name[:-1]
          say = 1
        else:
          loadsound("errn1")
      if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        if name.isspace() == False: 
          loadsound("s1")
          item = str(name[:-1])
          return item
        else:
          loadsound("errn1")
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        wait = loadsound("back1")
        pygame.time.wait(wait)
        return

def setplayer(player):
  player.population = 0
  player.culture = 0
  player.science = 0
  player.happiness = 0
  player.unhappiness = 0
  player.resources = list()
  player.income = 0
  player.outcome = 0
  for unit in player.units: player.outcome += unit.maintenance
  set_city(player)
  for city in player.cities:
    player.population += city.population
    player.culture += city.culture
    player.science += city.science
    player.happiness += city.happiness
    player.unhappiness += city.unhappiness
    player.resources += city.resources
    player.income += city.gold
    for building in city.buildings: player.outcome += building.maintenance

def setplayersstart():
  global numplayers, num, players, position, turn
  
  nomads = 0  
  num = 0
  numplayers = 1
  player = Player()
  players = [DC(player) for i in range(numplayers)]
  if nomads: 
    players.append(DC(player))
    players[-1].nation = nomads
    players[-1].ai = 1
    players[-1].nomads = 1
    
#   players[0].position = wmap[225]
#   players[0].position = wmap[273]
#   players[0].position = wmap[252]
  players[0].nation = natives
  
#   players[1].position = wmap[255]
#   players[1].position = wmap[153]
#   players[1].nation = castellum
  
  players[-1].position = wmap[274]
  
  for pl in players:
    pl.player = pl.nation.name
    pl.actions = list()
    pl.actions = pl.nation.actions
    pl.commandpoints = pl.nation.commandpoints
    pl.friends = list()
    pl.citynames = pl.nation.citynames
    if pl.nation.randomname: shuffle(pl.citynames)
    pl.enemies = list()
    pl.cities = list()
    pl.improvements = list()
    pl.units = list()
    pl.revealed = list()
    pl.resources = list()
    pl.research = list()
    pl.researching = list()
    pl.seen= list()
    
    pl.av_buildings = pl.nation.av_buildings
    pl.av_improvements = pl.nation.av_improvements
    pl.av_units = pl.nation.av_units
    pl.researched = pl.nation.researched
    pl.av_tech = pl.nation.av_tech
    pl.initial_units = pl.nation.initial_units
    pl.initial_buildings = pl.nation.initial_buildings
    
    for res in resource_list:
      if res.visible == 1: pl.revealed.append(res)
    
    if pl.full_tech:
      for tech in pl.av_tech:
        if tech not in pl.researched: 
          pl.researched.append(DC(tech))
    
    if pl.position == None:
      pl.position = set_position(pl)
    
    setplace(pl.position, value=3, action="block")
    
    for u in pl.initial_units:
      if pl.nomads == 0:
        add_unit(pl, pl.position, u)
      if pl.nomads:
        position = set_position()
        add_unit(pl, position, u)
  
  for pl in players:
      tech.setself(pl)  
  
  for pl in players:
    if pl.cities:
      set_city(pl)  
  
  for i in wmap: i.starter = 1
  
  num = 0
  position = None
  turn = 1

def set_population(city):
  global players

  city.popgrowth += city.food-(city.population *2)
  sp.speak(city.popgrowth)
  if city.popgrowth > 0:
    sp.speak('avansa')
    if city.popgrowth >= city.nextpop:
      sp.speak('crece')
      city.population += 1
      city.popgrowth -= city.nextpop
    return
  if city.popgrowth < 0:
    sp.speak('decrece')
    city.population -= 1
    city.popgrowth = city.nextpop+city.popgrowth

def set_position(player=None):
  blacklist = [5, 6, 7, 8]
  if player: 
    whitelist1 = player.nation.startbasepreference
    whitelist2 = player.nation.starttoppreference
  while True:
    x = choice(wmap)
    if x.terrain not in blacklist and x.starter:
      if player:
        if x.terrain not in whitelist1 or x.subterrain not in whitelist2: 
          continue
      return x

def set_units(can_combat):
  global allunits
  allunits = list()
  for unit in tileunits:
    if unit.can_combat == can_combat:
      allunits.append(unit)

def set_science(player):
  global players
  player.science = 0
  for city in player.cities:
    player.science += city.science
    

def sight1(player):
  for t in wmap: t.sight = 0
  for t in wmap:
    if t.player in player.friends:
      t.sight = 1
      if t in player.seen: player.seen.remove(t)
      player.seen.append(t)
    
#     if t.civil+t.military:
#       for unit in t.civil+t.military:
#         if unit.player in player.friends:
#           square = setplace(t, value=1, action='return')
#           for sq in square:
#             sq.sight = 1
#             if sq in player.seen: player.seen.remove(sq)
#             player.seen.append(sq)
          
#           if t.hill: 
#             squarex = setplace(sq, value=1, action='return')
#             for sqx in squarex:
#               if sqx.terrain not in [5] and sqx not in square:
#                 sqx.sight = 1
#                 if sqx in player.seen: player.seen.remove(sqx)
#                 player.seen.append(sqx)

def sight2(player):
#   for t in wmap: t.sight = 0
  for t in wmap:
    for unit in t.military+t.civil:
      if unit.player == player.player:
        if t.hill == 0 or (t.hill and day == 0):
          square = setplace(t, value=1, action='return')
          for sq in square: 
            sq.sight = 1
            if sq not in player.seen: player.seen.append(sq)
        if t.hill and day:
          square = setplace(t, value=2, action='return')
          for sq in square: sq.sight = 1
          up = wmap[wmap.index(t)-width]
          upl = wmap[wmap.index(t)-width-1]
          upl2 = wmap[wmap.index(t)-width-2]
          upr = wmap[wmap.index(t)-width+1]
          upr2 = wmap[wmap.index(t)-width+2]
          up2 = wmap[wmap.index(t)-width*2]
          up2l = wmap[wmap.index(t)-width*2-1]
          up2r = wmap[wmap.index(t)-width*2+1]
          up2l2 = wmap[wmap.index(t)-width*2-2]
          up2r2 = wmap[wmap.index(t)-width*2+2]
          down = wmap[wmap.index(t)+width]
          downl = wmap[wmap.index(t)+width-1]
          downr = wmap[wmap.index(t)+width+1]
          downl2 = wmap[wmap.index(t)+width-2]
          downr2 = wmap[wmap.index(t)+width+2]
          down2 = wmap[wmap.index(t)+width*2]
          down2l = wmap[wmap.index(t)+width*2-1]
          down2r = wmap[wmap.index(t)+width*2+1]
          down2l2 = wmap[wmap.index(t)+width*2-2]
          down2r2 = wmap[wmap.index(t)+width*2+2]
          left = wmap[wmap.index(t)-1]
          left2 = wmap[wmap.index(t)-2]
          right = wmap[wmap.index(t)+1]
          right2 = wmap[wmap.index(t)+2]
          
          if up and up2 in square and up.terrain == 5: 
            up2.sight = 0
          if upl in square and upl.terrain == 5:
            if upl2 in square: upl2.sight = 0
            if up2l in square: up2l.sight = 0
            if up2l2 in square: up2l2.sight = 0
          
          if upr in square and upr.terrain == 5:
            if up2r in square: up2r.sight = 0
            if up2r2 in square: up2r2.sight = 0
            if upr2 in square: upr2.sight = 0
          
          if down and down2 in square and down.terrain == 5: down2.sight = 0
          if downl in square and downl.terrain == 5:
            if down2l in square: down2l.sight = 0
            if down2l2 in square: down2l2.sight = 0
            if downl2 in square: downl2.sight = 0
          if downr in square and downr.terrain == 5:
            if down2r in square: down2r.sight = 0
            if down2r2 in square: down2r2.sight = 0
            if downr2 in square: downr2.sight = 0
          
          if right  and right2 in square and right.terrain==5:
            right2.sight = 0
          if left in square and left2 in square and left.terrain == 5: left2.sight = 0
          for sq in square:
            if sq.sight and sq not in player.seen:
              player.seen.append(sq)

def show_f1(player, sound='back1'):
  loadsound(sound)
  setplayer(player)
  
  names = [gold_t, cities_t, population_t, culture_t, science_t, resources_t, 
    units_t, income_t, outcome_t, estimated_gold_t]
  coin = player.gold
  cities = len(player.cities)
  population = player.population
  culture = player.culture
  science = player.science
  resources = player.resources
  units = len(player.units)
  income = player.income
  outcome = player.outcome
  totalgold = income-outcome
  param = [coin, cities, population, culture, science, resources, units, 
    income, outcome, totalgold]
  if player.researching: 
    cost = ceil(player.researching[0].science_cost/player.science)
    researching = '{} {} {} {}'.format(researching_t, 
      player.researching[0].name, in_t, cost)
    names.insert(5, researching)
    param.insert(5, turns_t)
  
  x = 0
  say = 1
  sleep(0.5)
  while True:
    sleep(0.01)
    playsound(position)
    if say:
      say = 0
      if names[x] == resources_t:
        sp.speak(names[x]) 
        [sp.speak(res.name) for res in resources]
      else: sp.speak('{} {}.'.format(names[x], param[x]))
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
            sp.speak(enabled_t)
            Pdb().set_trace()
            sp.speak(disabled_t)
      
      if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        x = selector(names, x, go='up')
        say = 1
        sp.speak(' ', 1)
      if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        x = selector(names, x, go='down')
        say = 1
        sp.speak(' ', 1)
      
      whitelist = [pygame.K_RETURN, pygame.K_ESCAPE]
      if event.type == pygame.KEYDOWN and event.key in whitelist:
        wait = loadsound('back1')
        sleep(wait)
        sp.speak(' ', 1)
        return

def spandcity(player, city, pos):
  spread = setplace(pos, value=1, action='return')
  spreadto = list()
  whitelist = list()
  if pos not in wmap[:width]:
    sp.speak('no en norte')
    whitelist.append(1)
  if pos not in wmap[len(wmap)-1:]:
    sp.speak('no en sur)')
    whitelist.append(7)
  if pos not in west:
    sp.speak('no en oeste')
    whitelist.append(3)
  if pos not in east:
    sp.speak('no en este')
    whitelist.append(5)
  spreadto = [i for i in spread  if spread.index(i) in whitelist and i.player != player.player]
  sp.speak('fase 1 completada')
  sortedspread = [i for i in spreadto if i.resource]
  sp.speak('fase 2 completada') 
  if sortedspread:
    sp.speak('se espande por recurso') 
    sortedspread = sorted(spreadto, key=attrgetter('resource.type'))
  if sortedspread == list():
    sp.speak('se espande por food')
    sortedspread = sorted(spreadto, key=attrgetter('food', 'production'),reverse=True)
  if sortedspread: 
    sortedspread[0].player = player.player
    sortedspread[0].name = city.name
    sortedspread[0].culture = pos.culture - 100
    sp.speak('se espande a {} {}.'.format(sortedspread[0].x, sortedspread[0].y))
    city.owns.append(sortedspread[0])
    return city

def set_culture(player):
  global tospand, spread, spreadto, whitelist, sortedspread
  for city in player.cities:
    culture = city.culture
    tospand = [t for t in city.owns if t.city == None and t.resource and t.culture < 100]
    tospand = [res for res in tospand if res.resource.visible]
    if tospand:
      sp.speak('por recursos') 
      tospand = sorted(tospand, key=attrgetter('resource.type'))
    if tospand == list():
      sp.speak('food')
      tospand = [t for t in city.owns if t.city == None and t.culture < 100]
      tospand = sorted(tospand, key=attrgetter('food', 'production'),reverse=True)
    if tospand:
      tospand = tospand[0]
      tospand.culture += culture
      sp.speak('{} {}.'.format(culture, culture_t))
      if tospand.culture >= 100:
        city = spandcity(player, city, tospand)
  
def startturn(player):
  global players
  set_city(player)
  setplayer
  player.gold += player.income-player.outcome
  
  for city in player.cities:
    position = wmap[city.location]
    setpopulation(city)
    if player.researching: 
      player.researching[0].science_cost -= player.science
      if player.researching[0].science_cost < 0:
        player.researching[0].setself(player)
        player.researched.append(player.researching[0])
        player.researching.remove(player.researching[0])
    
    #  queue.
    if city.queue: city.queue[0].production_cost -= city.production
    if city.queue and city.queue[0].production_cost < 0: 
      if  len(city.queue) > 1:
        city.queue[1].production_cost += city.queue[0].production
      
      if (city.queue and city.queue[0].production_cost <= 0 
        and city.queue[0].is_building):
        city.queue[0].production_cost = 0 
        city.queue[0].setself(player, city)
        city.buildings.append(city.queue.pop(0))
      
      if (city.queue and city.queue[0].production_cost <= 0 
        and city.queue[0].is_unit):
        city.queue[0].production_cost = 0
        add_unit(player, wmap[city.location], city.queue[0])
        city.queue.remove(city.queue[0])
  
  set_city(player)
  set_science(player)
  set_culture(player)
  
  # Units.
  for unit in player.units:
    position = wmap[unit.location]
    if unit.is_worker and unit.is_working:        
      position.improvement.turns -= 1
      if position.improvement.turns == 0:
        position.improvement.location = wmap.index(position)
        player.improvements.append(position.improvement)
        unit.is_working = 0
        position.improvement.in_progress = 0
        position.improvement.addresource(player, position)
        position.improvement.setself(position)
        
    # units restoration.
    healunit(unit)
    for t in wmap:
      for unit in t.military+t.civil:
        if unit.moves < unit.moves_max:
          unit.moves = unit.moves_max

def tile_info(position):
  global info, saycord, sayitem, sayterrain, sayunit
  if info:
    info = 0 
    sayitem, sayterrain, sayunit = [1 for i in range(3)]
  
  if saycord:
    saycord = 0
    sp.speak("{} {}".format(position.x, position.y),1)
  
  if sayitem:
    sayitem = 0
  
  if sayterrain:
    sayterrain = 0
    if position.sight == 0:
      sp.speak('{}.'.format(fog_t),1)
      if position in player.seen:
        sighted = player.seen[player.seen.index(position)]
        if sighted.name: sp.speak(sighted.name,1)
        if sighted.city and sighted.city.capital == 0: sp.speak(city_t)
        if sighted.city and sighted.city.capital: sp.speak(capital_t)
        if sighted.resource and sighted.resource.visible:
          sp.speak(sighted.resource.name)
        if sighted.hill: sp.speak(hill_t)
        sp.speak(terrains[sighted.terrain])
        if sighted.subterrain >= 0: sp.speak(subterrains[sighted.subterrain])
    
    if position.sight:
      if position.name: sp.speak(position.name)
      if position.city and position.city.capital == 0: sp.speak(city_t)
      if position.city and position.city.capital: sp.speak(capital_t)
      if position.city and position.player == player.player and position.city.queue:
        remain = ceil(position.city.queue[0].production_cost 
          / position.city.production) 
        sp.speak('{} {} {} {}.'.format(position.city.queue[0].name, in_t, 
          remain, turns_t))
        
      if position.resource and position.resource in player.revealed:  
        sp.speak(position.resource.name)
      if position.hill: sp.speak(hill_t)
      sp.speak(terrains[position.terrain])
      if position.subterrain >= 0: sp.speak(subterrains[position.subterrain])
      if position.improvement: descriveimprovement(position.improvement)
      if position.is_working and sayworking:
        sayworking = 0   
        sp.speak(working_t)
  
  if sayunit:
    sayunit = 0
    if len(position.civil+position.military):
      sp.speak("{} {}, {} {}.".format(civil_t, len(position.civil), military_t, len(position.military)))
#     if position.military: sp.speak("{} {} .".format(military_t, 
#       len(position.military))) 
#     if position.civil: sp.speak("{} {}.".format(civil_t, len(position.civil)))
  
def blocktile(playername, cityname, pos):
  for pl in players:
    if pl.player == playername:
      for city in pl.cities:
        if city.name == cityname:
          city.is_working -= 1
          pos.is_working = 0


def maingame    ():
  global saycord, sayitem, sayterrain, sayunit, saydetails, tomove
  global can_combat, globales, position, builder, checknext, tomove, civil, ship
  global city, cityview, cityviewer, info, ct, rangattack, rangunit, square, x1, x2, x3
  global player, players, newturn, num, turn, day, loop
  global resource_list 
  now = datetime.now()
  logname = "logevent _ {}_{}_{}, {}_{}_{}_{}.log".format(now.year, now.month, now.day, 
    now.hour, now.minute, now.second, now.microsecond)
  
  
  allrevealed = 1
  city = None
  cityview = 0
  ct = 0
  info = 1
  can_combat = 0
  newturn = 1
  rangattack = 0
  rangunit = list()
  resource_list = sorted(resource_list, key=attrgetter('name')) 
  saycord = 0
  sayitem, sayterrain, sayunit = [1 for i in range(3)]
  sayworking = 1
  ship = list()
  square = list()
  tomove = list()
  x1 = 0
  x2 = 0
  x3 = -1
  
  if builder: 
    position = wmap[0]
  if builder == 0 and position == None:
    position = players[num].position
    get_units(position)
    set_units(can_combat)
    tomove = list()
  
  base1 = ticks()
  sleep(0.5)
  loop = 1
  while loop:
    sleep(0.1)
    mapupdate()
    player = players[num]
    if allrevealed: 
      for i in wmap: i.sight = 1
    
    if builder == 0:
      if players[num].ai:
        nextturn()
      if players[num].ai == 0:
        player.position = position
        if newturn:
          newturn = 0
          if turn > 1:position = players[num].lastposition
          sp.speak('{} {} {}.'.format(player.player, turn_t, turn))
        
        playsound(position)
        player.lastposition = position
        tile_info(position)
        if cityview:
          city = player.cities[ct]
          

    if builder:
      pass    
    
    for event in pygame.event.get():
      try:
        #debuging.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
          sp.speak(enabled_t)
          Pdb().set_trace()
          sp.speak(disabled_t)
        
        
        #Actions.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
          set_actions(event, position, tomove)
        
        
        # Map cursor.
        if event.type == pygame.KEYDOWN and event.key in explorekeys:
          explore_map(event)
          get_units(position)
          set_units(can_combat)


#Menus.
        if event.type == pygame.KEYDOWN and event.key in menukeys:
          if event.key == pygame.K_F1:
            show_f1(player)
          if event.key == pygame.K_F10:
            if player.cities:
              loadsound("back2")
              cityview = 1
              position = wmap[player.cities[ct].location]
        
        
        #Movements.
        if event.type == pygame.KEYDOWN and event.key in movementkeys:
          if tomove:
            position = wmap[tomove.location]
            set_move(event, position)
            moving()
            get_units(position)
          set_units(can_combat)
        
        
        #Next Turn.
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN 
          and pygame.key.get_mods() & pygame.KMOD_CTRL):
          nextturn()
        
        
        #tile information.
        if event.type == pygame.KEYDOWN and event.key in infokeys:
          set_info(event, position)
          
          
        #Quiting.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
          quiting()
      except:
        logging.basicConfig(filename=os.path.join("logs\\"+logname), level=logging.ERROR)
        timeerror = "{}:{}:{}.{}.".format(now.hour, now.minute, now.second, now.microsecond)
        logging.exception(timeerror)
        raise
              
        
      
def setfolders():
  if os.path.exists(os.path.join('saves')) == False:
    os.makedirs(os.path.join('saves'))
  if os.path.exists(os.path.join('logs')) == False:
    os.makedirs(os.path.join('logs'))


builder = 0


def start_app():
  if builder == 0:
    setfolders()
    loadingmap("maps//", "/*.cvm")
    definitions()
    setplayersstart()
    maingame()
  if builder == 1:
    loadingmap("maps//", "/*.cvm")
    setfolders()
  #         creatingmap()
    maingame()


start_app()