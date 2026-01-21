'''
Main Decagon Library
init.py

SQL SCHEMA

T_ID, G_ID, FILE, DATE, TIME, SYS_NAME, SUCCESS, REVERT, REF, OP, USER


'''
import pymysql
import os
import time
import ENC


def SQLInit():
    try:
        la = pymysql.connect(host = "localhost",user = "root", password = "sql123")

    
                
    except Exception as e:
        print(e)
        print("\nFailed to initialise SQL Connection!")
        return 1
    def is_connected():
        try:
            la.ping(reconnect=False)
            print('1')
            return True
        except pymysql.Error as e:
            print(e)
            print('0')
            return False
    if not is_connected():
        return 1
    cur = la.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS DEK")
    cur.execute("USE DEK")
    try:
        cur.execute("SELECT * FROM LOG")
        a = cur.fetchall()
    except:
        cur.execute("CREATE TABLE LOG(T_ID BIGINT UNIQUE NOT NULL, G_ID BIGINT NOT NULL, F_NAME VARCHAR(100) NOT NULL, DATE DATE NOT NULL, TIME TIME NOT NULL, SYSNAME VARCHAR(25) NOT NULL, SUCCESS INT NOT NULL CHECK (SUCCESS = 1 OR SUCCESS = 0), REVERT INT NOT NULL CHECK (REVERT = 0 OR REVERT = 1), REF INT,OP INT CHECK(OP = 1 OR OP = 0), USER VARCHAR(25) NOT NULL)")
        cur.execute("INSERT INTO LOG VALUES(0,0,'None','1970-01-01','00:00:00','none',1,1,NULL,0,'None');")
    cur.execute("COMMIT;")
    la.close()
    return 0

def copy(file,sysname):
    '''
    Administrative/Teacher copy, supports folder copying and will overwrite the file if it already exists
    '''
    #print("an attempt was made")
    file = file.replace("/","\\")
    if file[-1] == "*":
        g = file.split("\\")[-2]
        os.system(f'''mkdir \\\\{sysname}\\D\\"g"''')
        os.system(f'''xcopy "{file}" \\\\{sysname}\\D\\"g" /e /Y >> cpystat''')
        with open("cpystat","r") as copystat:
            a = copystat.readlines()
            if "0 f" in a[1].lower()[:3:]:
                success = False
            else:
                success = True
    else:
        os.system(f'''xcopy "{file}" \\\\{sysname}\\D\\ /Y >> cpystat''')
        with open("cpystat","r") as copystat:
            a = copystat.readlines()
            if "0 f" == a[-1].lower()[:3:]:
                success = False
            else:
                success = True
    os.system("del cpystat")
    ztime = time.strftime("%H:%M:%S")
    date = time.strftime("%Y-%m-%d")
    return success, ztime, date

def Zdel(file,sysname):
    file = file.replace("/","\\")
    g = file.split("\\")[-1]
    print(g)
    if file in ["*","*.*","*.",".*",""," "]:
        success = False
    if file[-1] == "*":
        g = file.split("\\")[-2]
        print(f'''rmdir \\\\{sysname}\\D\\"{g}" /S /Q''')
        z = os.system(f'''rmdir \\\\{sysname}\\D\\"{g}" /S /Q''')
        if int(z) == 1:
            success = True
        else:
            success = False
    else:
        print(f'''del \\\\{sysname}\\D\\"{g}" /Q >> delstat''')
        os.system(f'''del \\\\{sysname}\\D\\"{g}" /Q >> delstat''')
        with open("delstat","r") as copystat:
            a = copystat.read()
            if "deleted" in a.lower():
                success = True
            else:
                success = False
        os.system("del delstat")
    ztime = time.strftime("%H:%M:%S")
    date = time.strftime("%Y-%m-%d")
    return success, ztime, date


def simCopy(file,sysname):
    '''
    Copying for unprivelleged users, will not copy if file exists
    Can only handle single files'''
    file = file.replace("\\","/")
    try:
        with open(file,"rb") as initFile:
            initcontent = initFile.read()
        filename = file.split("/")[-1]
        with open("//"+str(sysname)+"/D/"+filename,"xb") as FinalFile:
            FinalFile.write(initcontent)
        success = True
    except Exception as e:
        print(e)
        success = False
    ztime = time.strftime("%H:%M:%S")
    date = time.strftime("%Y-%m-%d")
    return success, ztime, date

def multiCopy(file,sysList,rev,user,tid,gid,priv):
    la = pymysql.connect(host="localhost", user="root", password="sql123", database="DEK")
    if not is_connected() == 1:
        return 1
    if priv not in [0,1]:
        return 2
    if rev == True:
        for i in sysList:
            success, ztime, date = copy(file,i)
            ref = tid
            if success:
                cur.execute(f"UPDATE LOG SET REVERT = 1 WHERE T_ID = {tid};")
            cur = la.cursor()
            cur.execute(f"SELECT MAX(T_ID) FROM LOG;")
            file = file.replace("\\","/")
            thing = cur.fetchall()
            number = int(thing[0][0])
            cur.execute(f"INSERT INTO LOG VALUES ({number+1},{gid},'{file}','{date}','{ztime}','{i}',{int(success)},{int(rev)},{ref},0,'{user}');")
            cur.execute("COMMIT;")
        la.close()
        return 0
    else:
        for i in sysList:
            success, ztime, date = copy(file,i)
            ref = "NULL"
            cur = la.cursor()
            cur.execute(f"SELECT MAX(T_ID) FROM LOG;")
            file = file.replace("\\","/")
            thing = cur.fetchall()
            number = int(thing[0][0])
            cur.execute(f"INSERT INTO LOG VALUES ({number+1},{gid},'{file}','{date}','{ztime}','{i}',{int(success)},{int(rev)},{ref},0,'{user}');")
            cur.execute("COMMIT;")
        la.close()
        return 0

def multiDel(file,sysList,rev,user,tid,gid,priv):
    '''Administrative deletion of folders/files of multiple systems, cannot be accessed by others for obvious reasons'''
    la = pymysql.connect(host="localhost", user="root", password="sql123", database="")
    if not is_connected() == 1:
        return 1
    if priv not in [0,1]:
        return 2
    if rev == True:
        for i in sysList:
            success, ztime, date = ZDel(file,i)
            ref = tid
            if success:
                cur.execute(f"UPDATE LOG SET REVERT = 1 WHERE T_ID = {tid};")
            cur = la.cursor()
            cur.execute(f"SELECT MAX(T_ID) FROM LOG;")
            file = file.replace("\\","/")
            thing = cur.fetchall()
            number = int(thing[0][0])
            cur.execute(f"INSERT INTO LOG VALUES ({number+1},{gid},'{file}','{date}','{ztime}','{i}',{int(success)},{int(rev)},{ref},1,'{user}');")
            cur.execute("COMMIT;")
        la.close()
        return 0
    else:
        for i in sysList:
            success, ztime, date = ZDel(file,i)
            ref = "NULL"
            cur = la.cursor()
            cur.execute(f"SELECT MAX(T_ID) FROM LOG;")
            file = file.replace("\\","/")
            thing = cur.fetchall()
            number = int(thing[0][0])
            cur.execute(f"INSERT INTO LOG VALUES ({number+1},{gid},'{file}','{date}','{ztime}','{i}',{int(success)},{int(rev)},{ref},1,'{user}');")
            cur.execute("COMMIT;")
        la.close()
        return 0


def DelInit(file,sysname,rev,user,tid,gid,priv):
    '''Administrative deletion of folders/files, cannot be accessed by others for obvious reasons'''
    la = pymysql.connect(host="localhost", user="root", password="sql123", database="DEK")
    if not is_connected() == 1:
        return 1
    cur = la.cursor()
    if priv not in [0,1]:
        return 2
    if rev == True:
        success,ztime,date = Zdel(file,sysname)
        if success:
            cur.execute(f"UPDATE LOG SET REVERT = 1 WHERE T_ID = {tid};")
        ref = tid
    else:
        success,ztime,date = Zdel(file,sysname)
        ref = "NULL"
    
    cur.execute(f"SELECT MAX(T_ID) FROM LOG;")
    file = file.replace("\\","/")
    thing = cur.fetchall()
    number = int(thing[0][0])
    cur.execute(f"INSERT INTO LOG VALUES ({number+1},{gid},'{file}','{date}','{ztime}','{sysname}',{int(success)},{int(rev)},{ref},1,'{user}');")
    cur.execute("COMMIT;")
    la.close()

def CopyInit(file,sysname,rev,user,tid,gid,priv):
    '''
    Main function to initiate a copy
    '''
    la = pymysql.connect(host="localhost", user="root", password="sql123", database="DEK")
    if not is_connected() == 1:
        return 1
    cur = la.cursor()
    if rev == True:
        success, time, date = copy(file,sysname)
        ref = tid
        if success:
            cur.execute(f"UPDATE LOG SET REVERT = 1 WHERE T_ID = {tid};")        
    else:
        if priv in [0,1]:
            success, ztime, date = copy(file,sysname)
            ref = "NULL"
        else:
            success, ztime, date = simCopy(file, sysname)
            ref = "NULL"
    file = file.replace("\\","/")
    cur.execute(f"SELECT MAX(T_ID) FROM LOG;")
    thing = cur.fetchall()
    number = int(thing[0][0])
    cur.execute(f"INSERT INTO LOG VALUES ({number+1},{gid},'{file}','{date}','{ztime}','{sysname}',{int(success)},{int(rev)},{ref},0,'{user}');")
    cur.execute("COMMIT;")
    la.close()
    return 0

def revert(user,gid,priv):
    la = pymysql.connect(host="localhost",user="root",password="sql123",database="DEK")
    if not is_connected() == 1:
        return 1
    if priv not in [0,1]:
        return 2
    cur = la.cursor()
    try:
        cur.execute(f"SELECT * FROM LOG WHERE G_ID = {gid};")
        z = cur.fetchall()
    except:
        return 3
    cur.execute("SELECT MAX(G_ID) FROM LOG;")
    ar = cur.fetchall()
    arz = int(ar[0][0]) + 1
    for i in z:
        if i[6] == 1:
            # Logically cannot revert a deleted file unless a copy is stored elsewhere.
            '''if i[9] == 1:
                CopyInit(i[2],i[5],True,user,i[0],arz,priv)'''
            if i[9] == 0:
                DelInit(i[2],i[5],True,user,i[0],arz,priv)
            else:
                return 4
    return 0
