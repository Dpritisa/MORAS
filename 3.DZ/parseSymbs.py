def _parse_symbols(self):
    # Inicijalizacija predefiniranih oznaka.
    self._init_symbols()
    
    # Prvo parsiramo deklaracije oznaka. Npr. "(LOOP)".
    self._iter_lines(self._parse_labels)

    # Na kraju parsiramo varijable i reference na oznake te ih pretvaramo u
    # konstante. Npr. "@SCREEN" pretvaramo u "@16384" ili "@END" kojemu je
    # oznaka "(END)" bila u trecoj liniji pretvaramo u "@3".
    self._n = 16
    self._iter_lines(self._parse_variables)





#2. zadatak
def _makro_naredbe (self):
    lines = []
    i = 0;
    for(line, m , n) in self._lines:
        if line[0] == "$" and line[1:6] == "WHILE":
            self._broj+=1
            a = line[6:].split(")")
            b = a[0].split(",") 
            c = b[0].split("(") # c[1] = A
            if len(a) == 2 and len(b) == 1 and len(c[0]) == 0 and len(a[1])<1 and len(c)<=2 and len(b[0])>1:
                lines.append(("(WHILE"+str(self._broj)+ ")",i,n))
                lines.append(("@"+ str(b[0]),i+1,n))
                lines.append(("D=M",i+2,n))
                lines.append(("@"+ "END"+ str(self._broj),i+3,n))
                lines.append(("D;JEQ",i+4,n))
                self._lines_while.append(n)
                i+=5
            else:
                self._flag = False
                self._errm = "Incorrect WHILE macro."
                self._line = n
                break 
        
        elif line[0]=="$" and line[1:4]=="END" :
            if self._broj==0:
                self._flag=False
                self._errm="incorrect while loop"
                self._line=n
                break
            lines.append(("@"+"WHILE"+str(self._broj),i,n))
            lines.append(("0;JMP",i+1,n))
            lines.append(("(END"+str(self._broj)+ ")",i+2,n))
            self._lines_while.pop()
            i=i+3
            self._broj-=1
            
        elif line[0] == "$" and line[1:3] == "MV":
            l1=line[3:].split(")")
            l2=l1[0].split(",") #------->l2[1] je B
            l3=l2[0].split("(") #--------->l3[1] je A
            if len(l1) == 2 and len(l2)==2 and len(l3) <= 2 and len(l3[0]) <= 0 and len(l1[1])<1 and len(l2[0])>1 and len(l2[1])>=1:
                lines.append(("@"+str(l3[1]),i,n))
                lines.append(("D=M",i+1,n))
                lines.append(("@"+str(l2[1]),i+2,n))
                lines.append(("M=D",i+3,n))
                i=i+4

                #return ["@"+a,"D=M", "@"+b, "M=D"]
                
            else:
                self._flag = False
                self._errm = "Incorrect MV macro."
                self._line = n
                break
            
        elif line[0] == "$" and line[1:4] == "SWP":
            l4=line[4:].split(")")
            l5=l4[0].split(",") #l5[1] je B
            l6=l5[0].split("(") #l6[1] je A
            if len(l4) == 2 and len(l4[1])<1 and len(l5[0])>1 and len(l5[1])!=0 and len(l6[0]) == 0 and len(l5) == 2 and len(l6)<=2:
                lines.append(("@"+str(l6[1]),i,n))
                lines.append(("D=M",i+1,n))
                lines.append(("@"+str(l5[1]),i+2,n))
                lines.append(("MD=D+M",i+3,n))
                lines.append(("@"+str(l6[1]),i+4,n))
                lines.append(("MD=D-M",i+5,n))
                lines.append(("@"+str(l5[1]),i+6,n))
                lines.append(("M=M-D",i+7,n))
                i = i + 8
            else:
                self._flag = False
                self._errm = "Incorrect SWP macro."
                self._line = n
                break 
            
        elif line[0] == "$" and line[1:4] == "SUM":
            l7=line[4:].split(")")
            l8=l7[0].split(",") #l8[1] je B, l8[2] je D
            l9=l8[0].split("(") #l9[1] je A
            if len(l7) == 2 and len(l7[1])<1 and len(l8[0])>1 and len(l8[1])!=0 and len(l8[2])!=0 and len(l8) == 3 and len(l9[0])==0 and len(l9)<=2:
                lines.append(("@"+str(l9[1]),i,n)) 
                lines.append(("D=M",i+1,n))
                lines.append(("@"+str(l8[1]),i+2,n))
                lines.append(("D=D+M",i+3,n))
                lines.append(("@"+str(l8[2]),i+4,n))
                lines.append(("M=D",i+5,n))
                i = i + 6
            else:
                self._flag = False
                self._errm = "Incorrect SUM macro."
                self._line = n
                break           
        else:
            lines.append((line,i,n))
            i = i+1
        self._lines = lines




# Svaka oznaka mora biti sadrzana unutar oblih zagrada. Npr. "(LOOP)". Svaka
# oznaka koju procitamo treba zapamtiti broj linije u kojoj se nalazi i biti
# izbrisana iz nje. Koristimo dictionary _labels.
def _parse_labels(self, line, p, o):
    if line[0] != "(":
        return line
    else:
        label = line[1:].split(")")[0]
        if len(label) == 0:
            self._flag = False
            self._line = o
            self._errm = "Invalid label"
        else:
            self._labels[label] = str(p)
            
    return ""

# Svaki poziv na varijablu ili oznaku je oblika "@NAZIV", gdje naziv nije broj.
# Prvo provjeriti oznake ("_labels"), a potom varijable ("_vars"). Varijablama
# dodjeljujemo memorijske adrese pocevsi od 16. Ova funkcija nikad ne vraca
# prazan string!
def _parse_variables(self, line, p, o):
    if line[0] != "@":
        return line

    l = line[1:]

    if l.isdigit():
        return line

    if l in self._labels.keys():
        return "@" + self._labels[l]
    elif l in self._variables.keys():
        return "@" + self._variables[l]
    else:
        self._variables[l] = str(self._n)
        self._n += 1
        return "@" + str(self._n - 1)

# Inicijalizacija predefiniranih oznaka.
def _init_symbols(self):
    self._labels = {
        "SCREEN" : "16384",
        "KBD" : "24576",
        "SP" : "0",
        "LCL" : "1",
        "ARG" : "2",
        "THIS" : "3",
        "THAT" : "4"
    }
    
    for i in range(0, 16):
        self._labels["R" + str(i)] = str(i)
