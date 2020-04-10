import requests
import json
import os

class Pokemon:
    def __init__(self, name):
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        rq = json.loads(requests.get(url).text)
        self.moves = rq['moves']
        self.abilities = rq['abilities']
        self.forms = rq['forms']
        self.games = rq['game_indices']
        self.id = rq['id']
        self.items = rq['held_items']
        self.species = rq['species']
        self.sprites = rq['sprites']
        self.stats = rq['stats']
        self.types = rq['types']
        self.versions = [j['version_group']['name'] for j in rq['moves'][0]['version_group_details']]
    
    @property
    def full_moves(self):
        moves = []
        versions = []
        for i in self.moves:
            moves.append(i['move']['name'].capitalize())
            versions.append([j for j in i['version_group_details']])
        return list(zip(moves, versions))

    def export_to_json(self):
        moves = self.full_moves
        with open('moves.json', 'w+') as fwrite:
            json.dump(moves, fwrite)
        pokemon = {}
        pokemon['moves'] = self.moves
        pokemon['abilities'] = self.abilities
        pokemon['games'] = self.games
        pokemon['versions'] = self.versions
        pokemon['species'] = self.species
        pokemon['stats'] = self.stats
        pokemon['types'] = self.types
        pokemon['sprites'] = self.sprites
        
        with open('pokemon.json', 'w+') as fwrite:
            json.dump(pokemon, fwrite)
    def get_machine_moves(self):
        moves = {}
        for i in self.moves:
            for j in i['version_group_details']:
                if j['move_learn_method']['name'] == 'machine':
                    if j['version_group']['name'] not in moves:
                        moves[j['version_group']['name']] = []

                    moves[j['version_group']['name']].append(i['move']['name'])
        return moves

    def __convert(self, x):
        number = ''
        for i in x:
            number += i if i.isdigit() else ''
        return int(number)



if __name__ == '__main__':
    with open('data/pokedex.json', 'r+') as fread:
        pokedex = json.load(fread)
    
    pid = len(os.listdir('data/machine_moves/')) + 1
    while pid < len(pokedex):
        pokemon = Pokemon(pid)
        
        with open(f'data/machine_moves/{pid:03d}.json', 'w+') as fwrite:
            json.dump(pokemon.get_machine_moves(), fwrite)
        print(pokedex[pid - 1]['name']['english'] + ' finished Dumping....')
        pid += 1