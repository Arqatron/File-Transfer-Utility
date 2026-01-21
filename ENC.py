import pickle
import os
'''
Simple binary encoder for python code
by GauthamK, mainly for Decagon Project
May be used for other projects as well.

Its main purpose is to prevent tampering of the code
Main functions are

encode(file) - encodes the file to "kernel.bin"
decode() - decodes all the files from "kernel.bin"
'''
global files
def chkfile(file):
    '''internal file check function, not to be called outside this program'''
    try:
        z = open(file,"rb")
        z.close()
        return True
    except:
        return False

def encode(file):
    '''
    Primary encoder

    Encoding process
    1) It takes the file's contents
    2) It splits the contents to a list, with each individual character as an element
    3) It makes a dictionary with the format {<FileName>:<Contents stored in list>}
    4) This dictionary is dumped to the external file'''
    if chkfile(file):
        if file[-3::] == ".py":
            z = open(file,"r")
            a = z.read()
            b = []
            for i in a:
                b.append(i)
            c = {file:b}
            z.close()
            ab = open("kernel.bin","ab")
            pickle.dump(c,ab)
            ab.close()
        else:
            z = open(file,"rb")
            a = z.read()
            c = {file:a}
            z.close()
            ab = open("kernel.bin","ab")
            pickle.dump(c,ab)
            ab.close()

def chkfile2():
    try:
        z = open("kernel.bin","rb")
        z.close()
        return True
    except:
        return False

def decode():
    global files
    files = []
    if chkfile2():
        with open("kernel.bin","rb") as ab:
            try:
                while True:
                    #print("item")
                    a = pickle.load(ab)
                    #print(a)
                    files.append(str(list(a.keys())[0]))
                    if (list(a.keys())[0])[-3::] == ".py":
                        z = open(list(a.keys())[0],"w")
                        zr = ""
                        for i in a[list(a.keys())[0]]:
                            zr = zr + str(i)
                        z.write(zr)
                        z.close()
                    else:
                        z = z = open(list(a.keys())[0],"wb")
                        z.write(a[list(a.keys())[0]])
                        z.close()
            except EOFError:
                kz2 = open("files.bin","wb")
                pickle.dump(files, kz2)
                kz2.close()
                return True
            except ValueError:
                return False
                    
    else:
        return False

def encinfo():
    global files
    if chkfile2() and chkfile("info.bin"):
        os.system("xcopy kernel.bin back.bin /Q /-I")
        with open("back.bin","rb") as zr:
            nuFile = open("kernel.bin", "wb")
            found = False
            while True:
                try:
                    k = pickle.load(zr)
                    if list(k.keys())[0] == "info.bin":
                        found = True
                        z = open("info.bin" ,"rb")
                        a = z.read()
                        c = {"info.bin":a}
                        z.close()
                        pickle.dump(c,nuFile)
                    else:
                        pickle.dump(k,nuFile)
                except EOFError:
                    if found == False:
                        z = open("info.bin" ,"rb")
                        a = z.read()
                        c = {"info.bin":a}
                        z.close()
                        pickle.dump(c,nuFile)
                    nuFile.close()
                    zr.close()
                    os.system("del back.bin /Q")
                    if "info.bin" not in files:
                        files.append("info.bin")
                    return True
                    break
                except:
                    nuFile.close()
                    zr.close()
                    os.system("del kernel.bin /Q")
                    os.rename("back.bin","kernel.bin")
                    return False
                    break
def clear():
    global files
    print("STUB")
    try:
        print(files)
    except:
        kz2 = open("files.bin","rb")
        files = pickle.load(kz2)
        kz2.close()
    print(files)
    if len(files) == 0:
        return False
    else:
        for i in files:
            os.system("delete "+i)


    
