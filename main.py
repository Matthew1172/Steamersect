import math
import requests

my_key = "check env variables"
my_id = "76561198012762732"

def get_friend_ids(steam_id):
    friend_r = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship=friend".format(
        my_key, steam_id)
    result = requests.get(friend_r)
    friend_ids = []
    for i in result.json()["friendslist"]["friends"]:
        friend_ids.append(i["steamid"])
    return friend_ids

def get_owned_games(steam_id):
    games_r = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json".format(
        my_key, steam_id)
    result = requests.get(games_r).json()['response']
    if len(result) > 0:
        return [i['appid'] for i in result['games']]
    else:
        return []

def get_app_details(appid):
    get_app_details_call = "https://store.steampowered.com/api/appdetails?appids={}"
    return requests.get(get_app_details_call.format(appid)).json()

def enter_steam_ids():
    flag = False
    player_ids = []
    while not flag:
        inp = input("Please enter a steam id, then type q to stop.")
        if not (inp == 'q' or inp == 'Q'):
            player_ids.append(inp)
        else:
            flag = True
    return player_ids

'''
pre: ids is a list of steam ids we want to operate on. length of the list is less than 200.
post: return a 2d list where each element of the list is a list of games for the person respective to their index
'''
def get_games_from_ids(player_ids):
    return [get_owned_games(player_id) for player_id in player_ids]

'''
pre: input a 2d list of players games
post: output a dictionary of the union of all games and number of people that have the game
'''
def build_game_map(list_of_games):
    total = {}
    for player in list_of_games:
        for game in player:
            if game in total:
                total[game] += 1
            else:
                total[game] = 1
    return total

def filter(list_of_games, a):
    '''
    :param list_of_games: a 2d list of games where the outer list are players and the inner list are their owned games
    :return: a list of games ids where 50% or more of all players own the game
    '''
    return [k for k, v in build_game_map(list_of_games).items() if a(len(list_of_games), v)]

def get_game_details(list_of_games):
    '''
    :param list_of_games: input is a list of steam game ids
    :return: list of steam game objects. Could have an error type json object as an element, so when traversing the output of this function be mindful.
    '''
    return [requests.get("https://store.steampowered.com/api/appdetails?appids={}".format(app)).json() for app in list_of_games]

def get_game_names(list_of_game_details):
    '''
    :param list_of_game_details: list of steam game objects
    :return: list of game names
    '''
    return [v['data']['name'] for game in list_of_game_details for k, v in game.items() if v['success']]

if __name__ == '__main__':
    #ids = enter_steam_ids()
    friend_ids = get_friend_ids(my_id)
    ids = friend_ids
    ids.append(my_id)

    games = get_games_from_ids(ids)
    print(games)

    #find the intersection
    intersect = lambda n, v: True if v == n else False
    intersection = filter(games, intersect)
    #print(intersection)

    #find the majority
    maj = lambda n, v: True if v >= math.ceil(n/2) else False
    majority = filter(games, maj)
    #print(majority)
    #print the majority
    print(get_game_names(get_game_details(majority)))
