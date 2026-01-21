import pickle
'''
Very rudimentary password handler
'''

def chkfile(file):
    '''internal file check function, not to be called outside this program'''
    try:
        z = open(file,"rb")
        z.close()
        return True
    except:
        return False

def encode(c):
    if chkfile("info.bin"):
        for i in c.keys():
            z = []
            for j in c[i][0][::-1]:
                z.append(j)
            c[i][0] = z
        ab = open("info.bin","wb")
        pickle.dump(c,ab)
        ab.close()
        return True
    else:
        return False


def decode():
    if chkfile("info.bin"):
        with open("info.bin","rb") as ab:
            z = pickle.load(ab)
            for i in z.keys():
                c = ""
                for j in z[i][0][::-1]:
                    c = c+str(j)
                z[i][0] = c
            return z
    else:
        return {}
