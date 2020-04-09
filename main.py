import tkinter
import pokedex
import pokeAPI


tk = pokedex.Pokedex()

img = tkinter.PhotoImage(file=tk.url['url'])
lblname = tkinter.Label(tk.topFrame, text=tk.pokemon[tk.url['id'] - 1]['name']['english'])
lbl = tkinter.Label(tk.win, image=img)
listbox = tkinter.Listbox(tk.rightFrame, width=50, height=50, font=('Helvetica', 12))

search = tkinter.Entry(tk.topFrame, width=50, borderwidth=5, font=('Aerial', 20))
search.pack()

btnseach = tkinter.Button(tk.topFrame, text='Search Pokemon', command=lambda: [tk.search_pokemon(lbl, lblname, search), tk.list_moves(listbox)])
btnseach.pack()


lblname.pack()


lbl.pack()
btnnext = tkinter.Button(tk.bottomFrame, text='>', fg='darkblue', bg='white', command=lambda: [tk.next_image(lbl, lblname), tk.list_moves(listbox)])
btnprev = tkinter.Button(tk.bottomFrame, text='<', fg='darkblue', bg='white', command=lambda: [tk.prev_image(lbl, lblname), tk.list_moves(listbox)])
btnnext.grid(row=0, column=1, rowspan = 2)
btnprev.grid(row=0, column=0, rowspan = 2)


listbox.pack()

tk.list_moves(listbox)

scrollbar = tkinter.Scrollbar(tk.rightFrame, orient='vertical')
scrollbar.config(command=listbox.yview)
scrollbar.pack(side='right', fill='y')

tk.win.bind('<Right>', lambda e: [tk.next_image(lbl, lblname), tk.list_moves(listbox)])
tk.win.bind('<Left>', lambda e: [tk.prev_image(lbl, lblname), tk.list_moves(listbox)])
tk.win.bind('<Return>', lambda e: [tk.search_pokemon(lbl, lblname, search), tk.list_moves(listbox)])

tk.win.mainloop()
