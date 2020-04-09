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
        self.id = rq['game_indices'][0]['game_index']
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


if __name__ == '__main__':
    name = input()
    pokemon = Pokemon(name)
    print(pokemon.get_levelup_moves())