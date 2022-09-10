from random import choices
from submission_helper.bot_battle import BotBattle
from submission_helper.state import *
from submission_helper.enums import *
from typing import Optional


game_info: Optional[GameInfo] = None
bot_battle = BotBattle()

def get_next_alive_player():
    next_alive = (game_info.player_id + 1) % 5
    while game_info.players_cards_num[next_alive] == 0:
        next_alive = (next_alive + 1) % 5
    return next_alive

def get_highest_health():
    if game_info.players_cards_num[get_next_alive_player()] == 2:
        return get_next_alive_player()
    i = 0
    while i < 4:
        if game_info.players_cards_num[int(game_info.player_id) + i] == 2:
            return int(game_info.player_id) + i
    while i < 4:
        if game_info.players_cards_num[int(game_info.player_id) + i] == 1:
            return int(game_info.player_id) + i
    print("Error on get_highest_health", flush = True)

def move_controller(game_info: GameInfo):
    if game_info.requested_move == RequestedMove.PrimaryAction:
        primary_action_handler(game_info: GameInfo)

    elif game_info.requested_move == RequestedMove.CounterAction:
        counter_action_handler()

    elif game_info.requested_move == RequestedMove.ChallengeAction:
        challenge_action_handler()

    elif game_info.requested_move == RequestedMove.ChallengeResponse:
        challenge_response_handler()

    elif game_info.requested_move == RequestedMove.DiscardChoice:
        discard_choice_handler()

    else:
        return Exception(f'Unknown requested move: {requested_move}')

def primary_action_handler(game_info: GameInfo):
    if game_info.balances[game_info.player_id] >= 10:
        play(PrimaryAction.Coup, game_info)
    else:
        income = 0
        exchange = 0
        ForeignAid = 0
        Tax = 0
        Steal = 0
        Assassinate = 0
        Coup = 0
        
        choose([1,2,3,4,5,6,7])

def choose(weights: list, population: list = [1,2,3,4,5,6,7]):
    return choices(population, weights, k = 1)

def play(move: int, game_info: GameInfo, target_player_id: int = get_next_alive_player()):
    if move == PrimaryAction.Income or PrimaryAction.Exchange or PrimaryAction.ForeignAid or PrimaryAction.Tax:
        bot_battle.play_primary_action(move)
    elif move == PrimaryAction.Steal:
        bot_battle.play_primary_action(move, target_player_id)
    elif move == PrimaryAction.Assassinate and game_info.balances[game_info.player_id] >= 3:
        bot_battle.play_primary_action(move, target_player_id)
    elif move == PrimaryAction.Coup and game_info.balances[game_info.player_id] >= 7:
        bot_battle.play_primary_action(move, target_player_id)
    else:
        print("Invalid Play", flush=True)
        bot_battle.play_primary_action(PrimaryAction.Income)
    return True



#For later work
def counter_action_handler():
    bot_battle.play_counter_action(CounterAction.NoCounterAction)

def challenge_action_handler():
    bot_battle.play_challenge_action(ChallengeAction.NoChallenge)

def challenge_response_handler():
    bot_battle.play_challenge_response(0)

def discard_choice_handler():
    bot_battle.play_discard_choice(0)


def is_valid_primary():
    return True



if __name__ == "__main__":
    while True:
        game_info = bot_battle.get_game_info()
        move_controller(game_info.requested_move)



