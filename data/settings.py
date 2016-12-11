lang = 0 # 0 = english, 1 = spanish.

# speaker options are "jaws", "sapi5", 'NVDA'.
speaker = "NVDA"

if lang == 0:
  from languages.english import *
if lang == 1:
  from languages.spanish import * 