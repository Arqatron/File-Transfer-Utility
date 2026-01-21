
    
def init(window,username,perm=2):
    '''Initializes the wizard,requires the username and permission'''
    import init as copytool
    copytool.SQLInit()
    global File_display
    import pymysql 
    import tkinter as tk
    
    from tkinter import filedialog as fd
    from tkinter import ttk
    
    import os

    global root
    global subroot
    root=tk.Toplevel(window)
    root.withdraw()
    subroot=tk.Toplevel(root)

    subroot.geometry('500x400')
    subroot.title('Wizard')
    subroot.resizable(False,False)
    
    
    
    def filetransfer(username,perm):
        '''Handles all file transfer functions, requires username and permission level'''
        global filepaths
        filepaths=[]
        root.withdraw()

        subroot.destroy()
        filewin=tk.Toplevel(root)

        img2=tk.PhotoImage(file='wiz.png')
        img3=img.subsample(11,2)
        photo=tk.Label(master=filewin,image=img3)
        photo.image=img3
        photo.place(x=10,y=0)
        def opfile():
            
            path=fd.askopenfilename(filetypes=[('All Files','*.*')])
            try:
                File_display.config(text=f'Currently Opened: {path}')
            except:
                pass
            
            
            filepaths.append(path)
        def store(nvar):
            varstore=[]
            varstore.append(nvar)
            return varstore
        def move(button,win):
            def scopy(win,filepaths):
                    
                    def cont3(filepaths):
                        
                                    
                        la = pymysql.connect(host = "localhost",user = "root", password = "sql123",database='DEK')
                        cur=la.cursor()

                        if len(str(pc_entry.get()))>0:
                            cur.execute("SELECT MAX(G_ID) FROM LOG;")
                            ar=cur.fetchall()
                            arz=int(ar[0][0])+1
                            
                            try:
                                
                                operation=copytool.CopyInit(str(filepaths[-1]),str(prefix.get())+str(pc_entry.get()),False,username,0,arz,perm)
                                
                                filepaths=[]
                            except Exception as e:
                                print(e)
                                pass
                        else:
                            pass
                    
                    win.withdraw()
                    scopy_win=tk.Toplevel(root)
                    scopy_win.geometry('500x400')
                    scopy_win.resizable(False,False)
                    scopy_win.title('Single Copy')

                    prefix=ttk.Combobox(scopy_win,values=['NPS',' '])
                    prefix.place(x=150,y=150)
                    
                    pc=tk.Label(master=scopy_win,text='Please enter the system number that \nyou want to copy the file to:')
                    pc.place(x=150,y=0)
                    
                    img2=tk.PhotoImage(file='wiz.png')
                    img3=img.subsample(11,2)
                    photo=tk.Label(master=scopy_win,image=img3)
                    photo.image=img3
                    photo.place(x=10,y=0)
                    
                    pc_entry=ttk.Entry(scopy_win)
                    pc_entry.place(x=150,y=50)

                    copyconf=ttk.Button(master=scopy_win,text='Confirm',command=lambda:cont3(filepaths))
                    copyconf.place(x=150,y=200)

                    
                
            def mcopy(win,filepaths):
                
                    '''Multi copy function - requires window and list of filepaths to be entered'''
                    win.withdraw()
                    mcopy_win=tk.Toplevel(root) 
                    mcopy_win.geometry('500x400')
                    mcopy_win.resizable(False,False)
                    mcopy_win.title('Multicopy')

                    img2=tk.PhotoImage(file='wiz.png')
                    img3=img.subsample(11,2)
                    photo=tk.Label(master=mcopy_win,image=img3)
                    photo.image=img3
                    photo.place(x=10,y=0)

                    prefix=ttk.Combobox(mcopy_win,values=['NPS',' '])
                    prefix.place(x=150,y=150)
                    
                    sys_prompt=tk.Label(mcopy_win,text='Enter the target system numbers:')
                    sys_prompt.pack()

                    sys=ttk.Entry(master=mcopy_win)
                    sys.pack()

                    def confirm(filepaths):
                        if len(str(sys))>0:
                            systems=str(sys.get()).split(',')
                            
                            la = pymysql.connect(host = "localhost",user = "root", password = "sql123",database='DEK')
                            cur=la.cursor()
                            cur.execute("SELECT MAX(G_ID) FROM LOG;")
                            ar=cur.fetchall()
                            arz=int(ar[0][0])+1
                            for i in systems:
                                for j in filepaths:
                                    try:
                                        operation=copytool.CopyInit(str(j),str(prefix.get())+str(i),False,username,0,arz,perm)
                                            
                                        
                                        
                                    except Exception as e:
                                        
                                        pass
                                    else:
                                        pass
                               

                               
                            filepaths=[]   
                            
                    multc=ttk.Button(master=mcopy_win,text='Confirm')
                    multc.config(command=lambda:confirm(filepaths))
                    multc.pack()
            
            try:               
                if button==next2:
                    
                    opfile()
                    scopy(win,filepaths)
                
                if button==next3:
                    
                    newpath=fd.askopenfilename(filetypes=[('All Files','*.*')])
                    if len(newpath)>0:
                        filepaths.append(newpath)
                        File_display.config(text=f'Currently Opened: {filepaths}')
                    if len(filepaths)==1:
                        mult=ttk.Button(win,text='Continue to Multicopy',command=lambda:mcopy(win,filepaths))
                        mult.place(x=150,y=350)
            except:
                pass
               
        filewin.title('File Transfer')
        filewin.geometry('525x400')
        filewin.resizable(False,False)
        File_display=tk.Label(filewin,text='Currently Opened:')
        File_display.place(x=170,y=200)
        def back_to_wiz(username):
            filewin.destroy()
            init(root,username,perm)
            
            
        back=ttk.Button(master=filewin,text='Back',command=lambda:back_to_wiz(username))
        back.place(x=0,y=350)
        
        filewin.wm_attributes('-topmost',True)

        
        Optxt=tk.Label(filewin,text='Choose single/multi copy method: ',font=('Times New Roman',20))
        Optxt.place(x=117,y=0)

        
        
        
        global next3
        global next2
        next2=ttk.Button(filewin,text='Single Copy')
        next2.config(command=lambda:move(next2,filewin))
        next2.place(x=400,y=350)

        if perm==0:
            next3=ttk.Button(filewin,text='Multi Copy')
            next3.config(command=lambda:move(next3,filewin))
            next3.place(x=300,y=350)


        
    
        
        
        
    def opexec(operation):
        
        if operation.lower()=='file transfer':
            filetransfer(username,perm)
            
        elif operation.lower()=='revert':
            revert()
        elif operation=='':
            pass
    def buttonconf(option):
        
        
        if option.lower()=='file transfer':
            if op1.cget('bg')=='green':
                op1.config(bg='grey')
            
            elif op1.cget('bg')=='grey':
                op1.config(bg='green')
                
            if op1.cget('bg')=='green':
                sub0.config(command=lambda:opexec(option))
            else:
                sub0.config(command=lambda:opexec(''))
           
        
    
    
    
    

    
    #image code - DO NOT TOUCH
    img=tk.PhotoImage(file='wiz.png')
    img1=img.subsample(11,2)
    photo=tk.Label(master=subroot,image=img1)
    photo.image=img
    photo.place(x=10,y=0)
    #----------------------------------------------
    title=ttk.Label(subroot,text='Wizard',font=('Times New Roman',20))
    
    title.place(x=250,y=0)
    
    inst1=tk.Label(subroot,text="This wizard will help you transfer files from one system to another. \n First, select an option to proceed.\
\n \n Please select an option: ")
    inst1.place(x=125,y=50)
    
    op1=tk.Button(subroot,text='File Transfer',command=lambda:buttonconf('File Transfer'),bg='grey')
    op1.place(x=250,y=200)

    sub0=ttk.Button(subroot,text='Next')
    sub0.place(x=400,y=350)
    
    
    root.mainloop()

        
        


    















