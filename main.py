import tkinter
from tkinter.ttk import Progressbar
import pokedex
import pokeAPI


tk = pokedex.Pokedex()
tk.win.title('Pokedex')


img = tkinter.PhotoImage(file=tk.url['url'])
lblname = tkinter.Label(tk.topFrame, text=f'{tk.pokemon[tk.url["id"] - 1]["name"]["english"]}: 1', font=('Helvetica', 40))
lbl = tkinter.Label(tk.win, image=img)
listbox = tkinter.Listbox(tk.rightFrame, width=50, height=20, font=('Helvetica', 12))
listbox1 = tkinter.Listbox(tk.rightFrame, width=20, height=10, font=('Helvetica', 14))

search = tkinter.Entry(tk.topFrame, width=50, borderwidth=5, font=('Aerial', 20))
search.pack()

type1 = tkinter.PhotoImage(file='data/types_images/grass.png')
type2 = tkinter.PhotoImage(file='data/types_images/poison.png')
lbltype1 = tkinter.Label(tk.win, image=type1)
lbltype2 = tkinter.Label(tk.win, image=type2)

btnseach = tkinter.Button(tk.topFrame, text='Search Pokemon', command=lambda: [tk.search_pokemon(lbl, lblname, search, lbltype1, lbltype2), tk.list_moves(listbox)])
btnseach.pack()


lblname.pack()


lbl.pack()

lbltype1.pack()
lbltype2.pack()

lblhp = tkinter.Label(text='HP: 45', font=('Helvetica', 15))
lblhp.pack()

statushp = Progressbar(tk.win, length=255)
statushp['value'] = (45 / 255) * 100
statushp.pack()

lblattack = tkinter.Label(text='Attack: 49', font=('Helvetica', 15))
lblattack.pack()

statusattack = Progressbar(tk.win, length=255)
statusattack['value'] = 49 / 255 * 100
statusattack.pack()

lbldef = tkinter.Label(text='Defense: 49', font=('Helvetica', 15))
lbldef.pack()

statusdef = Progressbar(tk.win, length=255)
statusdef['value'] = 49 / 255 * 100
statusdef.pack()

lblspatk = tkinter.Label(text='Special Atack: 65', font=('Helvetica', 15))
lblspatk.pack()

statusspatk = Progressbar(tk.win, length=255)
statusspatk['value'] = 65 / 255 * 100
statusspatk.pack()

lblspdef = tkinter.Label(text='Special Defense: 65', font=('Helvetica', 15))
lblspdef.pack()

statusspdef = Progressbar(tk.win, length=255)
statusspdef['value'] = 65 / 255 * 100
statusspdef.pack()

lblspd = tkinter.Label(text='Speed: 45', font=('Helvetica', 15))
lblspd.pack()

statusspd = Progressbar(tk.win, length=255)
statusspd['value'] = 45 / 255 * 100
statusspd.pack()

stats = [lblhp, statushp, lblattack, statusattack, lbldef, statusdef, lblspatk, statusspatk, lblspdef, statusspdef, lblspd, statusspd]

btnnext = tkinter.Button(tk.bottomFrame, text='>', fg='darkblue', bg='white', command=lambda: [tk.next_image(lbl, lblname, lbltype1, lbltype2), tk.list_moves(listbox), tk.label_stats(stats)])
btnprev = tkinter.Button(tk.bottomFrame, text='<', fg='darkblue', bg='white', command=lambda: [tk.prev_image(lbl, lblname, lbltype1, lbltype2), tk.list_moves(listbox), tk.label_stats(stats)])
btnnext.grid(row=0, column=1, rowspan = 2)
btnprev.grid(row=0, column=0, rowspan = 2)


btnlevelup = tkinter.Button(tk.rightFrame, text='Level up Moves', command = lambda: tk.list_moves(listbox))

btnmachine = tkinter.Button(tk.rightFrame, text='Machine moves', command = lambda: tk.list_machine_moves(listbox))

btntutor = tkinter.Button(tk.rightFrame, text='Tutor Moves', command = lambda: tk.list_tutor_moves(listbox))

btnlevelup.grid(row=0,column=0)
btnmachine.grid(row=1,column=0)
btntutor.grid(row=2,column=0)

listbox.grid(row=3,column=0)
listbox1.grid(row=5,column=0)
scrollbar1 = tkinter.Scrollbar(tk.rightFrame, orient='vertical')
scrollbar1.config(command=listbox1.yview)

tk.list_abilities(listbox1)

tk.list_moves(listbox)

scrollbar = tkinter.Scrollbar(tk.rightFrame, orient='vertical')
scrollbar.config(command=listbox.yview)

tk.win.bind('<Right>', lambda e: [tk.next_image(lbl, lblname, lbltype1, lbltype2), tk.list_moves(listbox), tk.label_stats(stats), tk.list_abilities(listbox1)])
tk.win.bind('<Left>', lambda e: [tk.prev_image(lbl, lblname, lbltype1, lbltype2), tk.list_moves(listbox), tk.label_stats(stats), tk.list_abilities(listbox1)])
tk.win.bind('<Return>', lambda e: [tk.search_pokemon(lbl, lblname, search, lbltype1, lbltype2), tk.list_moves(listbox), tk.label_stats(stats), tk.list_abilities(listbox1)])
listbox.bind('<Double-1>', lambda e: tk.get_move_info(listbox))
listbox1.bind('<Double-1>', lambda e: tk.get_abl_info(listbox1))

tk.win.mainloop()
