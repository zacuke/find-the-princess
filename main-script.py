from typing import * 
from random import *

class user_state:
    choice: int
    nextchoice: int
    smartPlayerPhase: bool
    smartPlayerRepeatingPhase: bool

    def __init__(self, choice, nextchoice, smartPlayerPhase, smartPlayerRepeatingPhase):
        self.choice = choice
        self.nextchoice = nextchoice
        self.smartPlayerPhase = smartPlayerPhase
        self.smartPlayerRepeatingPhase = smartPlayerRepeatingPhase

    def __str__(self):
        return f"user_state({self.choice},{self.nextchoice},{self.smartPlayerPhase},{self.smartPlayerRepeatingPhase})"
    
    def __eq__(self, other):
        return self.choice == other.choice and self.nextchoice == other.nextchoice and self.smartPlayerPhase == other.smartPlayerPhase and self.smartPlayerRepeatingPhase == other.smartPlayerRepeatingPhase

def check_and_move(userChoice:int, current_location: int, max_location:int, nextChoice:int, allowOracle:bool) -> int:
    #print (userChoice, nextChoice)
    if userChoice < 1 or userChoice > max_location:
        return -1
    if userChoice == current_location:
        return 0
    elif current_location == max_location:
        return max_location-1
    elif current_location == 1:
        return 2
    elif allowOracle == False:
        randChoice = randint(0, 1)
        if randChoice == 0:
            return current_location-1
        else:
            return current_location+1
    else:
        randChoice = randint(0, 1)
        if randChoice == 0:
            if current_location-1 == nextChoice:
                return current_location+1
            else:
                return current_location-1      
        else:
            if current_location+1 == nextChoice:
                return current_location-1
            else:
                return current_location+1

def inner_game_loop(max_location:int, allowOracle:bool, allowSmartPlayer:bool) -> int:
    starting = randint(1,max_location)
    running_state =  user_state(2,3,False, False)

    if allowSmartPlayer == False:
    #     running_state.choice = 2
    #     running_state.nextchoice = 3
    # else:
        running_state.choice = randint(1,max_location)
        running_state.nextchoice = randint(1,max_location)
 
    turn_result = check_and_move(running_state.choice, starting, max_location, running_state.nextchoice, allowOracle)
    if turn_result == 0:
        return 1
    num_turns = 1
    while turn_result != 0:
        num_turns += 1
        if running_state.choice == -1:
            raise "invalid state"
        
        current_choice = running_state.choice 
        prev_state = running_state
        running_state.choice = running_state.nextchoice
        if allowSmartPlayer:
            running_state = smart_player_logic(running_state, max_location)

        else:
            running_state.nextchoice = randint(1,max_location)
        turn_result = check_and_move(running_state.choice, turn_result, max_location, running_state.nextchoice, allowOracle)
        if turn_result == 0:
            return num_turns
        
def smart_player_logic(current_state:user_state, max_location: int) -> user_state:
    choice = current_state.choice
    nextchoice = current_state.nextchoice
    smartPlayerPhase = current_state.smartPlayerPhase
    smartPlayerRepeatingPhase = current_state.smartPlayerRepeatingPhase

        
    # if smartPlayerRepeatingPhase == False and choice == nextchoice: 
    #     return user_state(-1,-1,False,False)
    
    if choice < 2 or choice > max_location-1 or nextchoice < 1 or nextchoice > max_location:
        return user_state(-1,-1,False,False)

    
    if smartPlayerPhase == False:
        nextchoice = choice + 1
        if nextchoice >= max_location:
            if smartPlayerRepeatingPhase == False:
                smartPlayerRepeatingPhase = True
                nextchoice = choice
            else:
                smartPlayerRepeatingPhase = False
                nextchoice = choice - 1
                smartPlayerPhase = True
    else:
        nextchoice = choice - 1
        if nextchoice <= 1:
            if smartPlayerRepeatingPhase == False:
                smartPlayerRepeatingPhase = True
                nextchoice = choice
            else:
                smartPlayerRepeatingPhase = False             
                nextchoice = choice + 1       
                smartPlayerPhase = False
 
    current_state.choice = choice
    current_state.nextchoice = nextchoice
    current_state.smartPlayerPhase = smartPlayerPhase
    current_state.smartPlayerRepeatingPhase = smartPlayerRepeatingPhase

    return current_state

def outer_game_loop(numberOfGames:int, gameSize:int, allowOracle:bool, allowSmartPlayer:bool) -> float:
    result_list = []
    for x in range(1,numberOfGames):  
        result = inner_game_loop(gameSize, allowOracle, allowSmartPlayer)   
        #print(result)
        result_list.append(result)
     
    return sum(result_list)/len(result_list)

seed(12345)
numgames = 200

#print('five')
assert outer_game_loop(numgames,5, False, False) == 5.296482412060302
assert outer_game_loop(numgames,5, True, False) == 17.371859296482413
assert outer_game_loop(numgames,5, False, True) == 3.3266331658291457
assert outer_game_loop(numgames,5, True, True) == 3.85929648241206

#print('six')
assert outer_game_loop(numgames,6, False, False) == 6.567839195979899
assert outer_game_loop(numgames,6, True, False) == 22.90954773869347
assert outer_game_loop(numgames,6, False, True) == 4.788944723618091
assert outer_game_loop(numgames,6, True, True) == 5.36180904522613

#print ('seven')
assert outer_game_loop(numgames,7, False, False) == 6.698492462311558
assert outer_game_loop(numgames,7, True, False) == 39.32663316582914
assert outer_game_loop(numgames,7, False, True) == 5.648241206030151
assert outer_game_loop(numgames,7, True, True) == 6.663316582914573

#print ('eight')
assert outer_game_loop(numgames,8, False, False) == 8.522613065326633
assert outer_game_loop(numgames,8, True, False) == 44.81909547738694
assert outer_game_loop(numgames,8, False, True) == 5.663316582914573
assert outer_game_loop(numgames,8, True, True) == 8.015075376884422

#print ('nine')
assert outer_game_loop(numgames,9, False, False) == 8.78894472361809
assert outer_game_loop(numgames,9, True, False) == 76.63819095477388
assert outer_game_loop(numgames,9, False, True) == 7.366834170854271
assert outer_game_loop(numgames,9, True, True) == 9.924623115577889

assert inner_game_loop(5,False, False) == 1
assert inner_game_loop(5,True, False) == 12
assert inner_game_loop(5,True, True) == 4
assert inner_game_loop(5,False, True) == 1

assert inner_game_loop(6,False, False) == 1
assert inner_game_loop(6,True, False) == 40
assert inner_game_loop(6,True, True) == 1
assert inner_game_loop(6,False, True) == 1

assert inner_game_loop(7,False, False) == 10
assert inner_game_loop(7,True, False) == 1
assert inner_game_loop(7,True, True) == 10
assert inner_game_loop(7,False, True) == 9

assert inner_game_loop(8,False, False) == 4
assert inner_game_loop(8,True, False) == 19
assert inner_game_loop(8,True, True) == 12
assert inner_game_loop(8,False, True) == 1

assert inner_game_loop(9,False, False)  == 39
assert inner_game_loop(9,True, False) == 82
assert inner_game_loop(9,True, True) == 8
assert inner_game_loop(9,False, True) == 1

assert check_and_move(1, 1, 5, 4, False)== 0
assert check_and_move(1, 2, 5, 4, False)== 1
assert check_and_move(1, 3, 5, 4, False)== 4
assert check_and_move(1, 4, 5, 4, False)== 3
assert check_and_move(1, 5, 5, 4, False)== 4
assert check_and_move(1, 1, 5, 4, True)== 0
assert check_and_move(1, 2, 5, 4, True)== 3
assert check_and_move(1, 3, 5, 4, True)== 2
assert check_and_move(1, 4, 5, 4, True)== 3
assert check_and_move(1, 5, 5, 4, True)== 4
assert check_and_move(6, 1, 5, 4, False)== -1
assert check_and_move(6, 5, 5, 4, True)== -1
assert check_and_move(2, 1, 5, 4, False) == 2
assert check_and_move(2, 1, 5, 4, True) == 2


assert smart_player_logic(user_state(1,2,False,False),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(2,2,False,False),5) == user_state(2,3,False,False)
assert smart_player_logic(user_state(3,2,False,False),5) == user_state(3,4,False,False)
assert smart_player_logic(user_state(4,2,False,False),5) == user_state(4,4,False,True)
assert smart_player_logic(user_state(5,2,False,False),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(6,2,False,False),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(1,6,False,False),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(1,2,True,False),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(2,2,True,False),5) == user_state(2,2,True,True)
assert smart_player_logic(user_state(3,2,True,False),5) == user_state(3,2,True,False)
assert smart_player_logic(user_state(4,2,True,False),5) == user_state(4,3,True,False)
assert smart_player_logic(user_state(5,2,True,False),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(6,2,True,False),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(1,6,True,False),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(1,2,True,True),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(2,2,True,True),5) == user_state(2,3,False,False)
assert smart_player_logic(user_state(3,2,True,True),5) == user_state(3,2,True,True)
assert smart_player_logic(user_state(4,2,True,True),5) == user_state(4,3,True,True)
assert smart_player_logic(user_state(5,2,True,True),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(6,2,True,True),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(1,6,True,True),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(1,2,False,True),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(2,2,False,True),5) == user_state(2,3,False,True)
assert smart_player_logic(user_state(3,2,False,True),5) == user_state(3,4,False,True)
assert smart_player_logic(user_state(4,2,False,True),5) == user_state(4,3,True,False)
assert smart_player_logic(user_state(5,2,False,True),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(6,2,False,True),5) == user_state(-1,-1,False,False)
assert smart_player_logic(user_state(1,6,False,True),5) == user_state(-1,-1,False,False)





















