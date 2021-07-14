from tkinter import ttk
from tkinter import *
import pyodbc

cnct = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=FlyDAAA;UID=sa;PWD=reallyStrongPwd123')
cursor = cnct.cursor()

window = Tk()
window.title('FlyDAAA')
window.geometry('1280x650+80+50')

framePack = Frame(window)
framePack.pack(side='top')

tree = ttk.Treeview(framePack, selectmode='browse', height=25)
tree.pack(pady=10)

frameGrid = Frame(window)
frameGrid.pack()

labels = [
    'ID:',
    'First name:',
    'Last name:',
    'DOB:',
    'Email:',
    'Phone:',
    'Possition:',
    'Exp:',
    'Contract term:',
    'Work schedule:',
    'Check up:',
    'Salary:',
    'Airline ID:']

Columns = [
    'Employees_ID',
    'First_Name',
    'Last_Name',
    'DOB',
    'Email',
    'Telephone_Number',
    'Possition',
    'Experience',
    'Contract_Term',
    'Work_Schedule',
    'CheckUp',
    'Salary',
    'Airline_ID']

entries = []

for i in range(13):
    label = Label(frameGrid,text=labels[i])
    label.grid(row=0, column=i)
    if i == 0:
        entry = Entry(frameGrid, width=2)
        entry.grid(row=1, column=i)
        entries.append(entry)
    else:
        entry = Entry(frameGrid, width=10)
        entry.grid(row=1, column=i)
        entries.append(entry)

def refresh():
    print("Refresh")
    cursor.execute("select * from Employees")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", text=str(row.Employees_ID), values=(row.First_Name, row.Last_Name, row.DOB, row.Email, row.Telephone_Number, row.Position, row.Experience,row.Contract_Term, row.Work_Schedule, row.CheckUp, row.Salary, row.Airline_ID))

def insert():
    print("Insert")
    cursor.execute(f"INSERT INTO Employees VALUES ('{entries[1].get()}', '{entries[2].get()}', '{entries[3].get()}', '{entries[4].get()}', '{entries[5].get()}', '{entries[6].get()}', '{entries[7].get()}', '{entries[8].get()}', '{entries[9].get()}', '{entries[10].get()}', '{int(entries[11].get())}', '{entries[12].get()}')")
    cnct.commit()
    refresh()

def update():
    print("Update")
    for i in range(1, 13):
        if len(entries[i].get()) > 0:
            cursor.execute(f"UPDATE Employees SET {Columns[i]}='{entries[i].get()}' WHERE Employees_ID={entries[0].get()}")
            cnct.commit()
    refresh()

def delete():
    print("Delete")
    cursor.execute(f"DELETE FROM Employees WHERE Employees_ID={entries[0].get()}")
    cnct.commit()
    refresh()

insert_btn = Button(frameGrid,text="Insert",width=10, pady=3, font="50", command=insert)
insert_btn.grid(row=2, column=10)
update_btn = Button(frameGrid,text="Update", width=10, pady=3, command=update)
update_btn.grid(row=2, column=11)
delete_btn = Button(frameGrid,text="Delete", width=10, pady=3, command=delete)
delete_btn.grid(row=2, column=12)

tree["columns"]=("cl1","cl2","cl3","cl4","cl5","cl6","cl7","cl8","cl9","cl10","cl11","cl12")

tree.column("#0", width=40)
for i in range(1,13):
    if i == 4:
        tree.column("cl" + str(i), width=150)
    elif i == 7:
        tree.column("cl" + str(i), width=50)
    elif i == 12:
        tree.column("cl" + str(i), width=70)
    else:
        tree.column("cl"+str(i), width=100)

tree.heading("#0", text="ID")
for i in range(1,13):
    tree.heading("cl"+str(i), text=""+str(labels[i]))

refresh()

window.mainloop()