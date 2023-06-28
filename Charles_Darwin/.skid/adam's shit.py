import random
import colored
from colored import fg
import time
import sys
import os
import pymongo
from pymongo import MongoClient

num_modules = 17
module = 1
last_module = 0
possible_moves = []
alive = True
won = False
power = 100
fuel = 500
locked = 0
queen = 0
vent_shafts = []
info_panels = []
workers = []
main_menu = True
logged_in = False
Username = 0
Password = 0


def connect_db():
  myclient = pymongo.MongoClient('mongodb+srv://admin:admin@cluster0.zkk4jok.mongodb.net/test')


#  db = myclient["Python"]
#  collection = db["School"]
#  mlist = [
#    {
#      "Username": "BOBO",
#      "Password": "123"
#    },
#  ]

#mid = collection.insert_many(mlist)

def load_module():
  global module, possible_moves
  possible_moves = get_modules_from(module)


def get_modules_from(module):
  moves = []
  text_file = open("Charles_Darwin/module" + str(module) + ".txt", "r")
  for counter in range(0, 4):
    move_read = text_file.readline()
    move_read = int(move_read.strip())
    if move_read != 0:
      moves.append(move_read)
  text_file.close()
  return moves


def output_module():
  global module
  print()
  print("------------------------------------------------------------")
  print()
  print("Your are in module", module)
  print()


def output_moves():
  global possible_moves
  print()
  print("From  here  you  can  move  to  modules:  |  ", end='')
  for move in possible_moves:
    print(move, '| ', end='')
  ting = 0
  for move in possible_moves:
    ting = ting + 1
    if ting == 1:
      room_1 = move
    if ting == 2:
      room_2 = move
    if ting == 3:
      room_3 = move
    if ting == 4:
      room_4 = move
  if ting == 1:  # only 1 room
    if room_1 < 10:
      room_1 = " " + str(room_1) + " "
    print('\n     _______\n    │       │\n    │  ', room_1, ' │')

  if ting == 2:
    if room_1 < 10:
      room_1 = " " + str(room_1) + " "
    if room_2 < 10:
      room_2 = " " + str(room_2) + " "
    print('\n     _______      _______\n    │       │    │       │\n    │ ',
          room_1, ' │    │ ', room_2, ' │\n    │_______│    │_______│')

  if ting == 3:
    if room_1 < 10:
      room_1 = " " + str(room_1) + " "
    if room_2 < 10:
      room_2 = " " + str(room_2) + " "
    if room_3 < 10:
      room_3 = " " + str(room_3) + " "
    print(
      '\n     _______      _______      _______\n    │       │    │       │    │       │\n    │ ',
      room_1, ' │    │ ', room_2, ' │    │ ', room_3,
      ' │\n    │_______│    │_______│    │_______│')

  if ting == 4:
    if room_1 < 10:
      room_1 = " " + str(room_1) + " "
    if room_2 < 10:
      room_2 = " " + str(room_2) + " "
    if room_3 < 10:
      room_3 = " " + str(room_3) + " "
    if room_4 < 10:
      room_4 = " " + str(room_4) + " "
    print(
      '\n     _______      _______      _______      _______\n    │       │    │       │    │       │    │       │\n    │ ',
      room_1, ' │    │ ', room_2, ' │    │  ', room_3, ' │    │  ', room_4,
      ' │\n    │_______│    │_______│    │_______│    │_______│')


def get_action():
  global module, last_module, possible_moves
  valid_action = False
  while valid_action == False:
    print("What  do  you  want  to  do  next  ?  (MOVE,  SCANNER, MENU)")
    action = input(">")
    if action == "MOVE" or action == "m" or action == "Move" or action == "move" or action == "M":
      move = int(input("Enter  the  module  to  move  to:  "))
      if move in possible_moves:
        valid_action = True
        last_module = module
        module = move
      else:
        print("The module must be connected to the current module.")
    if action == "SCANNER" or action == "s" or action == "scanner" or action == "scan":
      command = input("Scanner Ready. Enter command (LOCK):")
      if command == "Lock" or "lock" or "LOCK" or "L" or "(Lock)" or "(LOCK)":
        lock()
    if action == "menu" or action == "MENU" or action == "Menu":
      main_menu_confirm = input(
        "Are you sure you want to leave this Game? (Y/N):")
      if main_menu_confirm == "Y" or main_menu_confirm == "y" or main_menu_confirm == "yes" or main_menu_confirm == "Yes" or main_menu_confirm == "YES":
        os.system("clear")
        main_menu == True
        start_menu()
      else:
        get_action()


def spawn_npcs():
  global num_modules, queen, vent_shafts, info_panels, workers
  module_set = []
  for counter in range(2, num_modules + 1):
    module_set.append(counter)
  random.shuffle(module_set)
  i = 0
  queen = module_set[i]
  for counter in range(0, 3):
    i = i + 1
    vent_shafts.append(module_set[i])

  for counter in range(0, 2):
    i = i + 1
    info_panels.append(module_set[i])

  for counter in range(0, 3):
    i = i + 1
    workers.append(module_set[i])


spawn_npcs()

# MAIN CODE BODY


def lock():
  global num_modules, power, locked
  new_lock = int(input("Enter a module to Lock:"))
  if new_lock < 0 or new_lock > num_modules:
    print("Invalid Module. Operation Failed.")
  elif new_lock == queen:
    print("Operation Failed. Unable to Lock Module")
  else:
    locked = new_lock
    print("Aliens cannot get into Module", locked)
  power = 25 + 5 * random.randint(0, 5)


def move_queen():
  global num_modules, module, last_module, locked, queen, won, vent_shafts
  if int(module) == queen:
    print("There it is! The queen alien is in this module...")
    moves_to_make = random.randint(1, 3)
    can_move_to_last_module = False
    while moves_to_make > 0:
      escapes = get_modules_from(queen)
      if module in escapes:
        escapes.remove(module)
      if last_module in escapes and can_move_to_last_module == False:
        escapes.remove(last_module)
      if locked in escapes:
        escapes.remove(locked)
      if len(escapes) == 0:
        won = True
        moves_to_make = 0
        print("...and the door is locked. It's trapped.")
      else:
        if moves_to_make == 1:
          print("...and has escaped.")
        queen = random.choice(escapes)
        moves_to_make = moves_to_make - 1
        can_move_to_last_module = True
        while queen in vent_shafts:
          if moves_to_make > 1:
            print("...and has escaped.")
          print("We can hear scuttling in the ventilation shafts.")
          valid_move = False
          while valid_move == False:
            valid_move = True
            queen = random.randint(1, num_modules)
            if queen in vent_shafts:
              valid_move = False


def check_vent_shafts():
  global num_modules, module, vent_shafts, fuel
  if module in vent_shafts:
    print("There is a bank of fuel cells here.")
    print("You load one into your flamethrower.")
    fuel_gained = 50
    print("Fuel was", fuel, "now reading: ", fuel + fuel_gained)
    fuel = fuel + fuel_gained
    print("The doors suddenly lock shut.")
    print("What is happening to the station?")
    print("Our only escape is to climb into the ventilation shaft.")
    print("We have no idea where we are going.")
    print("We follow the passages and find ourselves sliding down.")
    last_module = module
    module = random.randint(1, num_modules)
    load_module()


def worker_aliens():
  global module, workers, fuel, alive
  if module in workers:
    print("Startled, a young alien scuttles across the floor.")
    print("It turns and leaps towards us.")
    successful_attack = False
    while successful_attack == False:
      print("You can:")
      print()
      print("- Short blast your flamethrower to frighten it away.")
      print("- Long blast your flamethrower to try to kill it.")
      print()
      print("How will you react? (S, L)")
      action = 0
      while action not in ("s", "L"):
        action = input("Press the trigger: ")
        fuel_used = int(input("How much fuel will you use? ..."))
        fuel = fuel - fuel_used
        if fuel <= 0:
          alive = False
          return
        if action == "S" or action == "s":
          fuel_needed = 36 + 10 * random.randint(0, 5)
        if action == "L" or action == "l":
          fuel_needed = 96 + 10 * random.randint(0, 5)
        if fuel_used >= fuel_needed:
          successful_attack = True
        else:
          print("The alien squeals but is not dead. It’s angry.")
      if action == "s" or action == "S":
        print("The Alien scuttles away into the corner of the room.")
      if action == "l" or action == "L":
        print("The Alien has been destroyed.")
        workers.remove(module)
      print()


def intuition():
  global possible_moves, workers, vent_shafts
  for connected_module in possible_moves:
    if connected_module in workers:
      print("I can hear something scuttling")
    if connected_module in vent_shafts:
      print("I can feel cold Air")


def coin_shop():
  global logged_in, Username, Password
  if logged_in == False:
    os.system("clear")
    start_menu()
    print("Unable to load Coins! - Not Logged In")
    print("Go back to the Main Menu to Create a Account or Login!")
  else:
    os.system("clear")
    myclient = pymongo.MongoClient('mongodb+srv://admin:admin@cluster0.zkk4jok.mongodb.net/test')
    db = myclient["Python"]
    collection = db["School"]
    doc = collection.find_one({"Username": Username, "Password": Password})
    #c = fg("yellow")
    #b = fg("white")
    print("  _____       _          _____ _                 ")
    print(" / ____|     (_)        / ____| |                ")
    print("| |     ___  _ _ __    | (___ | |__   ___  _ __  ")
    print("| |    / _ \| | '_ \    \___ \| '_ \ / _ \| '_ \ ")
    print("| |___| (_) | | | | |   ____) | | | | (_) | |_) |")
    print(" \_____\___/|_|_| |_|  |_____/|_| |_|\___/| .__/ ")
    print("                                          | |   ")
    print("                                          |_|")
    print("Coins -", doc["Coins"])
    print("  ⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽ ")
    print(" |       Upgrade      |             Description            |   Price   |   Code    |")
    print(" |――――――――――――――――――――|――――――――――――――――――――――――――――――――――――|―――――――――――|―――――――――――|")
    print(" |    Teleportation   | Teleport to any Module (1-17)      |   $250    |     1     |")
    print(" |――――――――――――――――――――|――――――――――――――――――――――――――――――――――――|―――――――――――|―――――――――――|")
    print(" |   More Fuel (x3)   | Adds 50 Fuel with every Purchase   |   $50     |     2     |")
    print(" |――――――――――――――――――――|――――――――――――――――――――――――――――――――――――|―――――――――――|―――――――――――|")
    print(" |   Double Workers   | More workers , More coins to Earn  |   $150    |     3     |")
    print(" |――――――――――――――――――――|――――――――――――――――――――――――――――――――――――|―――――――――――|―――――――――――|")
    print(" |    Double Coins    | Earn x2 amount of Coins            |   $150    |     4     |")
    print(" |――――――――――――――――――――|――――――――――――――――――――――――――――――――――――|―――――――――――|―――――――――――|")
    print(" |    Extra Life(s)   | Extra Lifes to bypass Death        |   $300    |     5     |")
    print(" |――――――――――――――――――――|――――――――――――――――――――――――――――――――――――|―――――――――――|―――――――――――|")
    print(" |        EMP         | Lock Every Module at Once!         |   $450    |     6     |")
    print("  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ")
    print("To purchase an item enter the code, to go back to the main menu enter (MENU)")
    ting = input("Enter Code to Purchase or (MENU):")
    if ting == "MENU" or ting == "m" or ting == "M" or ting == "menu" or ting == "Menu":
      os.system("clear")
      start_menu()
    else:
      os.system("clear")
      start_menu()


# Do main menu with a bunch of stuff people can leave the game by doing MENU and then confirming


def start_screen():
  c = fg("light_green")
  b = fg("white")
  print(b + " ________          __ __                       ")
  print(b + "|        \        |  \  \                      ")
  print(b + " \▓▓▓▓▓▓▓▓ ______ | ▓▓\▓▓__    __ ______ ____  ")
  print(b + "   | ▓▓   /      \| ▓▓  \  \  |  \      \    \ ")
  print(b + "   | ▓▓  |  ▓▓▓▓▓▓\ ▓▓ ▓▓ ▓▓  | ▓▓ ▓▓▓▓▓▓\▓▓▓▓\ ")
  print(b + "   | ▓▓  | ▓▓    ▓▓ ▓▓ ▓▓ ▓▓  | ▓▓ ▓▓ | ▓▓ | ▓▓ ")
  print(b + "   | ▓▓  | ▓▓▓▓▓▓▓▓ ▓▓ ▓▓ ▓▓__/ ▓▓ ▓▓ | ▓▓ | ▓▓ ")
  print(b + "   | ▓▓   \▓▓     \ ▓▓ ▓▓\▓▓    ▓▓ ▓▓ | ▓▓ | ▓▓ ")
  print(b + "    \▓▓    \▓▓▓▓▓▓▓\▓▓\▓▓ \▓▓▓▓▓▓ \▓▓  \▓▓  \▓▓ ")
  print(b + "             ___  _  _        ___      _   ___   _   __   ")
  print(b + "            | _ )| || |      /   \  _ | | / __| / | /  \  ")
  print(b + "            | _ \ \_. |      | - | | || | \__ \ | || () | ")
  print(b + "            |___/ |__/       |_|_|  \__/  |___/ |_| \__/  ")
  print(b + " ")


def connecting_animation():
  load_str = "connecting to database..."
  ls_len = len(load_str)
  animation = "|/-\\"
  anicount = 0
  counttime = 0
  i = 0
  while (counttime != 65):
    time.sleep(0.04)
    load_str_list = list(load_str)
    x = ord(load_str_list[i])
    y = 0
    # if the character is "." or " ", keep it unaltered
    # switch uppercase to lowercase and vice-versa
    if x != 32 and x != 46:
      if x > 90:
        y = x - 32
      else:
        y = x + 32
      load_str_list[i] = chr(y)
    res = ''
    for j in range(ls_len):
      res = res + load_str_list[j]
    sys.stdout.write("\r" + res + animation[anicount])
    sys.stdout.flush()
    load_str = res
    anicount = (anicount + 1) % 4
    i = (i + 1) % ls_len
    counttime = counttime + 1
  if os.name == "nt":
    os.system("cls")

  # for linux / Mac OS
  else:
    os.system("clear")


def load_animation():
  load_str = "telium is loading..."
  ls_len = len(load_str)
  animation = "|/-\\"
  anicount = 0
  counttime = 0
  i = 0
  while (counttime != 65):
    time.sleep(0.04)
    load_str_list = list(load_str)
    x = ord(load_str_list[i])
    y = 0
    # if the character is "." or " ", keep it unaltered
    # switch uppercase to lowercase and vice-versa
    if x != 32 and x != 46:
      if x > 90:
        y = x - 32
      else:
        y = x + 32
      load_str_list[i] = chr(y)
    res = ''
    for j in range(ls_len):
      res = res + load_str_list[j]
    sys.stdout.write("\r" + res + animation[anicount])
    sys.stdout.flush()
    load_str = res
    anicount = (anicount + 1) % 4
    i = (i + 1) % ls_len
    counttime = counttime + 1
  if os.name == "nt":
    os.system("cls")

  # for linux / Mac OS
  else:
    os.system("clear")



def alien_info():
  print("Queen Alien is located in module:", queen)
  print("Ventilation shafts are located in modules:", vent_shafts)
  print("Information panels are located in modules:", info_panels)
  print("Worker aliens are located in modules:", workers)


def start_menu():
  global main_menu, Username, Password, logged_in
  myclient = pymongo.MongoClient('mongodb+srv://admin:admin@cluster0.zkk4jok.mongodb.net/test')
  db = myclient["Python"]
  collection = db["School"]
  main_menu == True
  print("Connected to Database - Cluster0.zkk4jok")
  print(" __  __       _         __  __                  ")
  print("|  \/  |     (_)       |  \/  |                 ")
  print("| \  / | __ _ _ _ __   | \  / | ___ _ __  _   _ ")
  print("| |\/| |/ _` | | '_ \  | |\/| |/ _ \ '_ \| | | |")
  print("| |  | | (_| | | | | | | |  | |  __/ | | | |_| |")
  print("|_|  |_|\__,_|_|_| |_| |_|  |_|\___|_| |_|\__,_|")
  print()
  print(
    "Start - S, Login / Sign Up (Save Data) - L, Stats (Saved Data)- D, Map - M"
  )
  action = input(">")
  if action == "S" or action == "s":
    main_menu = False
  if action == "L" or action == "l":
    action2 = input("Login (L) or Create Account (C):")
    if action2 == "l" or action2 == "L":
      username = input("Username:")
      password = input("Password:")
      doc = collection.find_one({"Username": username, "Password": password})
      if doc:
        print("Logged Into account - ", doc["Username"])
        logged_in = True
        Username = username
        Password = password
        main_menu = False
      else:
        os.system("clear")
        print("Previous Login attempt Failed!")
        print()
        start_menu()
    if action2 == "c" or action2 == "C":
      username2 = input("Username:")
      password2 = input("Password:")
      confirm_password = input("Confirm Password:")
      if password2 == confirm_password:
        doc = collection.find_one({"Username": username2})
        if doc:
          if username2 == doc["Username"]:
            os.system("clear")
            print("Username already in Use, Please try Again!")
            print()
            start_menu()
        else:  # doc not found ie username doesnt exist
          new_account = [{
            "Username": username2,
            "Password": password2,
            "Coins": 0
          }]
          collection.insert_many(new_account)
          logged_in = True
          print(logged_in)
          Username = username2
          Password = password2
          print("Account Created Successfully!")
          ting = input("Back to Main Menu (Y) - ")
          if ting == "Y" or ting == "y" or ting == "yes" or ting == "YES":
            os.system("clear")
            start_menu()
          else:
            os.system("clear")
            start_menu()
      else:
        os.system("clear")
        print("Previous Account Creation Attempt Failed!")
        print()
        start_menu()
  if action == "D" or action == "d":
    coin_shop()
  if action == "m" or action == "M":
    print("\033[1;37;50m")
    print("                                   ___                         ")
    print("                                  | 1 |                         ")
    print("                                  |‾‾‾|                           ")
    print("                                  |   |                           ")
    print("                 ___          ___ /   \ ___          ___           ")
    print("                | 4 | ‾‾‾‾‾‾ | 2 |     | 3 | ‾‾‾‾‾‾ | 5 |            ")
    print("                |‾‾‾| ‾‾‾‾‾‾ |‾‾‾|     |‾‾‾| ‾‾‾‾‾‾ |‾‾‾|             ")
    print("   ___         /   /  ___   /    |     |    \   ___  \   \         ___  ")
    print("  | 6 |‾‾‾‾‾‾‾     ‾‾| 7 |‾‾    /       \    ‾‾| 8 |‾‾     ‾‾‾‾‾‾‾| 9 |   ")
    print("  \‾‾‾\‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ‾‾‾ ‾‾‾‾‾           ‾‾‾‾‾ ‾‾‾ ‾‾‾‾‾‾‾‾‾‾‾‾‾‾/‾‾‾/  ")
    print("   \   \                           ___                           /   /   ")
    print("    \    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ |10 | ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾    /        ")
    print("     ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾/  / \  \‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾        ")
    print("       ___             ___     /  /   \  \      ___             ___        ")
    print("      |13 | ‾‾‾‾‾‾‾‾‾ |11 | ‾‾   /     \  ‾‾‾‾ |12 | ‾‾‾‾‾‾‾‾‾ |14 |                ")
    print("       ‾‾‾  ‾‾‾‾‾‾‾‾‾ \‾‾‾\ ‾‾‾‾         ‾‾‾‾‾ |‾‾‾| ‾‾‾‾‾‾‾‾‾  ‾‾‾                    ")
    print("                       \   \       ___         |   |                   ")
    print("                        \    ‾‾‾‾ |15 |        |   |                       ")
    print("                        |   |‾‾‾‾ \‾‾‾ \       |   |                        ")
    print("                        |___|      \    \___   |   |                  ")
    print("                        |16 | ‾‾‾‾‾‾    |17 | ‾    /                    ")
    print("                         ‾‾‾  ‾‾‾‾‾‾‾‾‾  ‾‾‾  ‾‾‾‾                           ")
    print("                                                                        ")
    print("                                                                        ")
    b = fg("white")
    print(b + " ")
    ting = input("Back to Main Menu (Y) - ")
    if ting == "Y" or ting == "y" or ting == "yes" or ting == "YES":
      os.system("clear")
      start_menu()
    else:
      os.system("clear")
      start_menu()



start_screen()
load_animation()
start_screen()
connecting_animation()
connect_db()
start_menu()




while alive and not won:
  if won == False and alive == True and main_menu == False:
    check_vent_shafts()
    worker_aliens()
    move_queen()
    load_module()
    intuition()
    output_moves()
    get_action()
    #os.system("clear")

if won == True:
  print("The queen is trapped and you burn it to death with your flamethrower")
  print("Game Over. You Win!")
if alive == False:
  print(
    "The station has run out of power.	Unable to sustain life support, you die."
  )
