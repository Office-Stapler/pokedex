import tkinter
import sys
import os
import random
import json

class Pokedex:
    def __init__(self):
        with open('data/pokedex.json', 'r+', encoding='utf-8') as f:
            self.pokemon = json.loads(f.read())

        self.url = {'url': 'data/images/001.png', 'id': 1}
        self.win = tkinter.Tk()

        self.topFrame = tkinter.Frame(self.win)
        self.topFrame.pack(side=tkinter.TOP)

        self.bottomFrame = tkinter.Frame(self.win)
        self.bottomFrame.pack(side=tkinter.BOTTOM)

        self.leftFrame = tkinter.Frame(self.win)
        self.leftFrame.pack(side=tkinter.LEFT)

        self.rightFrame = tkinter.Frame(self.win)
        self.rightFrame.pack(side=tkinter.RIGHT)

    def next_image(self, lbl, lblname, event=None):
        nxt = self.url['id'] + 1
        new_url = f'data/images/{nxt:03d}.png'
        if nxt <= len(os.listdir('data/images')):
            lbl.image = tkinter.PhotoImage(file=new_url)
            lbl.config(image=lbl.image)
            self.url['url'] = new_url
            self.url['id'] += 1
            lblname.config(text = self.pokemon[self.url['id'] - 1]['name']['english'])

    def prev_image(self, lbl, lblname, event=None):
        prev = self.url['id'] - 1
        new_url = f'data/images/{prev:03d}.png'
        if prev >= 1:
            lbl.image = tkinter.PhotoImage(file=new_url)
            lbl.config(image=lbl.image)
            self.url['url'] = new_url
            self.url['id'] -= 1
            lblname.config(text = self.pokemon[self.url['id'] - 1]['name']['english'])

    def search_pokemon(self, lbl, lblname, search, event=None):
        text = search.get().capitalize()
        if text == '':
            return
        is_number = False
        try:
            pkid = int(text)
            if not 1 <= pkid <= len(self.pokemon):
                return
            new_url = f'data/images/{pkid:03d}.png'
            lbl.image = tkinter.PhotoImage(file=new_url)
            lbl.config(image=lbl.image)
            self.url['url'] = new_url
            self.url['id'] = pkid
            lblname.config(text = self.pokemon[self.url['id'] - 1]['name']['english'])
        except ValueError:
            for i in self.pokemon:
                if text in i['name'].values():
                    new_url = f'data/images/{i["id"]:03d}.png'
                    lbl.image = tkinter.PhotoImage(file=new_url)
                    lbl.config(image=lbl.image)
                    self.url['url'] = new_url
                    self.url['id'] = i['id']
                    lblname.config(text = self.pokemon[self.url['id'] - 1]['name']['english'])
                    break
        search.delete(0, tkinter.END)
        search.insert(0, '')


    def get_levelup_moves(self, pid = None):
        if not pid:
            with open(f'data/levelup_moves/{self.url["id"]:03d}.json', 'r') as fread:
                moves =  json.load(fread)
        else:
            with open(f'data/levelup_moves/{pid:03d}.json', 'r') as fread:
                moves =  json.load(fread)
        
        return moves

    def list_moves(self, listbox):
        listbox.delete('0', 'end')
        moves = self.get_levelup_moves()
        if not moves:
            return

        for i in list(moves.keys())[::-1]:
            listbox.insert(tkinter.END, f'==={i.upper()}==')
            for j in moves[i]:
                listbox.insert(tkinter.END, j)
