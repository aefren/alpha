# -*- encoding: utf-8 -*-
from data.classes import Event, City
from languages.english import *
from pdb import Pdb
from proyecto3 import setplace


class Start_City(Event):
  name = 'Start new city'
  turns = 0
  delete_unit = 1
  
  def addcity(self, player, position):
    position.city = City()
    square = setplace(position, value=1, action='return')
    for sq in square:
      if sq.terrain in [6, 7, 8]:
        position.city.coastalcity = 1
    city = position.city
    position.culture = 100
    
    city.location = wmap.index(player.position)
    city.buildings = []
    city.improvements = []
    city.owns = []
    city.queue = []
    city.resources = []
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
      
      
start_city = Start_City() 