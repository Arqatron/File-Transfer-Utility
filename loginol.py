import tkinter
from tkinter import ttk
import init
import mysql.connector as mc
def display():
    z = mc.connect(host="localhost",user="root",password="sql123",database="dek")
    if z.is_connected():
        cur = z.cursor()
        cur.execute("SELECT * FROM LOG;")
        k = cur.fetchall()
    return k

def log():
    k = display()
    for i in range(0,len(k),1):
        z = ttk.Frame(frame1, borderwidth = 2, relief = "sunken")
        for j in range(0,len(k[i]),1):
            zi = ttk.Label(z, text = k[i][j],borderwidth=2, relief="sunken")
            zi.grid(column=j+1, row = 1, sticky ="e")
        z.grid(column=1, row = 4 + i, sticky="ew")


def Wizzo():
    wizzo_root = tkinter.Tk()
    wizzo_root.resizable(False, False)
    wizzo_root.title("Sample Wizard")
    wizzo_root.update_idletasks()
    style = ttk.Style()
    style.configure('Custom.TFrame', background='blue')
    x = wizzo_root.winfo_screenwidth() //2 - 500//2
    y = wizzo_root.winfo_screenheight() //2 - 400//2
    wizzo_root.geometry(f"500x400+{x}+{y}")
    StartFrame = ttk.Frame(wizzo_root, padding=(5,10))
    StartFrame.pack(fill="both")
    InnerFrame = ttk.Frame(StartFrame, style="Custom.TFrame")
    InnerFrame.grid(column = 1, row = 1, columnspan = 5, rowspan = 10, sticky ="nse")
    '''zText = ttk.Label(StartFrame, text = "This is a sample Wizard", font=("Tahoma",16,"bold"))
    zText.grid(column=1, row = 1, sticky = "e")'''
    
root = tkinter.Tk()
root.resizable(False, False)

root.title("Decagon Settings")


root.update_idletasks()
x = root.winfo_screenwidth() //2 - 500//2
y = root.winfo_screenheight() //2 - 400//2
root.geometry(f"500x400+{x}+{y}")

notebook = ttk.Notebook(root)
frame1 = ttk.Frame(notebook, padding=(5,10))
frame2 = ttk.Frame(notebook, padding=(5,10))
frame1.pack(fill="both")
frame2.pack(fill="both")
notebook.add(frame1, text="Log")
notebook.add(frame2, text="Wizard test")
notebook.pack(fill="both")

labelA = ttk.Label(frame1, text = "Log", font=("Tahoma", 16, "bold"))
labelA.grid(column=1, row=2, sticky = "ew")
log()


labelB = ttk.Button(frame2, text = "Start Wizard",command = Wizzo)
labelB.grid(column=10, row=1, sticky = "ew")

root.mainloop()
