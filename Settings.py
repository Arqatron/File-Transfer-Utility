
import tkinter as tk
from tkinter import ttk
import pickle as p
import os
import DECLOG as loginhandler


def Settings(window,username,perm=2):
    root=tk.Toplevel(window)
    root.withdraw()
    root.title('Decagon-Settings')
    

    def Search(combobox_obj, combobox_options):
        Setwin.withdraw()
        searched=combobox_obj.get()
        if searched in combobox_options:
            if searched.strip().lower() == 'add users':
                def add_user(win,permobj):
                    uname=ufield.get()
                    upasswd=upass.get()
                    perm=permobj.get()
                    records=loginhandler.decode()
                    newrec={}
                    
                    for i in records:
                        newrec[i]=records[i]
                    newrec[uname]=[upasswd,perm]
                            
                    
                    if len(uname.strip())!=0 and len(upasswd.strip())!=0:
                        try:
                            loginhandler.encode(newrec)
                               
                        except Exception as e:
                            print(e)
                                
                    win.destroy() 
                global reg
                reg=tk.Toplevel(Setwin)
                reg.title('Add Users')
                reg.geometry('400x300')
                reg.resizable(False,False)
                
                tk.Label(reg, text="Enter new user's username:").pack()
                global ufield
                ufield = ttk.Entry(reg)
                ufield.pack()

                tk.Label(reg, text="Enter new user's password:").pack()
                global upass
                upass = ttk.Entry(reg, show="*")
                upass.pack()

                tk.Label(reg,text='Permission:').pack()
                permchk=ttk.Combobox(reg,values=[0,1,2])
                permchk.pack()

                ttk.Button(reg, text="Save", command=lambda:add_user(reg,permchk)).pack()
            if searched.strip().lower()=='remove users':
                global rem
                rem=tk.Toplevel(Setwin)
                rem.geometry('400x300')
                rem.title('Remove Users')
                rem.resizable(False,False)
                rec=loginhandler.decode()
                ulist=[]
                for i in rec.keys():
                    if rec[i][1]!=0:
                        ulist.append(i)
                

                
                def start_removal():
                    rem.withdraw()
                    os.remove('info.bin')
                    records=loginhandler.decode()
                    for i in records.keys():
                            if records[i].lower()!=uname.get().lower():
                                loginhandler.encode({i:[records[i][0],records[i][1]]})
                    success=tk.Toplevel(Setwin)
                    success.geometry('200x100')
                    success.resizable(False,False)
                    success_lab=tk.Label(success,text=f'"{uname.get()} has been removed!"')
                    success_lab.pack()
                    okconf=ttk.Button(success,text='Ok',command=lambda:success.destroy()).pack()
                tk.Label(rem,text='Enter Username:').pack()
                uname=ttk.Combobox(rem,values=ulist)
                uname.pack()

                conf=ttk.Button(rem,text='Confirm',command=start_removal)
                conf.pack()            
                    
            if searched.strip().lower()=='revert':
                revwin=tk.Toplevel(Setwin)
                revwin.title('Revert')
                revwin.geometry('500x400')
                revwin.resizable(False,False)

                lab=tk.Label(revwin,text="Enter File name you'd like to recover:")
                lab.pack()
                    
                    
            if searched.strip().lower()=='change username':
                chuwin=tk.Toplevel(Setwin)
                chuwin.geometry('500x400')
                chuwin.resizable(False,False)
                chuwin.title('Change Username')

                def conf(usebox,newuse,data):
                    unew=newuse.get()
                    uold=usebox.get()
                    tempdat=data[uold]
                    data.pop(uold)
                    data[unew]=tempdat

                    loginhandler.encode(data)
                    chuwin.withdraw()
                    
                    
                    

                data=loginhandler.decode()
                dat=[]
                for i in data.keys():
                    if i!='root':
                        dat.append(i)
                inst=tk.Label(chuwin,text='Choose User:')
                inst.place(x=100,y=0)
                usebox=ttk.Combobox(chuwin,values=dat)
                usebox.place(x=120,y=50)

                newuse=ttk.Entry(chuwin)
                newuse.place(x=120,y=75)

                confirm=ttk.Button(chuwin,text='Confirm',command=lambda:conf(usebox,newuse,data))
                confirm.place(x=120,y=100)
                
                    
            if searched.strip().lower()=='change password':
                chpwin=tk.Toplevel(Setwin)
                chpwin.geometry('500x400')
                chpwin.resizable(False,False)

                def conf(usebox,newpass,data):
                    uname=usebox.get()
                    perm=data[uname][1]
                    data.pop(uname)
                    data[uname]=[str(newpass.get()),perm]
                    loginhandler.encode(data)
                    chpwin.withdraw()
                data=loginhandler.decode()
                dat=[]
                for i in data.keys():
                    if i!='root':
                        dat.append(i)
                inst=tk.Label(chpwin,text='Choose User:')
                inst.place(x=100,y=0)

                usebox=ttk.Combobox(chpwin,values=dat)
                usebox.place(x=120,y=50)
                
                newpass=ttk.Entry(chpwin)
                newpass.place(x=120,y=75)
            
                confirm=ttk.Button(chpwin,text='Confirm',command=lambda:conf(usebox,newpass,data))
                confirm.place(x=120,y=100)
                

    Setwin = tk.Toplevel(root)
    root.withdraw()
    Setwin.geometry('400x300')
    Setwin.resizable(False,False)
    
    if perm==0: 
        options = ['Add Users','Remove Users','Change Username','Change Password']
    elif perm==1:
        options = ['']
    
    cbox = ttk.Combobox(Setwin, values=options)
    cbox.pack()

    ttk.Button(Setwin, text='Search', command=lambda: Search(cbox, options)).pack()

    Setwin.mainloop()
