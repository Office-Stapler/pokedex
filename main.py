import tkinter
import pokedex
import pokeAPI


tk = pokedex.Pokedex()
tk.win.title('Pokedex')


img = tkinter.PhotoImage(file=tk.url['url'])
lblname = tkinter.Label(tk.topFrame, text=f'{tk.pokemon[tk.url["id"] - 1]["name"]["english"]}: 1', font=('Helvetica', 40))
lbl = tkinter.Label(tk.win, image=img)
listbox = tkinter.Listbox(tk.rightFrame, width=50, height=20, font=('Helvetica', 12))

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


btnnext = tkinter.Button(tk.bottomFrame, text='>', fg='darkblue', bg='white', command=lambda: [tk.next_image(lbl, lblname, lbltype1, lbltype2), tk.list_moves(listbox)])
btnprev = tkinter.Button(tk.bottomFrame, text='<', fg='darkblue', bg='white', command=lambda: [tk.prev_image(lbl, lblname, lbltype1, lbltype2), tk.list_moves(listbox)])
btnnext.grid(row=0, column=1, rowspan = 2)
btnprev.grid(row=0, column=0, rowspan = 2)


btnlevelup = tkinter.Button(tk.rightFrame, text='Level up Moves', command = lambda: tk.list_moves(listbox))

btnmachine = tkinter.Button(tk.rightFrame, text='Machine moves', command = lambda: tk.list_machine_moves(listbox))

btntutor = tkinter.Button(tk.rightFrame, text='Tutor Moves', command = lambda: tk.list_tutor_moves(listbox))

btnlevelup.grid(row=0,column=0)
btnmachine.grid(row=1,column=0)
btntutor.grid(row=2,column=0)

listbox.grid(row=3,column=0)
btnmoves = tkinter.Button(tk.rightFrame, text='About Move', command= lambda: tk.get_move_info(listbox))
btnmoves.grid(row=2,column=1)
tk.list_moves(listbox)

scrollbar = tkinter.Scrollbar(tk.rightFrame, orient='vertical')
scrollbar.config(command=listbox.yview)

tk.win.bind('<Right>', lambda e: [tk.next_image(lbl, lblname, lbltype1, lbltype2), tk.list_moves(listbox)])
tk.win.bind('<Left>', lambda e: [tk.prev_image(lbl, lblname, lbltype1, lbltype2), tk.list_moves(listbox)])
tk.win.bind('<Return>', lambda e: [tk.search_pokemon(lbl, lblname, search, lbltype1, lbltype2), tk.list_moves(listbox)])
listbox.bind('<Double-1>', lambda e: tk.get_move_info(listbox))

tk.win.mainloop()
