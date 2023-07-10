import sys

'''
Group A7
Assembler
'''
c = 0

labels = {}
vars={} 
L = []
lister = []
MC = {"R0":0,"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0}
count = 0
im = 0
opcod = {'add':'10000',
        'sub':'10001',
        'mov':'10010',#move immediate
        'mov_':'10011',#move register
        'ld':'10100',
        'st':'10101',
        'mul':'10110',
        'div':'10111',
        'rs':'11000',
        'ls':'11001',
        'xor':'11010',
        'or':'11011',
        'and':'11100',
        'not':'11101',
        'cmp':'11110',
        'jmp':'11111',
        'jlt':'01100',
        'jgt':'01101',
        'je':'01111',
        'hlt':'01010'}

reg_cod = {'R0':'000',
        'R1':'001',
        'R2':'010',
        'R3':'011',
        'R4':'100',
        'R5':'101',
        'R6':'110',
        'FLAGS':'111'}

flags = {"V":0,"L":0,"G":0,"E":0}

Type = {
    'add':'A',
    'sub':'A',
    'mov':'B',#immediate
    'mov_':'C',#register
    'ld':'D',
    'st':'D',
    'mul':'A',
    'div':'C',
    'rs':'B',
    'ls':'B',
    'xor':'A',
    'or':'A',
    'and':'A',
    'not':'C',
    'cmp':'C',
    'jmp':'E',
    'jlt':'E',
    'jgt':'E',
    'je':'E',
    'var' : 'var',
    'VAR' : 'VAR',
    'hlt':'F',
    '.':'.'
}

bs = ""

def outpu(lister):
    # print(lister)
    o = sys.stdout
    for a in lister:
        o.write(a + '\n')
    sys.exit()

def cbin(n):
    global bs
    bs = ""
    while(n != 0):
        r = n % 2
        bs = bs + str(r)
        n = n // 2
    return bs[::-1]

def cbin1(a):
    opcstr = ""
    bnr = cbin(a)
    zs = 8 - len(bnr)
    im = zs * '0'
    opcstr = opcstr + im
    opcstr = opcstr + bnr
    return opcstr

def typeA(m):
    global lister
    opcstr = ""
    zs = ""
    if(len(m) != 4):
        sys.stderr.write("Syntax Error: Invalid syntax for type A instruction")
    for i in opcod:
        if(m[0] == i):
            opcstr = opcstr + opcod[i]  
    zs = 2 * '0'
    opcstr = opcstr + zs
    if(MC[m[2]] > (2**16)):
        flags["V"] = 1
    if(m[1] == "FLAGS" or m[2] == "FLAGS" or m[3] == "FLAGS"):
        sys.stderr.write("Error in line : " + str(count) + " Illegal Use of Flags")
        return
    if(not(0 <= int(m[1][1]) < 7)):
        sys.stderr.write("Error in line : " + str(count) + " Not a valid register")
        return
    if(not(0 <= int(m[2][1]) < 7)):
        sys.stderr.write("Error in line : " + str(count) + " Not a valid register")
        return
    if(not(0 <= int(m[3][1]) < 7)):
        sys.stderr.write("Error in line : " + str(count) + " Not a valid register")
        return
    if(m[1][0] != "R" or m[2][0] != "R" or m[3][0] != "R"):
        sys.stderr.write("Error in line : " + str(count) + " Not a valid register")
        return
    else:
        for i in range(1,4):
            if m[i] in reg_cod.keys():
                opcstr+=reg_cod[m[i]]
        lister.append(opcstr)

def typeB(m):
    global lister
    global count
    global bs
    opcstr = ""
    global im
    if(len(m) != 3):
        sys.stderr.write("Syntax Error: Invalid syntax for type B instruction")
    for i in opcod:
        if(m[0] == i):
            opcstr = opcstr + opcod[i]
    for i in reg_cod:
        if(m[1] == i and m[1]!= "FLAGS" and 0 <= int(m[1][1]) < 7):
            opcstr = opcstr + reg_cod[i]
        elif(m[1] == "FLAGS"):
            sys.stderr.write("Error in line : " + str(count) + " Illegal Use of Flags")
            return
        elif(not(0 <= int(m[1][1]) < 7)):
            sys.stderr.write("Error in line : " + str(count) + " Not a valid register")
            return
        elif(m[1][0] != "R"):
            sys.stderr.write("Error in line : " + str(count) + " Not a valid register")
            return
    # for i in range(1,len(m)):
    try:
        m[2] = m[2][1:]
        im_ = int(m[2])
    except ValueError:
        m[2] = m[2][1:]
        im = cbin(int(m[2]))
        l = 8 - len(im)
        zs = l * '0'
        im = zs + im
        opcstr = opcstr + im
    if (im_<0 or im_>255):
        sys.stderr.write("Error: Immediate value is not correct")
    else:
        im = cbin(im_)
        l = 8 - len(im)
        zs = l * '0'
        im = zs + im
        opcstr = opcstr + im
    lister.append(opcstr)
    bs = ""
        
def typeC(m):
    global lister
    global count
    global bs
    opcstr = ""
    global im
    if(len(m) != 3):
        sys.stderr.write("Syntax Error: Invalid syntax for type B instruction")
    for i in opcod:
        if(m[0] == i):
            opcstr = opcstr + opcod[i]
    zs = 5 * '0'
    opcstr = opcstr + zs
    if(MC[m[1]] == MC[m[2]]):
        pass#to set up the flags register
    for i in reg_cod:
        if(m[1] == i and m[1]!= "FLAGS" and 0 <= int(m[1][1]) < 7):
            opcstr = opcstr + reg_cod[i]
        if(m[2] == i and m[2]!= "FLAGS" and 0 <= int(m[2][1]) < 7):
            opcstr = opcstr + reg_cod[i]
        elif(m[1] == "FLAGS"):
            sys.stderr.write("Error in line : " + str(count) + " Illegal Use of Flags")
            return
        elif(not(0 <= int(m[1][1]) < 7)):
            sys.stderr.write("Error in line : " + str(count) + " Not a valid register")
            return
        elif(m[1][0] != "R"):
            sys.stderr.write("Error in line : " + str(count) + " Not a valid register")
            return
    lister.append(opcstr)
    bs = ""

def typeD(m,L):
    global vars
    global count
    global c
    global lister
    # global L
    opcstr = ""
    if(len(m) != 3):
        sys.stderr.write("Syntax Error: Invalid syntax for type D instruction")
    # c=0
    # i=0
    # while(L[i][0]=="var" and i<=len(L)-1):
    #     c+=1
    #     i+=1
    for i in range(len(L)):
        if(L[i][0] == "var"):
            c = c + 1
    x = c
    for i in range(c):
        if (L[i][0]=="var" and len(vars) == 0):
            # print((len(L)-x)+i)
            vars[L[i][1]]=cbin1((len(L)-x)+i)
        elif (L[i][0]=="var" and len(vars) != 0):
            vars.clear()
            a = 0
            for i in range(len(L)):
                if(L[i][0] == "var"):
                    a = a + 1
            for i in range(a):
                vars[L[i][1]]=cbin1((len(L)-a)+i)
            

    # for i in vars:
    #     print(i, vars[i])
           
    # for i in range(len(L)):
    #     if (L[i][0]) != "var":
    #         c = c + 1
    # x = c
    # for i in range(len(L)):
    #     if(L[i][0] == "var"):
    #         # vars[L[i][1]] = 0
    #         # x = ((len(L)-x)+i)
    #         vars[L[i][1]] = cbin1(x)
    #         x = x + 1

    if m[0]==("st"):
        try:
            opcstr = opcstr + opcod[m[0]]
            opcstr = opcstr + reg_cod[m[1]]    
            opcstr = opcstr + vars[m[2]]
            lister.append(opcstr)
        except KeyError:
            sys.stderr.write("The variable has not been declared.")
    if m[0]==("ld"):
        try:
            opcstr = opcstr + opcod[m[0]]
            opcstr = opcstr + reg_cod[m[1]]    
            opcstr = opcstr + vars[m[2]]
            lister.append(opcstr)
        except KeyError:
            sys.stderr.write("The variable has not been declared.")
    elif(m[1] == "FLAGS"):
        sys.stderr.write("Error in line : " + str(count) + " Illegal Use of Flags")
        return
    elif(not(0 <= int(m[1][1]) < 7)):
        sys.stderr.write("Error in line : " + str(count) + " Not a valid register")
        return
    elif(m[1][0] != "R"):
        sys.stderr.write("Error in line : " + str(count) + " Not a valid register")
        return



def typeE(m,L):
    global labels    
    global lister
    opcstr = ""
    zs = ""
    if(len(m) != 2):
        sys.stderr.write("Syntax Error: Invalid syntax for type E instruction")
    for i in opcod:
        if(m[0] == i):
            opcstr = opcstr + opcod[i]
    zs = 3 * '0'
    opcstr = opcstr + zs
    # try:
    #     opcstr = opcstr + str(m[1])
    # except IndexError:
    #     opcstr = opcstr + m[1]
    for i in range(len(L)):
        if(L[i][0] == "jmp" or L[i][0] == "jlt" or L[i][0] == "jgt" or L[i][0] == "je"):
            if (L[i][1]) in labels:
                opcstr = opcstr + labels[L[i][1]]
            else:
                sys.stderr.write("Error: label not found")
    lister.append(opcstr)
    if(m[0] == "jlt"):
        flags['L'] = 1
    if(m[0] == "jgt"):
        flags['G'] = 1
    if(m[0] == "je"):
        flags['E'] = 1
    
def typeF(m):
    global lister
    global count
    opcstr = ""

    if(len(m) != 1):
        sys.stderr.write("Syntax Error: Invalid syntax for type F instruction")
    for i in opcod:
        if(m[0] == i):
            opcstr = opcstr + opcod[i]
    zs = 11 * '0'
    opcstr = opcstr + zs
    lister.append(opcstr)
    
    outpu(lister)

def typeld(m,L):
    global c
    global count
    global vars
    global lister
    # global L
    opcstr = ""
    if(len(m) != 3):
        sys.stderr.write("Syntax Error: Invalid syntax for type D instruction")
    # i=0
    # while(L[i][0]=="var" and i<=len(L)-1):
    #     c+=1
    #     i+=1
    # for i in range(len(L)):
    #     if(L[i][0] == "var"):
    #         c = c + 1
    # for i in range(c):
    #     if L[i][0]=="var":
    #         vars[L[i][1]]=cbin1((len(L)-c)+i)

    for i in range(len(L)):
        if(L[i][0] == "var"):
            c = c + 1
    x = c
    for i in range(c):
        if (L[i][0]=="var" and len(vars) == 0):
            # print((len(L)-x)+i)
            vars[L[i][1]]=cbin1((len(L)-x)+i)
        elif (L[i][0]=="var" and len(vars) != 0):
            vars.clear()
            a = 0
            for i in range(len(L)):
                if(L[i][0] == "var"):
                    a = a + 1
            for i in range(a):
                vars[L[i][1]]=cbin1((len(L)-a)+i)
        

    # for i in vars:
    #     print(i, vars[i])
    if m[0]==("ld"):
            try:
                opcstr = opcstr + opcod[m[0]]
                opcstr = opcstr + reg_cod[m[1]]    
                opcstr = opcstr + vars[m[2]]
                lister.append(opcstr)
            except KeyError:
                sys.stderr.write("The variable has not been declared.")

    elif(m[1] == "FLAGS"):
        sys.stderr.write("Error in line : " + str(count) + " Illegal Use of Flags")
        return
    elif(not(0 <= int(m[1][1]) < 7)):
        sys.stderr.write("Error in line : " + str(count) + " Not a valid register")
        return
    elif(m[1][0] != "R"):
        sys.stderr.write("Error in line : " + str(count) + " Not a valid register")
        return
    

def checker(L):
    global labels
    # print(L)
    for i in range(len(L)):
        m = L[i]
        if(L[i][0] == "mov" and L[i][2][0] == "$"):
            typeB(m)
        elif(L[i][0] == "mov" and L[i][2][0] == "R"):
            k = L[i]
            k[0] = "mov_"
            typeC(m)
        elif(L[i][0] == "mul" and len(m) == 4):
            typeA(m)
        elif(L[i][0] == "add" and len(m) == 4):
            typeA(m)
        elif(L[i][0] == "sub" and len(m) == 4):
            typeA(m)
        elif(L[i][0] == "st" and len(m) == 3):
            typeD(m,L)
        elif(L[i][0] == "ld" and len(m) == 3):
            typeld(m,L)
        elif(L[i][0] == "div"):
            typeC(m)
        elif(L[i][0] == "rs" and L[i][2][0] == "$"):
            typeB(m)
        elif(L[i][0] == "ls" and L[i][2][0] == "$"):
            typeB(m)
        elif(L[i][0] == "xor" and len(m) == 4):
            typeA(m)
        elif(L[i][0] == "or" and len(m) == 4):
            typeA(m)
        elif(L[i][0] == "and" and len(m) == 4):
            typeA(m)
        elif(L[i][0] == "not"):
            typeC(m)
        elif(L[i][0] == "cmp"):
            typeC(m)
        elif(L[i][0] == "jmp" and len(m) == 2):
            typeE(m,L)
        elif(L[i][0] == "jlt" and len(m) == 2):
            typeE(m,L)
        elif(L[i][0] == "jgt" and len(m) == 2):
            typeE(m,L)
        elif(L[i][0] == "je" and len(m) == 2):
            typeE(m,L)
        elif(L[i][0] == "hlt"):
            typeF(m)
        if(L[i].count(L[i][0]) > 1):
            # print(L[i].count(L[i][0]))
            sys.stderr.write("Error!! Label can be entered only once")
            quit()
        if(L[i][0][-1] == ":"):
            Type[L[i][0]] = L[i][0]
        else:
            if(m[0] not in Type):
                sys.stderr.write("Please enter valid input")
                # print(Type)
                quit()
        

def main():
    global labels
    global count
    s = "new"
    L = []
    while(s!='hlt'):
        s = sys.stdin.readline()
        count = count + 1
        m = s.split()
        if(m[0] != "hlt"):
            print(m[0])
            L.append(m)
            # print(m)
            # print(L)
            for line in m:
                if (line[-1] == ":"):#identifying labels
                    labels[line[0:-1]] = cbin1(count)#storing the label with their line number
                    print(cbin1(count))
                    m.pop(0)

            if(L[0][0] == "hlt" and count == 1):
                sys.stderr.write("Error in line : " + str(count) + " Halt Instruction can't be used in the beginning")
                typeF(m)
            else:
                 if(L[0][0] != "var"):
                    for i in range(1,len(L)):
                        if L[i][0]=="var":
                            sys.stderr.write("Error in line : " + str(count) + " Variable is not declared at the beginning")
                            quit()
        else:
            for i in range(15):
                if (" "*i) in m:
                    m.remove(" "*i)
            else:
                L.append(m)
            # if(m[0] == "label")
            checker(L)
            break
        #     for i in range(0,len(L)):
        #         if(L[i][0] == "mov" and L[i][2][0] == "$"):
        #             typeB(m)
        #         elif(L[i][0] == "mov" and L[i][2][0] == "R"):
        #             k = L[i]
        #             k[0] = "mov_"
        #             typeC(m)
        #         elif(L[i][0] == "mul" and len(m) == 4):
        #             typeA(m)
        #         elif(L[i][0] == "add" and len(m) == 4):
        #             typeA(m)
        #         elif(L[i][0] == "sub" and len(m) == 4):
        #             typeA(m)
        #         elif(L[i][0] == "st" and len(m) == 3):
        #             typeD(m,L)
        #         elif(L[i][0] == "ld" and len(m) == 3):
        #             typeD(m,L)
        #         elif(L[i][0] == "div"):
        #             typeC(m)
        #         elif(L[i][0] == "rs" and L[i][2][0] == "$"):
        #             typeB(m)
        #         elif(L[i][0] == "ls" and L[i][2][0] == "$"):
        #             typeB(m)
        #         elif(L[i][0] == "xor" and len(m) == 4):
        #             typeA(m)
        #         elif(L[i][0] == "or" and len(m) == 4):
        #             typeA(m)
        #         elif(L[i][0] == "and" and len(m) == 4):
        #             typeA(m)
        #         elif(L[i][0] == "not"):
        #             typeC(m)
        #         elif(L[i][0] == "cmp"):
        #             typeC(m)
        #         elif(L[i][0] == "jmp" and len(m) == 2):
        #             typeE(m,L)
        #         elif(L[i][0] == "jlt" and len(m) == 2):
        #             typeE(m,L)
        #         elif(L[i][0] == "jgt" and len(m) == 2):
        #             typeE(m,L)
        #         elif(L[i][0] == "je" and len(m) == 2):
        #             typeE(m,L)
        #         elif(L[i][0] == "hlt"):
        #             typeF(m,L)
        #         '''elif(i>0 and L[i][0] == "var"):
        #             sys.stderr.write("Error in line: "+str(count)+" Variables can only be declared in the beginning")
        #             sys.exit()
        #         else:
        #             sys.stderr.write("Error in line: "+str(count)+" Please enter the instructions in valid format")
        #             sys.exit()'''
    
main()