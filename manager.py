from string import hexdigits
from tkinter import *
from tkinter import messagebox
from turtle import width
from db import Database

db = Database('store.db')

##########################
# functions


def populate():
    name_list.delete(0, END)
    for row in db.fetch():
        name_list.insert(END, row)


def add_item():
    if name_text.get() == '' or customer_text.get() == '' or retail_text.get() == '' or price_text.get() == '':
        messagebox.showerror('Require Fields', 'Please include all fields')
        return

    db.insert(name_text.get(), customer_text.get(),
              retail_text.get(), price_text.get())
    name_list.delete(0, END)
    name_list.insert(END, (name_text.get(), customer_text.get(),
                     retail_text.get(), price_text.get()))

    clear_text()
    populate()


def select_item(event):
    try:
        global selected_item
        index = name_list.curselection()[0]
        selected_item = name_list.get(index)

        name_entry.delete(0, END)
        name_entry.insert(END, selected_item[1])
        customer_entry.delete(0, END)
        customer_entry.insert(END, selected_item[2])
        retail_entry.delete(0, END)
        retail_entry.insert(END, selected_item[3])
        price_entry.delete(0, END)
        price_entry.insert(END, selected_item[4])
    except IndexError:
        pass


def remove_item():
    db.remove(selected_item[0])
    clear_text()
    populate()


def update_item():
    db.update(selected_item[0], name_text.get(), customer_text.get(),
              retail_text.get(), price_text.get())
    populate()


def clear_text():
    name_entry.delete(0, END)
    customer_entry.delete(0, END)
    retail_entry.delete(0, END)
    price_entry.delete(0, END)


# create window
app = Tk()
app.title("Manager")
app.geometry("750x350")
##########################


##########################
# name
name_label = Label(app, text='Name', font=('bold', 14), padx=10, pady=20)
name_label.grid(row=0, column=0, sticky=W)

name_text = StringVar()
name_entry = Entry(app, textvariable=name_text)
name_entry.grid(row=0, column=1)

# customer
customer_label = Label(app, text='Customer', font=('bold', 14))
customer_label.grid(row=0, column=2)

customer_text = StringVar()
customer_entry = Entry(app, textvariable=customer_text)
customer_entry.grid(row=0, column=3)

# retail
retail_label = Label(app, text='Retail', font=('bold', 14), padx=10)
retail_label.grid(row=1, column=0, sticky=W)

retail_text = StringVar()
retail_entry = Entry(app, textvariable=retail_text)
retail_entry.grid(row=1, column=1)

# price
price_label = Label(app, text='Price', font=('bold', 14))
price_label.grid(row=1, column=2)

price_text = StringVar()
price_entry = Entry(app, textvariable=price_text)
price_entry.grid(row=1, column=3)
##########################


##########################
# listbox
name_list = Listbox(app, height=8, width=50, border=0)
name_list.grid(row=3, column=0, rowspan=6, columnspan=3, pady=20, padx=20)
# scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)
# set scrollbar to listbox
name_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=name_list.yview)
# bind select
name_list.bind('<<ListboxSelect>>', select_item)
##########################


##########################
# buttons
add_btn = Button(app, text='Add', width=12, command=add_item)
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app, text='Remove', width=12, command=remove_item)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text='Update', width=12, command=update_item)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text='Clear Input', width=12, command=clear_text)
clear_btn.grid(row=2, column=3)
##########################
# populate data
populate()

# running
app.mainloop()
