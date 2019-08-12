from tkinter import *
import sqlite3
window = Tk()
window.title("Matthew's Library")

def destroy():
    window.destroy()

def add():
    listbox.delete(0,END)
    insert(titleEntry.get(),authorEntry.get(),yearEntry.get(),isbnEntry.get())
    view()

# Database
def createTable():
    con = sqlite3.connect("library.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS library (title TEXT, author TEXT, year INTEGER, isbn INTEGER)")
    con.commit()
    con.close()
    
def insert(title,author,year,isbn):
    con = sqlite3.connect("library.db")
    cur = con.cursor()
    cur.execute("INSERT INTO library VALUES (?,?,?,?)", (title,author,year,isbn))
    con.commit()
    con.close()

def view():
    con = sqlite3.connect("library.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM library")
    rows = cur.fetchall()
    con.commit()
    con.close()
    listbox.delete(0,END)
    print(rows)
    for result in rows:
        listbox.insert(END, ("%s (%s) - %s" % (result[0],result[2],result[1])))

def onclick_event():
    if len(listbox.curselection()) > 0:
        return(listbox.get(listbox.curselection()))
    return ""

def delete():
    con = sqlite3.connect("library.db")
    cur = con.cursor()
    
    string = (onclick_event().split("("))[0] 
    print(string)
    cur.execute('DELETE FROM library WHERE title=?',(string.strip(),))
    
    con.commit()
    con.close()
    view()

def selectView():
    con = sqlite3.connect("library.db")
    cur = con.cursor()

    cur.execute('SELECT * FROM library WHERE title=?',(titleEntry.get(),))
    rows = cur.fetchall()

    con.commit()
    con.close()
    print(rows)
    listbox.delete(0,END)
    for row in rows:
        listbox.insert(END, ("%s (%s) - %s" % (row[0],row[2],row[1])))

def update():
    con = sqlite3.connect("library.db")
    cur = con.cursor()

    string = (onclick_event().split("("))[0]
    print(string)
    cur.execute("UPDATE library SET title=?,author=?,year=?,isbn=? WHERE title=?", (titleEntry.get(),authorEntry.get(),yearEntry.get(),isbnEntry.get(),string.strip()))

    con.commit()
    con.close()
    view()

#Top Entries for Title,Year,Author,ISBN
top = Frame(window)
Label(top,text="Title").grid(row=0,column=0)
titleEntry = Entry(top)
titleEntry.grid(row=0,column=1)

Label(top,text="Author").grid(row=0,column=2)
authorEntry = Entry(top)
authorEntry.grid(row=0,column=3)

Label(top,text="Year").grid(row=1,column=0)
yearEntry = Entry(top)
yearEntry.grid(row=1,column=1)

Label(top,text="ISBN").grid(row=1,column=2)
isbnEntry = Entry(top)
isbnEntry.grid(row=1,column=3)

top.grid(row=0,column=0)

# Buttons on the right column
buttonWindow = Frame(window)
Button(buttonWindow,text="View All",command=view).pack(fill=X)
Button(buttonWindow,text="Search Entry",command=selectView).pack(fill=X)
Button(buttonWindow,text="Add Entry",command=add).pack(fill=X)
Button(buttonWindow,text="Update Selected",command=update).pack(fill=X)
Button(buttonWindow,text="Delete Selected",command=delete).pack(fill=X)
Button(buttonWindow,text="Close",command=destroy).pack(fill=X)
buttonWindow.grid(row=2,column=3)

# Book list
frame = Frame(window)
scrollbar = Scrollbar(frame,orient = VERTICAL)
listbox = Listbox(frame,yscrollcommand = scrollbar.set,width=50, selectmode=SINGLE)
listbox.bind('<<ListboxSelect>>', lambda event: onclick_event())
scrollbar.config(command = listbox.yview)
scrollbar.pack(side = RIGHT)
listbox.pack(expand=1,side = LEFT)
frame.grid(row=2,column=0)

createTable()

window.mainloop()
