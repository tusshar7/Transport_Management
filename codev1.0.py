import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox
mydb = mysql.connector.connect(
  host="localhost",
  user="",
  password=""
)
mycursor = mydb.cursor()
try:
    mycursor.execute("CREATE DATABASE transport")
except:
    pass
try:
    mycursor.execute("use transport")
    mycursor.execute("CREATE TABLE Trucks(truck_no varchar(20), PRIMARY KEY(truck_no))")
except:
    pass
try:   
    mycursor.execute("CREATE TABLE Party(party varchar(50), PRIMARY KEY(party))")
except:
    pass
try:
    mycursor.execute("CREATE TABLE Expenditure_Types(expend_name varchar(50), PRIMARY KEY(expend_name))")
except:
    pass
try:
    mycursor.execute("CREATE TABLE Trips(uid varchar(25),truck_no varchar(20),trip_date date,totalamt float(30), advamt float(30),balaamt float(30),party_name varchar(50),completed int(1),totalexp float(50),account_no varchar(50), PRIMARY KEY(uid))")
except:
    pass
try:
    mycursor.execute("CREATE TABLE Expenditure(uid varchar(25),expend_name varchar(50),expend_amt float(30))")
except:
    pass
try:
    mycursor.execute("CREATE TABLE accounts(account_no varchar(50), PRIMARY KEY(account_no))")
except:
    pass
root = tk.Tk()
root.title("T")
s = ttk.Style()
s.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [5, 5],
                                        "font" : ('URW Gothic L', '10', 'bold')},}})
s.theme_use("MyStyle")
h = root.winfo_screenheight()
w = root.winfo_screenwidth()
canvas=tk.Canvas(root,width=w-100,height=h-200)
frame=tk.Frame(canvas)
def frame_configure(event):
    global canvas
    canvas.configure(scrollregion=canvas.bbox("all"))
frame.bind("<Configure>",frame_configure)
vsb=tk.Scrollbar(root,orient="vertical",command=canvas.yview)
vsb.grid(row=0,column=1,sticky="nsew")
hsb=tk.Scrollbar(root,orient="horizontal",command=canvas.xview)
hsb.grid(row=1,column=0,sticky="nsew")
canvas.configure(yscrollcommand=vsb.set)
canvas.configure(xscrollcommand=hsb.set)
canvas.grid(row=0,column=0,sticky="nsew")
canvas.create_window((3,2),window=frame,anchor="nw",tags="frame")

tabControl = ttk.Notebook(frame)
trucklist=['--Select From the list--']
expendlist=['--Select From the list--']
partylist=["--Select From the list--"]
cUID=["--Select From the list--"]
pUID=["--Select From the list--"]
UID=["--Select From the list--"]
Acct=["--Select From the list--"]
truckno=tk.StringVar()
totalamt=tk.DoubleVar()
advamt=tk.DoubleVar()
partyname=tk.StringVar()
accountno=tk.StringVar()
selectedAcct=tk.StringVar()
balamt=tk.DoubleVar()
selectedParty=tk.StringVar()
selectedTruck = tk.StringVar()
selectedUID = tk.StringVar()
selectedExpendRemove=tk.StringVar()
newexpend=tk.StringVar()
selectedExpend={}
expend={}
expendcnt=0
def make_ds(myresult,ds):
    ds.clear()
    ds.append("--Select From the list--")
    for x in myresult:
        for i in range(0,len(x)):
            ds.append(x[i])
def on_select(event):
    selected=event.widget.select()
    tab_text=event.widget.tab(selected,"text")
    selectedTruck.set("--Select From the list--")
    selectedParty.set("--Select From the list--")
    selectedUID.set("--Select From the list--")
    selectedExpendRemove.set("--Select From the list--")
    selectedAcct.set("--Select From the list--")
    newexpend.set("-Enter-")
    truckno.set("-Enter-")
    partyname.set("-Enter-")
    accountno.set("-Enter-")
    totalamt.set(0.0)
    advamt.set(0.0)
    balamt.set(0.0)
    expendcnt=0
    #Loading DataStructures:
    mycursor.execute("SELECT truck_no FROM trucks")
    myresult = mycursor.fetchall()
    make_ds(myresult,trucklist)
    mycursor.execute("SELECT party FROM Party")
    myresult = mycursor.fetchall()
    make_ds(myresult,partylist)
    mycursor.execute("SELECT expend_name FROM Expenditure_Types")
    myresult = mycursor.fetchall()
    make_ds(myresult,expendlist)
    mycursor.execute("SELECT uid FROM Trips")
    myresult = mycursor.fetchall()
    make_ds(myresult,UID)
    mycursor.execute("SELECT uid FROM Trips where completed='1'")
    myresult = mycursor.fetchall()
    make_ds(myresult,cUID)
    mycursor.execute("SELECT uid FROM Trips where completed='0'")
    myresult = mycursor.fetchall()
    make_ds(myresult,pUID)
    mycursor.execute("SELECT account_no from accounts")
    myresult = mycursor.fetchall()
    make_ds(myresult,Acct)
    if (tab_text=='Add Trip'):
        tk.OptionMenu(tab3,selectedTruck,*trucklist).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
        tk.OptionMenu(tab3,selectedParty,*partylist).grid(row=3, column=1,sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
        tk.OptionMenu(tab3,selectedAcct,*Acct).grid(row=4, column=1,sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
    elif (tab_text=='Remove Truck'):
        tk.OptionMenu(tab2,selectedTruck,*trucklist).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
    elif (tab_text=='Remove Trip'):
        tk.OptionMenu(tab5,selectedUID,*UID).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
    elif (tab_text=='Update Trip'):
        tk.OptionMenu(tab4,selectedUID,*UID).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
    elif (tab_text=='Remove Expenditure Types'):
        tk.OptionMenu(tab11,selectedExpendRemove,*expendlist).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
    elif (tab_text=='Remove Party'):
        tk.OptionMenu(tab13,selectedParty,*partylist).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
    elif (tab_text=='Completed Trips'):
        tk.OptionMenu(tab6,selectedUID,*cUID).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
    elif (tab_text=='Pending Trips'):
        tk.OptionMenu(tab7,selectedUID,*pUID).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
    elif (tab_text=='Remove Account'):
        tk.OptionMenu(tab15,selectedAcct,*Acct).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
def PendingTrips():
    global selectedUID
    ans=[]
    mycursor.execute("SELECT truck_no,trip_date,advamt,totalamt,balaamt,party_name,totalexp,account_no FROM Trips where uid='"+str(selectedUID.get())+"'")
    myresult = mycursor.fetchall()
    make_ds(myresult,ans)
    tk.Label(tab7,text="Truck No : "+str(ans[1]),font=("Arial",11)).grid(row=3, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab7,text="Trip Date : "+str(ans[2]),font=("Arial",11)).grid(row=4, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab7,text="Party Name : "+str(ans[6]),font=("Arial",11)).grid(row=5, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab7,text="Your Account No : "+str(ans[8]),font=("Arial",11)).grid(row=6, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab7,text="Total Amount : "+str(ans[4]),font=("Arial",11)).grid(row=7, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab7,text="Advance Amount Paid : "+str(ans[3]),font=("Arial",11)).grid(row=8, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab7,text="Balance Amount Paid : Not Paid",font=("Arial",11)).grid(row=9, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab7,text="Profit Made : Payment Pending....Cannot calculate!!",font=("Arial",11)).grid(row=10, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab7,text="Total Expenditure : "+str(ans[7]),font=("Arial",11)).grid(row=11, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
def CompletedTrips():
    global selectedUID
    ans=[]
    mycursor.execute("SELECT truck_no,trip_date,advamt,totalamt,balaamt,party_name,totalexp,account_no FROM Trips where uid='"+str(selectedUID.get())+"'")
    myresult = mycursor.fetchall()
    make_ds(myresult,ans)
    tk.Label(tab6,text="Truck No : "+str(ans[1]),font=("Arial",11)).grid(row=3, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab6,text="Trip Date : "+str(ans[2]),font=("Arial",11)).grid(row=4, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab6,text="Party Name : "+str(ans[6]),font=("Arial",11)).grid(row=5, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab6,text="Your Account No : "+str(ans[8]),font=("Arial",11)).grid(row=6, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab6,text="Total Amount : "+str(ans[4]),font=("Arial",11)).grid(row=7, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab6,text="Advance Amount Paid : "+str(ans[3]),font=("Arial",11)).grid(row=8, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab6,text="Balance Amount Paid : "+str(ans[5]),font=("Arial",11)).grid(row=9, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab6,text="Profit Made : "+str(ans[4]-ans[7]),font=("Arial",11)).grid(row=10, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab6,text="Total Expenditure : "+str(ans[7]),font=("Arial",11)).grid(row=11, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Label(tab6,text="Breakup of Expenditure : ",font=("Arial",11)).grid(row=12, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    mycursor.execute("SELECT expend_name,expend_amt FROM expenditure where uid='"+str(selectedUID.get())+"'")
    myresult = mycursor.fetchall()
    make_ds(myresult,ans)
    i=1
    while(i<len(ans)-1):
        tk.Label(tab6,text=str(ans[i])+": "+str(ans[i+1]),font=("Arial",11)).grid(row=12+i, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
        i=i+2
def UpdateUID():
    if(selectedUID.get()=="--Select From the list--"):
        messagebox.showerror("showerror", "Select valid UID!!")
        return
    ans=[]
    mycursor.execute("SELECT advamt,totalamt,completed FROM Trips where uid='"+str(selectedUID.get())+"'")
    myresult = mycursor.fetchall()
    make_ds(myresult,ans)
    if(ans[1]+balamt.get()!=ans[2]):
        messagebox.showerror("showerror", "Total amount is not equal to balance + advance!!")
        return
    if(ans[3]==1):
        messagebox.showerror("showerror", "UID Already updated!!")
        return
    sql="UPDATE trips SET balaamt='"+str(balamt.get())+"' , completed='1' WHERE uid='"+str(selectedUID.get())+"'"
    mycursor.execute(sql)
    mydb.commit()
    messagebox.showinfo("showinfo", "Update Successfull!!")
def AddAccount():
    global accountno
    try:
        if (accountno.get() in Acct):
            messagebox.showerror("showerror", "Account already present in database!!")
        else:
            sql="INSERT INTO accounts (account_no) VALUES (%s)"
            val=(accountno.get(),)
            mycursor.execute(sql,val)
            mydb.commit()
            messagebox.showinfo("showinfo", "Added Successfully!!")
    except:
        messagebox.showerror("showerror", "Something went wrong!!")
def RemoveAccount():
    global selectedAcct
    if(selectedAcct.get()=="--Select From the list--"):
        messagebox.showerror("showerror", "Accout not present in database!!")
        return
    try:
        sql="DELETE FROM accounts WHERE account_no='"+str(selectedAcct.get())+"'"
        mycursor.execute(sql)
        mydb.commit()
        messagebox.showinfo("showinfo", "Removed Successfully!!")
    except:
        messagebox.showerror("showerror", "Account not present in database!!")
def AddTruck():
    global truckno
    try:
        if (truckno.get() in trucklist):
            messagebox.showerror("showerror", "TruckNo already present in database!!")
        else:
            sql="INSERT INTO trucks (truck_no) VALUES (%s)"
            val=(truckno.get(),)
            mycursor.execute(sql,val)
            mydb.commit()
            messagebox.showinfo("showinfo", "Added Successfully!!")
    except:
        messagebox.showerror("showerror", "Something went wrong!!")
def RemoveTruck():
    global selectedTruck
    if(selectedTruck.get()=="--Select From the list--"):
        messagebox.showerror("showerror", "TruckNo. not present in database!!")
        return
    try:
        #trucklist.remove(selectedTruck.get())
        sql="DELETE FROM trucks WHERE truck_no='"+str(selectedTruck.get())+"'"
        mycursor.execute(sql)
        mydb.commit()
        messagebox.showinfo("showinfo", "Removed Successfully!!")
    except:
        messagebox.showerror("showerror", "TruckNo. not present in database!!")
def AddParty():
    global partyname
    try:
        if (partyname.get() in partylist):
            messagebox.showerror("showerror", "Party name already present in database!!")
        else:
            sql="INSERT INTO Party (party) VALUES (%s)"
            val=(partyname.get(),)
            mycursor.execute(sql,val)
            mydb.commit()
            messagebox.showinfo("showinfo", "Added Successfully!!")
    except:
        messagebox.showerror("showerror", "Something went wrong!!")
def RemoveParty():
    global selectedParty
    if(selectedParty.get()=="--Select From the list--"):
        messagebox.showerror("showerror", "Party name not present in database!!")
        return
    try:
        sql="DELETE FROM Party WHERE party='"+str(selectedParty.get())+"'"
        mycursor.execute(sql)
        mydb.commit()
        messagebox.showinfo("showinfo", "Removed Successfully!!")
    except:
        messagebox.showerror("showerror", "Party name not present in database!!")
def RemoveTrip():
    global selectedUID
    if(selectedUID.get()=="--Select From the list--"):
        messagebox.showerror("showerror", "UID not present in database!!")
        return
    try:
        sql="DELETE FROM trips WHERE uid='"+str(selectedUID.get())+"'"
        mycursor.execute(sql)
        sql="DELETE FROM expenditure WHERE uid='"+str(selectedUID.get())+"'"
        mycursor.execute(sql)
        mydb.commit()
        messagebox.showinfo("showinfo", "Removed Successfully!!")
    except:
        messagebox.showerror("showerror", "UID not present in database!!")
def RemoveExpend():
    global selectedExpendRemove
    if(selectedExpendRemove.get()=="--Select From the list--"):
        messagebox.showerror("showerror", "Expendtiture not present in database!!")
        return
    try:
        sql="DELETE FROM Expenditure_types WHERE expend_name='"+str(selectedExpendRemove.get())+"'"
        mycursor.execute(sql)
        mydb.commit()
        messagebox.showinfo("showinfo", "Removed Successfully!!")
    except:
        messagebox.showerror("showerror", "Expendtiture not present in database!!")
def AddTrip():
    flag=1
    total=0
    date=str(cal.selection_get())
    if(totalamt.get()==advamt.get()):
        complete=1
    else:
        complete=0
    uid=selectedTruck.get()
    uid=uid+date[0:4]
    uid=uid+date[5:7]
    uid=uid+date[8:10]
    for x,y in selectedExpend.items():
        total=total+float(expend[x].get())
        if(y.get()=="--Select From the list--"):
            flag=0
            break
    if(selectedParty.get()!="--Select From the list--" and flag==1 and selectedTruck.get()!="--Select From the list--" and selectedAcct.get()!="--Select From the list--"):
        try:
            sql="INSERT INTO trips (uid, truck_no, trip_date, totalamt, advamt, balaamt,party_name,completed,totalexp,account_no ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val=(uid,selectedTruck.get(),date,totalamt.get(),advamt.get(),0,selectedParty.get(),complete,total,selectedAcct.get())
            mycursor.execute(sql,val)
            mydb.commit()   
            for x,y in selectedExpend.items():
                sql="INSERT INTO Expenditure (uid, expend_name, expend_amt) VALUES (%s,%s,%s)"
                val=(uid,y.get(),expend[x].get())
                mycursor.execute(sql,val)
                mydb.commit()
            messagebox.showinfo("showinfo", "Trip added Successfully!!")
        except:
            messagebox.showerror("showerror","Trip already exists!!")
    else:
        messagebox.showerror("showerror", "Error!! Date, TruckNo, Party,AccoutNo., Expenditure are mandatory fields and cannot be null.")
def AddNewExpend():
    global newexpend
    try:
        if (newexpend.get() in expendlist):
            messagebox.showerror("showerror", "Expenditure type already present in database!!")
        else:
            sql="INSERT INTO Expenditure_Types (expend_name) VALUES (%s)"
            val=(newexpend.get(),)
            mycursor.execute(sql,val)
            mydb.commit()
            messagebox.showinfo("showinfo", "Added Successfully!!")
    except:
        messagebox.showerror("showerror", "Something went wrong!!")
def ShowUID():
    global selectedUID
    if (selectedUID.get() not in UID or selectedUID.get()=="--Select From the list--" ):
        messagebox.showerror("showerror", "Please select valid UID!!")
        return
    tk.Label(tab4,text="Balance Amount Paid:",font=("Arial",11)).grid(row=1, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    tk.Entry(tab4,textvariable=balamt).grid(row=1, column=1,sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
    tk.Button(tab4,text="Submit",command=UpdateUID,fg="black",bg="green").grid(row=2,column=0,padx=(10,0),pady=(10,0))
def AddExpend():
    global expendcnt
    expendcnt=expendcnt+1
    selectedExpend[expendcnt-1]=tk.StringVar()
    selectedExpend[expendcnt-1].set("--Select From the list--")
    tk.OptionMenu(tab3,selectedExpend[expendcnt-1],*expendlist).grid(row=6+expendcnt, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
    expend[expendcnt-1]=tk.StringVar()
    tk.Entry(tab3,textvariable=expend[expendcnt-1]).grid(row=6+expendcnt, column=1,sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
def DoneAdding():
    total=0
    try:
        for x,y in selectedExpend.items():
            total=total+float(expend[x].get())
        tk.Label(tab3,text="Total Expenditure:",font=("Arial",11)).grid(row=6+expendcnt+1, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
        tk.Label(tab3,text="Rs. "+str(total),font=("Arial",11)).grid(row=6+expendcnt+1, column=1,sticky=tk.W+tk.E+tk.N+tk.S)
        tk.Button(tab3,text="Submit",command=AddTrip,fg="black",bg="green").grid(row=6+expendcnt+1,column=2,sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
    except:
        messagebox.showerror("showerror", "Please enter valid amount in expenditure!!")
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)
tab6 = ttk.Frame(tabControl)
tab7 = ttk.Frame(tabControl)
tab8 = ttk.Frame(tabControl)
tab10 = ttk.Frame(tabControl)
tab11 = ttk.Frame(tabControl)
tab12 = ttk.Frame(tabControl)
tab13 = ttk.Frame(tabControl)
tab14 = ttk.Frame(tabControl)
tab15 = ttk.Frame(tabControl)

tabControl.bind("<<NotebookTabChanged>>",on_select)
tabControl.add(tab1, text ='Add Truck')
tabControl.add(tab2, text ='Remove Truck')
tabControl.add(tab3, text ='Add Trip')
tabControl.add(tab4, text ='Update Trip')
tabControl.add(tab5, text ='Remove Trip')
tabControl.add(tab6, text ='Completed Trips')
tabControl.add(tab7, text ='Pending Trips')
tabControl.add(tab10, text ='Add Expenditure Types')
tabControl.add(tab11, text ='Remove Expenditure Types')
tabControl.add(tab12, text ='Add Party')
tabControl.add(tab13, text ='Remove Party')
tabControl.add(tab14, text ='Add Account')
tabControl.add(tab15, text ='Remove Account')
tabControl.pack(expand = 1, fill ="both")


tk.Label(tab1,text="Enter Truck No. : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0))
tk.Entry(tab1,textvariable=truckno).grid(row=0, column=1, pady=(10,0))
tk.Button(tab1,text="Add",command=AddTruck,fg="black",bg="green").grid(row=1,column=0,padx=(10,0),pady=(10,0))


tk.Label(tab2,text="Select Truck No. : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0))
tk.OptionMenu(tab2,selectedTruck,*trucklist).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
tk.Button(tab2,text="Remove",command=RemoveTruck,fg="black",bg="green").grid(row=1,column=0,padx=(10,0),pady=(10,0))


tk.Label(tab3,text="Select Truck No : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.OptionMenu(tab3,selectedTruck,*trucklist).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
tk.Label(tab3,text="Total Amount: ",font=("Arial",11)).grid(row=1, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
tk.Entry(tab3,textvariable=totalamt).grid(row=1, column=1,sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
tk.Label(tab3,text="Advance Amount: ",font=("Arial",11)).grid(row=2, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
tk.Entry(tab3,textvariable=advamt).grid(row=2, column=1,sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
tk.Label(tab3,text="Select Party: ",font=("Arial",11)).grid(row=3, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
tk.OptionMenu(tab3,selectedParty,*partylist).grid(row=3, column=1,sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
tk.Label(tab3,text="Select Payment Accounts: ",font=("Arial",11)).grid(row=4, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
tk.OptionMenu(tab3,selectedAcct,*Acct).grid(row=4, column=1,sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
tk.Label(tab3,text="Select Date : ",font=("Arial",11)).grid(row=5, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
cal=Calendar(tab3,selectmode='day')
cal.grid(row=5,column=1,sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)

#tk.Button(tab3,text="Submit",command=RemoveTruck,fg="black",bg="green").grid(row=6,column=1,padx=(10,0),pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.Label(tab3,text="Expenditure : ",font=("Arial",11)).grid(row=6, column=0,sticky=tk.W+tk.E+tk.N+tk.S)
tk.Button(tab3,text="Add",command=AddExpend).grid(row=6,column=1,sticky=tk.W+tk.E+tk.N+tk.S)
tk.Button(tab3,text="Done",command=DoneAdding).grid(row=6,column=2,sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)

tk.Label(tab5,text="Select UID. : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.OptionMenu(tab5,selectedUID,*UID).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
tk.Button(tab5,text="Remove",command=RemoveTrip,fg="black",bg="green").grid(row=2,column=1,padx=(10,0),pady=(10,0))

tk.Label(tab4,text="Select UID : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.OptionMenu(tab4,selectedUID,*UID).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.Button(tab4,text="Submit",command=ShowUID,fg="black",bg="green").grid(row=1,column=0,padx=(10,0),pady=(10,0))

tk.Label(tab10,text="Enter Expentiture Type : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0))
tk.Entry(tab10,textvariable=newexpend).grid(row=0, column=1, pady=(10,0))
tk.Button(tab10,text="Add",command=AddNewExpend,fg="black",bg="green").grid(row=1,column=0,padx=(10,0),pady=(10,0))

tk.Label(tab11,text="Remove Expenditure Type : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.OptionMenu(tab11,selectedExpendRemove,*expendlist).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.Button(tab11,text="Submit",command=RemoveExpend,fg="black",bg="green").grid(row=1,column=0,padx=(10,0),pady=(10,0))

tk.Label(tab12,text="Enter Party Name : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0))
tk.Entry(tab12,textvariable=partyname).grid(row=0, column=1, pady=(10,0))
tk.Button(tab12,text="Add",command=AddParty,fg="black",bg="green").grid(row=1,column=0,padx=(10,0),pady=(10,0))

tk.Label(tab13,text="Remove Party : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.OptionMenu(tab13,selectedParty,*partylist).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.Button(tab13,text="Submit",command=RemoveParty,fg="black",bg="green").grid(row=1,column=0,padx=(10,0),pady=(10,0))

tk.Label(tab6,text="Select UID : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.OptionMenu(tab6,selectedUID,*cUID).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.Button(tab6,text="Submit",command=CompletedTrips,fg="black",bg="green").grid(row=1,column=0,padx=(10,0),pady=(10,0))

tk.Label(tab7,text="Select UID : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.OptionMenu(tab7,selectedUID,*pUID).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S)
tk.Button(tab7,text="Submit",command=PendingTrips,fg="black",bg="green").grid(row=1,column=0,padx=(10,0),pady=(10,0))

tk.Label(tab14,text="Enter Account No. : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0))
tk.Entry(tab14,textvariable=accountno).grid(row=0, column=1, pady=(10,0))
tk.Button(tab14,text="Add",command=AddAccount,fg="black",bg="green").grid(row=1,column=0,padx=(10,0),pady=(10,0))


tk.Label(tab15,text="Select Account No. : ",font=("Arial",11)).grid(row=0, column=0, pady=(10,0))
tk.OptionMenu(tab15,selectedAcct,*Acct).grid(row=0, column=1,pady=(10,0),sticky=tk.W+tk.E+tk.N+tk.S,columnspan=3)
tk.Button(tab15,text="Remove",command=RemoveAccount,fg="black",bg="green").grid(row=1,column=0,padx=(10,0),pady=(10,0))

tk.mainloop()

