import DECLOG as loginhandler
import init
import pymysql
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
import pickle as p
import Settings
import Wizard
global opt
opt=''
global root
root = tk.Tk()
root.title('Decagon')
init.SQLInit()
#===========================================================================================================================================================================
def chkfile(filename):
    '''Checks for existence of file'''
    try:
        with open(filename, 'r'):
            return True
    except FileNotFoundError:
        return False

            

def login(logtry=False):
    '''Initiates the login process, requests for username & password'''
    def attempt(menu,options,window):
                
                opt=menu.get()
                
                if opt in options:
                    
                    window.destroy()
                    showmain(opt)
                    
                else:
                    pass
                
    #Auto in code:
                
    #if logtry==True: 
       # if chkfile('logindetails.dat'):
         #   records=[]
          #  with open('logindetails.dat', 'rb') as file:
               #     while True:
                  #      try:
                     #       records.append(p.load(file))
                    #    except EOFError:
             #               break
            #loginquery=tk.Toplevel(root)
            #loginquery.geometry('600x400')
           # loginquery.resizable(False,False)
            #root.withdraw()
           # options=[]
           # for i in records:
            #    options.append(i[0])
            
            
            #prompt=tk.Label(loginquery,text='Choose user to login with: ')
            #menu=ttk.Combobox(loginquery,values=options)
            #menu.pack()
            #login=tk.Button(loginquery,text='Login',command=lambda:attempt(menu,options,loginquery))
            #login.pack()
            
        
            
    if logtry==False:           
        root.geometry('400x200')
        root.resizable(False,False)

        tk.Label(root, text='Enter Username:').pack()
        userfield = ttk.Entry(root)
        userfield.pack()

        tk.Label(root, text='Enter Password:').pack()
        passfield = ttk.Entry(root, show="*")
        passfield.pack()
        
        ttk.Button(root, text='Login',command=lambda:loginbutton(userfield, passfield,opt)).pack()
        root.bind('<Return>',lambda event:loginbutton(userfield, passfield,opt))
        
def loginbutton(userfield, passfield,opt):
    '''Function to check for existence of username,password, their validity and accordingly permits/rejects '''
    userid = userfield.get().strip()
    passwd = passfield.get().strip()
    
    dat=loginhandler.decode()
    
    perm=2
    try:
        for i in dat.keys():
            if i==userid and dat[i][0]==passwd:
                perm=dat[i][1]
                
                username=i
                showmain(opt,perm,i)
                break
            else:
                if i==list(dat.keys())[-1]:
                    wrong_cred=tk.Toplevel(root)
                    wrong_cred.geometry('200x100')
                    wrong_cred.resizable(False,False)

                    tk.Label(wrong_cred,text='Wrong Username/Password!').pack()
                    ttk.Button(wrong_cred,text='Ok',command=wrong_cred.destroy).pack()
                

    except Exception as e:
        print(e)
        pass

    
        
        
        
        
        #ask_autologin(userid, passwd,opt) #Remove comment for autologin
            

#def ask_autologin(perm, passwd,opt):
    #autologprompt = tk.Toplevel(root)
    #autologprompt.geometry('300x100')

    #tk.Label(autologprompt,
             #text='Would you like to login automatically next time?').pack()

    #tk.Button(autologprompt, text='Yes',
              #command=lambda: savelogindetails(userid, passwd, autologprompt,opt)).pack()
    #tk.Button(autologprompt, text='No',
              #command=lambda: close0(autologprompt)).pack()

#def close0(win):
    #with open('saved.txt', 'w') as file:
        #file.write('Saved : False')
    #win.destroy()
    #showmain(opt)


def showmain(opt,perm,username):
    '''Opens the main window where the user can select between changing settings (if they have root privileges) or initiating file transfer'''
    
    try:
        root.withdraw()
    except:
        pass
    
    mainwin = tk.Toplevel(root)
    mainwin.geometry('1336x768')
    
    
    tk.Label(mainwin, text='DECAGON FILE TRANSFER',font=('Times New Roman',25)).pack()
    def buttonfunction(button):
        ''''Function for buttons to direct user to the file transfer wizard or settings as needed'''
        try:
            if button==settings_button and button.cget('bg')=='green':
                Settings.Settings(root,username,perm)
        except:
            pass
        if button==wizard_button and button.cget('bg')=='green':
            Wizard.init(root,username,perm)
            
    def colorchange(button):
        '''Controls the colour change of the buttons as they are clicked'''
        if button.cget('bg')=='grey':
            button.config(bg='green')

        elif button.cget('bg')=='green':
            button.config(bg='grey')
        buttonfunction(button)
    
    menubar=Menu(mainwin)
    mainwin.config(menu=menubar)
    def History():
        ''''Manages the logic for retrieving the log of operations and their display'''
        la = pymysql.connect(host = "localhost",user = "root", password = "sql123",database='DEK')
        try:
            init.SQLInit()
        except:
            pass
        cur=la.cursor()
        cur.execute('select * from LOG')
        dat=cur.fetchall()
        
        hiswin=tk.Toplevel(root)
        hiswin.geometry('800x600')
        hiswin.resizable(True,False)
        
        tk.Label(hiswin,text='File Path | Date | Time | Sys',font=('Times New Eoman',25)).place(x=250,y=0)
        val=[]
        for rec in dat:
            val.append(rec[2])
        varx=250
        vary=40
        result=tk.Label(hiswin,text='')
        result.place(x=varx,y=vary)
        def searchrec(arg):
            ''''Accepts an argument of a transaction whose details are to be searched, and returns the details of that particular transition'''
            result.config(text='')
            for i in dat:
                if i[2]!='None' and i[2]==arg:
                    result.config(text=f'{i[2]} | {i[3]} | {i[4]} | {i[5]}',font=('Times New Roman',14))
                  
        select=ttk.Combobox(hiswin,values=val)
        select.place(x=250,y=100)
        search=ttk.Button(hiswin,text='Search',command=lambda:searchrec(str(select.get())))
        search.place(x=250,y=150)
        
                    
                
        
        
    File_Transfer=Menu(menubar,tearoff=0)
    menubar.add_cascade(label='File Transfer',menu=File_Transfer)
    File_Transfer.add_command(label='New...',command=lambda:Wizard.init(root,username,perm))
    File_Transfer.add_command(label='History...',command=History) 
    
    if perm in (0,1):
        settings=Menu(menubar,tearoff=0)
        menubar.add_cascade(label='Settings',menu=settings)
        settings.add_command(label='Privacy Settings...',command=lambda:Settings.Settings(root,username,perm))
        

        settings_button=tk.Button(mainwin,width=10,height=4,text='Settings',font=('Arial',30),bg='grey')
        settings_button.config(command=lambda:colorchange(settings_button))
        settings_button.place(x=400,y=100)

    Quit=Menu(menubar,tearoff=0)
    menubar.add_cascade(label='Quit',menu=Quit)
    Quit.add_command(label='Quit...',command=mainwin.destroy)
            
    wizard_button=tk.Button(mainwin,width=10,height=4,text='File Transfer \n Wizard',font=('Arial',30),bg='grey')
    wizard_button.config(command=lambda:colorchange(wizard_button))
    wizard_button.place(x=100,y=100)

    

    
  
   
        
    
    
#===========================================================================================================================================================================

logintry=False
try:
    with open('info.bin','rb') as file:
        file.close()
    #logintry=True #Remove comment if auto login is to be enabled
except:
    with open('info.bin','wb') as file:
        pass
    loginhandler.encode({'root':['123',0]})
    logintry=False
login(logintry) 

root.mainloop()
