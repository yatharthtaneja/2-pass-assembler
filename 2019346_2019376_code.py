"""pc is program counter , ilc is location counter , start and end count is to check multiple end or start
aopcode contains all opcodes aslist 
opcode containts opcodes as dictionaries 
opcode_w_operands contains all the opcodes that will be followed by an operand  """
global pc
global ilc
global startcount
global endcount
pc=0
startcount=0
endcount=0
ilc=0
aopcode=["CLA","LAC","SAC","ADD","SUB","BRZ","BRN","BRP","INP","DSP","MUL","DIV","STP"]
opcode={'CLA':'0000','LAC':'0001','SAC':'0010','ADD':'0011','SUB':'0100','BRZ':'0101','BRN':'0110','BRP':'0111','INP':'1000','DSP':'1001','MUL':'1010','DIV':'1011','STP':'1100'}
# opcode_w_operand=["LAC","SAC","ADD","SUB","BRZ","BRN","BRP","INP","DSP","MUL","DIV"]
labletable=["BRP","BRN","BRZ"]
opcodetable=[]
symboltavle={}
literaltabke={}
#helper function to remove space from list
def remove_empty(li):
    for i in li:
        if '' in li:
            li.remove('')
            # print(li)
    for i in li:
        if "" in li:
            remove_empty(li)   
#helper function to convert to binary   input output as string 12 digit address 
def to_binary(s):
    x=int(s)
    sum=0
    exp=1
    while(x>0):
        digit=x%2
        x=x//2
        sum+=digit*exp
        exp*=10
    sum='0'*(8-len(str(sum)))+str(sum)
    return sum
# print(to_binary(10))

#helper function to check type of the command
def check_line(com,line):
    global endcount
    global startcount
    li=com.split(" ")
    remove_empty(li)
    if(li[0]=="START"):
        startcount+=1
        return 1
    elif(li[0]=="END"):
        endcount+=1
        return 1
    elif(li[0] in aopcode):
        return 2
    else:
        print(" ERROR: SYNTAX ERROR \n LINE: ",line) #ERROR NUMBER 2  
        exit()
# print(check_line("CLA",10))

def pass1():
    global ilc
    global pc
    global startcount
    global endcount
    line_no=1
    ends=False 
    with open("input.txt","r") as file1:
        for line in file1:
            if(line[-1]=='\n'):
                line=line[:-1]
            #empty line
            if(line==""):
                continue
            #for comments use // 
            if(line.find("//")!=-1):
                line=line[:line.find("//")]
            if(ends):
                print(" ERROR: INSTRUCTION AFTER END  \n LINE: ",line_no) #error number 8
                exit()
            if(line_no==1):
                c1=line.find("START")
                if(c1==-1):
                    print(" ERROR: FILE DOESNT START WITH START \n LINE: ",line_no) #ERROR NUMBER 1
                    exit()
                else:
                    startcount+=1
                    start=line.split(" ")
                    remove_empty(start)
                    #assigning the initial pc value
                    if(len(start)==2):
                        pc=int(start[1])
                        ilc=pc
                    elif(len(start)==1):
                        ilc=0
                        pc=0
                    else:
                        print(" ERROR: ILLEGAL EXPRESSION AFTER START \n LINE: ",line_no) #error number 3
                        exit()
                line_no+=1
                continue
            if(line!=""):
                if(line.find(":")==-1):
                    statement=line.split(" ")
                    remove_empty(statement)
                    stype=check_line(line,line_no)
                    if(statement[0]=="CLA" or statement[0]=="STP" or statement[0]=="END"  ):
                        opcodetable.append([statement[0],"-"])
                    else:
                        if(len(statement)<2):
                            print(" ERROR: NO OPERAND \n LINE: ",line_no) #error number 3
                            exit()
                        elif(len(statement)>2):
                            print(" ERROR: MORE THAN ONE OPERAND \n LINE: ",line_no) #error number 4
                            exit()
                        # elif(statement[1].isalnum()==False):
                        #     print(" ERROR: ONLY ALPHABETS AND NUMBERS CAN BE USED TO DEFINE SYMBOLS \n LINE: ",line_no) #error number 8
                        #     exit()

                        elif(statement[0]in labletable):
                            if(statement[1]in symboltavle and  symboltavle[statement[1]]==-1):
                                print(" ERROR: LABLE WAS EXPECTED AS OPERAND \n LINE: ",line_no) #error number 7
                                exit()
                            elif(statement[1] not in symboltavle):
                                symboltavle[statement[1]]=-1*line_no
                            elif(statement[1][0]=="(" and statement[1][-1]==")"):
                                print(" ERROR: LABLE WAS EXPECTED AS OPERAND \n LINE: ",line_no) #error number 7
                                exit()
                        else:
                            if(statement[1]in symboltavle and symboltavle[statement[1]]!=-1):
                                print(" ERROR: LABLE GIVEN AS OPERAND \n LINE: ",line_no) #error number 2
                                exit()
                            elif(statement[1] in aopcode):
                                print(" ERROR: OPCODE GIVEN AS OPERAND \n LINE: ",line_no) #error number 14
                                exit()

                            elif(statement[1][0]=="(" and statement[1][-1]==")"):
                                if(statement[1][1:-1].isdigit()==True and statement[1][-1] not in literaltabke):
                                    literaltabke[statement[1][1:-1]]=-1
                                elif(statement[1][1:-1].isdigit()==False):
                                    print(" ERROR: LITERAL SHOULD BE A NUMBER \n LINE: ",line_no) #error number 15
                                    exit()
                            elif(statement[1] not in symboltavle):
                                symboltavle[statement[1]]=-1
                        opcodetable.append([statement[0],statement[1]])
                else:
                    #break statements case
                    statement2=line.split(":")
                    remove_empty(statement2)
                    label=statement2[0]
                    label=label.split(" ")
                    remove_empty(label)
                    if(len(label)==0):
                        print(" ERROR: NO LABEL NAME \n LINE: ",line_no) #error number 6
                        exit()
                    l=label[0]
                    if(l not in symboltavle ):
                        symboltavle[l]=ilc
                    elif(l in symboltavle and symboltavle[l]<-1):
                        symboltavle[l]=ilc
                    elif(l in symboltavle and symboltavle[l]==-1):
                        print(" ERROR: INVALID LABLE NAME ALREADY DECLARED AS SYMBOL \n LINE: ",line_no) #error number 6
                        exit()

                    else:
                        print(" ERROR: MULTIPLE LABLE DECLARATON \n LINE: ",line_no) #error number 6
                        exit()
                    ilc+=12
                    pc+=1
                    index1=line.find(":")+1
                    line=line[index1:]
                    if(line!=""):
                        statement=line.split(" ")
                        remove_empty(statement)
                        stype=check_line(line,line_no)
                        if(statement[0]=="CLA" or statement[0]=="STP" or statement[0]=="END"):
                            opcodetable.append([statement[0],"-"])
                        else:
                            if(len(statement)<2):
                                print(" ERROR: NO OPERAND \n LINE: ",line_no) #error number 4
                                exit()
                            elif(len(statement)>2):
                                print(" ERROR: MORE THAN ONE OPERAND \n LINE: ",line_no) #error number 5
                                exit()
                            # elif(statement[1].isalnum()==False):
                            #     print(" ERROR: ONLY ALPHABETS AND NUMBERS CAN BE USED TO DEFINE SYMBOLS \n LINE: ",line_no) #error number 8
                            #     exit()

                            elif(statement[0]in labletable):
                                if(statement[1]in symboltavle and  symboltavle[statement[1]]==-1):
                                    print(" ERROR: LABLE WAS EXPECTED AS OPERAND \n LINE: ",line_no) #error number 7
                                    exit()
                                elif(statement[1] not in symboltavle):
                                    symboltavle[statement[1]]=-1*line_no
                                elif(statement[1][0]=="(" and statement[1][-1]==")"):
                                    print(" ERROR: LABLE WAS EXPECTED AS OPERAND \n LINE: ",line_no) #error number 7
                                    exit()
                            else:
                                if(statement[1]in symboltavle and symboltavle[statement[1]]!=-1):
                                    print(" ERROR: LABLE GIVEN AS OPERAND \n LINE: ",line_no) #error number 6
                                    exit()
                                elif(statement[1] in aopcode):
                                    print(" ERROR: OPCODE GIVEN AS OPERAND \n LINE: ",line_no) #error number 14
                                    exit()
                                elif(statement[1][0]=="(" and statement[1][-1]==")"):
                                    if(statement[1][1:-1].isdigit()==True and statement[1][-1] not in literaltabke):
                                        literaltabke[statement[1][1:-1]]=-1
                                    elif(statement[1][1:-1].isdigit()==False):
                                        print(" ERROR: LITERAL SHOULD BE A NUMBER \n LINE: ",line_no) #error number 6
                                        exit()
                                elif(statement[1] not in symboltavle):
                                    symboltavle[statement[1]]=-1
                            opcodetable.append([statement[0],statement[1]])
            # print(symboltavle)
            # print(literaltabke)
            # print(opcodetable)
            
            if(stype==1 and endcount==1):
                ends=True
            
            if(endcount>1):
                print(" ERROR: MULTIPLE END PROVIDED \n LINE: ",line_no) #error number 5
                exit()
            if(startcount>1):
                print(" ERROR: MULLTIPLE START PROVIDED  \n LINE: ",line_no) #error number 7
                exit()
            if(stype!=1):
                ilc+=12
                pc+=1
                line_no+=1
        
    if(endcount==0): 
        print(" ERROR: NO END PROVIDED \n LINE: ",line_no) #error number 6
        exit()
    for k in symboltavle:
        if(symboltavle[k]==-1):
            symboltavle[k]=ilc
            ilc+=12
        if(symboltavle[k]<-1):
            print(" ERROR: LABEL GIVEN BUT NOT DEFINED \n LINE: ",line_no) #error number 10
            exit()
    for j in literaltabke:
        if(literaltabke[j]==-1):
            literaltabke[j]=ilc
            ilc+=12
    if(ilc>=256):
        print(" ERROR: ADDRESS OVERFLOW \n LINE: ",line_no) #error number 16
        exit()


    

pass1()
# print(symboltavle)
# print(literaltabke)
# print(opcodetable)
def pass2():
    ans=[]
    for op in opcodetable:
        if(op[0]=="END"):
            continue
        ans.append(opcode[op[0]])
        if(op[1]!="-"):
            if(op[1][0]=="(" and op[1][-1]==")"):
                op[1]=op[1][1:-1]
            if(op[1] in symboltavle):
                b1=to_binary(symboltavle[op[1]])
                ans.append(b1)
            elif(op[1] in literaltabke):
                b1=to_binary(literaltabke[op[1]])
                ans.append(b1)
        ans.append("\n")
        file2= open("output.txt","w")
        file2.writelines(ans)
        file2.close()
    print("COMPILATION SUCESSFULL!")
pass2()        

            




                            
                            
            


    

                            
            




