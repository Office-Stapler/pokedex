import tkinter
import sys
import os
import random
import json


class Win:
    def __init__(self, name):
        self.win = tkinter.Tk()
        self.win.title(name.replace('-',' '))
        self.win.geometry('250x250')
        with open('data/moves.json') as fread:
            moves = json.load(fread)

        for i in moves:
            if i['ename'].lower() == name.replace('-', ' ').lower():
                self.move = i
                break

        lblname = tkinter.Label(self.win, text=f'About {name.replace("-"," ")}', font=('Arial', 15))
        lblname.pack()
        typ = tkinter.PhotoImage(file=f'data/types_images/{self.move["type"].lower()}.png', master=self.win)
        lbltyp = tkinter.Label(self.win, image=typ)
        lbltyp.image = typ
        lbltyp.config(image=typ)
        lbltyp.pack()
        
        lblacc = tkinter.Label(self.win, text=f'Accuracy: {self.move["accuracy"]}', font=('Arial', 15))
        lblacc.pack()

        lblpower = tkinter.Label(self.win, text=f'Power: {self.move["power"]}', font=('Arial', 15))
        lblpower.pack()

        lblpp = tkinter.Label(self.win, text=f'PP: {self.move["pp"]}', font=('Arial', 15))
        lblpp.pack()

    def quit(self):
        self.win.destroy()

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

        self.movewin = None

    def next_image(self, lbl, lblname, lbltype1, lbltype2, event=None):
        nxt = self.url['id'] + 1
        new_url = f'data/images/{nxt:03d}.png'
        if nxt <= len(os.listdir('data/images')):
            lbl.image = tkinter.PhotoImage(file=new_url)
            lbl.config(image=lbl.image)
            self.url['url'] = new_url
            self.url['id'] += 1
            lblname.config(text = f'{self.pokemon[self.url["id"] - 1]["name"]["english"]}: {self.url["id"]}')
            self.__change_types(lbltype1, lbltype2)
        
    def prev_image(self, lbl, lblname, lbltype1, lbltype2, event=None):
        prev = self.url['id'] - 1
        new_url = f'data/images/{prev:03d}.png'
        if prev >= 1:
            lbl.image = tkinter.PhotoImage(file=new_url)
            lbl.config(image=lbl.image)
            self.url['url'] = new_url
            self.url['id'] -= 1
            lblname.config(text = f'{self.pokemon[self.url["id"] - 1]["name"]["english"]}: {self.url["id"]}')
            self.__change_types(lbltype1, lbltype2)

    def search_pokemon(self, lbl, lblname, search, lbltype1, lbltype2, event=None):
        text = search.get().capitalize()
        if text == '':
            return
        is_number = False
        try:
            pkid = int(text)
            if not 1 <= pkid <= len(self.pokemon):
                return
            types = self.get_type()
            type_base = 'data/types_images/'
            new_url = f'data/images/{pkid:03d}.png'
            lbl.image = tkinter.PhotoImage(file=new_url)
            lbl.config(image=lbl.image)
            self.url['url'] = new_url
            self.url['id'] = pkid
        except ValueError:
            for i in self.pokemon:
                if text in i['name'].values():
                    new_url = f'data/images/{i["id"]:03d}.png'
                    lbl.image = tkinter.PhotoImage(file=new_url)
                    lbl.config(image=lbl.image)
                    self.url['url'] = new_url
                    self.url['id'] = i['id']
                    break
        lblname.config(text = f'{self.pokemon[self.url["id"] - 1]["name"]["english"]}: {self.url["id"]}')
        self.__change_types(lbltype1, lbltype2)
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
            listbox.insert(tkinter.END, f'==={i.upper()}===')
            for j in moves[i]:
                listbox.insert(tkinter.END, j)

    def list_machine_moves(self, listbox):
        listbox.delete('0', 'end')
        moves = self.get_machine_moves()
        if not moves:
            return
        for i in list(moves.keys())[::-1]:
            listbox.insert(tkinter.END, f'==={i.upper()}===')
            for j in moves[i]:
                listbox.insert(tkinter.END, j.capitalize())

    def list_tutor_moves(self, listbox):
        listbox.delete('0', 'end')
        moves = self.get_tutor_moves()
        if not moves:
            return
        for i in list(moves.keys())[::-1]:
            listbox.insert(tkinter.END, f'==={i.upper()}===')
            for j in moves[i]:
                listbox.insert(tkinter.END, j.capitalize())

    def get_type(self, pid=None):
        if not pid:
            return [x.lower() for x in self.pokemon[self.url['id'] - 1]['type']]
        else:
            return [x.lower() for x in self.pokemon[pid - 1]['type']]

    def get_machine_moves(self, pid=None):
        if not pid:
            with open(f'data/machine_moves/{self.url["id"]:03d}.json', 'r') as fread:
                moves =json.load(fread)
        else:
            with open(f'data/machine_moves/{pid:03d}.json', 'r') as fread:
                moves =json.load(fread)
        return moves

    def get_tutor_moves(self, pid=None):
        if not pid:
            with open(f'data/tutor_moves/{self.url["id"]:03d}.json', 'r') as fread:
                moves =json.load(fread)
        else:
            with open(f'data/tutor_moves/{pid:03d}.json', 'r') as fread:
                moves =json.load(fread)
        return moves
    
    def get_move_info(self, listbox, event=None):
        move = listbox.curselection()
        if move == ():
            return
        mvstring = listbox.get(move[0])
        if '===' in mvstring:
            return
        if self.movewin:
            try:
                self.movewin.quit()
            except:
                self.movewin = None
        mvstring = mvstring.split(' ')[0]
        self.movewin = Win(mvstring)
        self.movewin.win.mainloop()


    def __change_types(self, lbltype1, lbltype2):
        types = self.get_type()
        type_base = 'data/types_images/'
        lbltype1.image = tkinter.PhotoImage(file=type_base + f'{types[0]}.png')
        if len(types) == 2:
            lbltype2.image = tkinter.PhotoImage(file=type_base + f'{types[1]}.png')
        else:
            lbltype2.image = ''
        lbltype1.config(image=lbltype1.image)
        lbltype2.config(image=lbltype2.image)
