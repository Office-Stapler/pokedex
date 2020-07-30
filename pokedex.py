import tkinter
import os
import json

class Win:
    def __init__(self, name):
        self.win = tkinter.Tk()
        self.win.title(name.replace('-',' '))
        self.win.geometry('300x300')

    def display_move(self, name):
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

    def display_ability(self, name, pid):
        with open(f'data/abilities/{pid:03d}.json') as fread:
            abl = json.load(fread)
        self.win.geometry('200x200')
        for i in abl:
            if i['name'] == name.lower():
                self.abl = i
                break

        lblname = tkinter.Label(self.win, text=f'About {name.replace("-"," ")}', font=('Arial', 15))
        lblname.pack()
        lbleffect = tkinter.Label(self.win, text=f'{self.abl["effect_entries"][0]["short_effect"]}', font=('Arial', 13), wraplengt=100)
        lbleffect.pack()

    def quit(self):
        self.win.destroy()

class Pokedex:
    ''' A Pokedex class gathers useful data about pokemon '''
    def __init__(self):
        with open('data/pokedex.json', 'r+', encoding='utf-8') as f:
            self.pokemon = json.loads(f.read())
        self.curr = {'name': 'Bulbasaur', 'id': 1}
    
    def next_pokemon(self):
        ''' Makes the next pokemon, the current pokemon'''
        pid = self.curr['id'] + 1
        if pid <= len(self.pokemon):
            self.curr = {'name': self.pokemon[pid - 1]['name']['english'], 'id': pid}

    def prev_pokemon(self):
        ''' Makes the previous pokemon, the current pokemon'''
        pid = self.curr['id'] - 1
        if pid >= 1:
           self.curr = {'name': self.pokemon[pid - 1]['name']['english'], 'id': pid}

    def search_pokemon(self, query: str):
        ''' searches for a pokemon with name or id "query" and it the current pokemon '''
        text = query.capitalize()
        try:
            text = int(text)
        except ValueError:
            for i in self.pokemon:
                if text in i['name'].values():
                    self.curr['name'] = i['name']['english'] 
                    self.curr['id'] = i['id']
                    return
        if 1 <= text <= len(self.pokemon):
            self.curr['name'] = self.pokemon[text - 1]['name']['english']
            self.curr['id'] = text

    def get_levelup_moves(self, pid = None):
        ''' get a list of moves learnt by levelup of the current pokemon or of pokemon with id 'pid' '''
        if not pid:
            with open(f'data/levelup_moves/{self.curr["id"]:03d}.json', 'r') as fread:
                moves =  json.load(fread)
        else:
            with open(f'data/levelup_moves/{pid:03d}.json', 'r') as fread:
                moves =  json.load(fread)
        
        return moves

    def get_type(self, pid=None):
        ''' get the typing of the current pokemon or of pokemon with id 'pid' '''
        if not pid:
            return [x.lower() for x in self.pokemon[self.curr['id'] - 1]['type']]
        else:
            return [x.lower() for x in self.pokemon[pid - 1]['type']]

    def get_machine_moves(self, pid=None):
        ''' get a list of moves learnt by machine of the current pokemon or of pokemon with id 'pid' '''
        if not pid:
            with open(f'data/machine_moves/{self.curr["id"]:03d}.json', 'r') as fread:
                moves =json.load(fread)
        else:
            with open(f'data/machine_moves/{pid:03d}.json', 'r') as fread:
                moves =json.load(fread)
        return moves

    def get_tutor_moves(self, pid=None):
        ''' get a list of moves learnt by tutors of the current pokemon or of pokemon with id 'pid' '''
        if not pid:
            with open(f'data/tutor_moves/{self.curr["id"]:03d}.json', 'r') as fread:
                moves =json.load(fread)
        else:
            with open(f'data/tutor_moves/{pid:03d}.json', 'r') as fread:
                moves =json.load(fread)
        return moves
    
    def get_move_info(self, name: str):
        ''' get more details of a specific move '''
        with open('data/moves.json') as fread:
            moves = json.load(fread)

        for i in moves:
            if i['ename'].lower() == name.replace('-', ' ').lower():
                return i

    def get_abilities(self, pid=None):
        ''' get a list of abilities for the current pokemon or of pokemon with id 'pid' '''
        if not pid:
            with open(f'data/abilities/{self.curr["id"]:03d}.json', 'r') as fread:
                abl =json.load(fread)
        else:
            with open(f'data/abilities/{pid:03d}.json', 'r') as fread:
                abl =json.load(fread)
        return abl



    @property
    def curr_stats(self):
        ''' get the stats of the current pokemon '''
        return self.pokemon[self.curr['id'] - 1]['base']
        

class pokeGUI:
    ''' A gui class that is to be displayed '''
    def __init__(self):
        self.pokedex = Pokedex()

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
        self.ablwin = None
    
    def label_stats(self, stats):
        ''' updates the stats of a list of progressbars '''
        base = self.pokedex.curr_stats
        stats[0].config(text = f'HP: {base["HP"]}')
        stats[1]['value'] = base['HP'] / 255 * 100
        stats[2].config(text = f'Attack: {base["Attack"]}')
        stats[3]['value'] = base['Attack'] / 255 * 100
        stats[4].config(text = f'Defense: {base["Defense"]}')
        stats[5]['value'] = base['Defense'] / 255 * 100
        stats[6].config(text = f'Sp. Attack: {base["Sp. Attack"]}')
        stats[7]['value'] = base['Sp. Attack'] / 255 * 100
        stats[8].config(text = f'Sp. Defense: {base["Sp. Defense"]}')
        stats[9]['value'] = base['Sp. Defense'] / 255 * 100
        stats[10].config(text = f'Speed: {base["Speed"]}')
        stats[11]['value'] = base['Speed'] / 255 * 100

    def command_next(self, lblimg, lblname, lbltype1, lbltype2, event=None):
        ''' tells the GUI to show the next pokemon '''
        self.pokedex.next_pokemon()
        new_url = f'data/images/{self.pokedex.curr["id"]:03d}.png'
        lblimg.image = tkinter.PhotoImage(file=new_url)
        lblimg.config(image=lblimg.image)
        lblname.config(text = f'{self.pokedex.curr["name"]}: {self.pokedex.curr["id"]}')

        types = self.pokedex.get_type()
        type_base = 'data/types_images/'
        lbltype1.image = tkinter.PhotoImage(file=type_base + f'{types[0]}.png')
        if len(types) == 2:
            lbltype2.image = tkinter.PhotoImage(file=type_base + f'{types[1]}.png')
        else:
            lbltype2.image = ''
        lbltype1.config(image=lbltype1.image)
        lbltype2.config(image=lbltype2.image)

    def command_prev(self, lblimg, lblname, lbltype1, lbltype2, event=None):
        ''' tells the GUI to show the previous pokemon '''
        self.pokedex.prev_pokemon()
        new_url = f'data/images/{self.pokedex.curr["id"]:03d}.png'
        lblimg.image = tkinter.PhotoImage(file=new_url)
        lblimg.config(image=lblimg.image)
        lblname.config(text = f'{self.pokedex.curr["name"]}: {self.pokedex.curr["id"]}')

        types = self.pokedex.get_type()
        type_base = 'data/types_images/'
        lbltype1.image = tkinter.PhotoImage(file=type_base + f'{types[0]}.png')
        if len(types) == 2:
            lbltype2.image = tkinter.PhotoImage(file=type_base + f'{types[1]}.png')
        else:
            lbltype2.image = ''
        lbltype1.config(image=lbltype1.image)
        lbltype2.config(image=lbltype2.image)
    
    def command_search(self, lblimg, lblname, search, lbltype1, lbltype2, event=None):
        ''' tells the GUI to show a searched pokemon '''
        self.pokedex.search_pokemon(search.get())
        pkid = self.pokedex.curr['id']
        types = self.pokedex.get_type()
        type_base = 'data/types_images/'
        new_url = f'data/images/{pkid:03d}.png'
        lblimg.image = tkinter.PhotoImage(file=new_url)
        lblimg.config(image=lblimg.image)
        lblname.config(text = f'{self.pokedex.curr["name"]}: {pkid}')

        types = self.pokedex.get_type()
        type_base = 'data/types_images/'
        lbltype1.image = tkinter.PhotoImage(file=type_base + f'{types[0]}.png')
        if len(types) == 2:
            lbltype2.image = tkinter.PhotoImage(file=type_base + f'{types[1]}.png')
        else:
            lbltype2.image = ''
        lbltype1.config(image=lbltype1.image)
        lbltype2.config(image=lbltype2.image)

        search.delete(0, tkinter.END)
        search.insert(0, '')

    def list_abilities(self, listbox, event=None):
        ''' lists the pokemon's ability to the given listbox '''
        listbox.delete('0', 'end')
        abl = self.pokedex.get_abilities()
        if not abl:
            return
        listbox.insert(tkinter.END, '==Abilities==')
        for i in abl:
            listbox.insert(tkinter.END, i['name'].capitalize())

    def get_abl_info(self, listbox, event=None):
        ''' opens a new window to show more information about the selected ability '''
        abl = listbox.curselection()
        if abl == ():
            return
        abstring = listbox.get(abl[0])
        if '==' in abstring:
            return
        
        if self.ablwin:
            try:
                self.ablwin.quit()
            except:
                self.ablin = None
        abstring = abstring.split(' ')[0]
        self.ablwin = Win(abstring)
        self.ablwin.display_ability(abstring, self.pokedex.curr['id'])
        self.ablwin.win.mainloop()

    def list_levelup_moves(self, listbox):
        ''' lists the pokemon's levelup moves for a selected listbox '''
        listbox.delete('0', 'end')
        moves = self.pokedex.get_levelup_moves()
        if not moves:
            return

        for i in list(moves.keys())[::-1]:
            listbox.insert(tkinter.END, f'==={i.upper()}===')
            for j in moves[i]:
                listbox.insert(tkinter.END, f'{j[0]} -> {j[1]}')

    def list_machine_moves(self, listbox):
        ''' lists the pokemon's machine moves for a selected listbox '''
        listbox.delete('0', 'end')
        moves = self.pokedex.get_machine_moves()
        if not moves:
            return
        for i in list(moves.keys())[::-1]:
            listbox.insert(tkinter.END, f'==={i.upper()}===')
            for j in moves[i]:
                listbox.insert(tkinter.END, j.capitalize())

    def list_tutor_moves(self, listbox):
        ''' lists the pokemon's tutor moves for a selected listbox '''
        listbox.delete('0', 'end')
        moves = self.pokedex.get_tutor_moves()
        if not moves:
            return
        for i in list(moves.keys())[::-1]:
            listbox.insert(tkinter.END, f'==={i.upper()}===')
            for j in moves[i]:
                listbox.insert(tkinter.END, j.capitalize())

    def get_move_info(self, listbox, event=None):
        ''' opens up a new window to show more info about the selected move '''
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
        self.movewin.display_move(mvstring)
        self.movewin.win.mainloop()

