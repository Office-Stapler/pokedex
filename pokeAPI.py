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
    
    def __convert(self, x):
        number = ''
        for i in x:
            number += i if i.isdigit() else ''
        return int(number)

    def get_levelup_moves(self):
        moves = {}
        for move in self.full_moves:
            for j in move[1]:
                ver = j['version_group']['name']
                if ver not in moves:
                    moves[ver] = []

                if j['level_learned_at']:
                    moves[ver].append(f'{move[0]} learnt at level {j["level_learned_at"]}')
        self.versions = list(moves.keys())
        for version in self.versions:
            moves[version] = sorted(moves[version], key=lambda x: self.__convert(x))
        return moves


if __name__ == '__main__':
    pid = len(os.listdir('data/moves/')) + 1

    with open('data/pokedex.json', 'r+', encoding='utf-8') as f:
        pokemon = json.loads(f.read())

    while pid <= len(os.listdir('data/images')):
        fpokemon = pokemon[pid - 1]['name']['english'].lower()
        npokemon = Pokemon(pid)
        with open(f'data/moves/{pid:03d}.json', 'w+') as fwrite:
            json.dump(npokemon.get_levelup_moves(), fwrite)
            print(f'Done Dumping {fpokemon.capitalize()}.json.... ')
        pid += 1