# Class used to store information for a wire
import random
from itertools import combinations
import csv
# import matplotlib.pyplot as plt

class Node(object):
    def __init__(self, name, value, gatetype, innames):
        self.name = name # string
        self.value = value # char: '0', '1', 'U' for unknown
        self.gatetype = gatetype # string such as "AND", "OR" etc
        self.is_input = False # boolean: true if this wire is a primary input of the circuit
        self.is_output = False # boolean: true if this wire is a primary output of the circuit
        self.interms = [] #list of nodes (first as strings, then as nodes), each is a input wire to the gatetype
        self.innames = innames  # helper string to temperarily store the interms' names, useful to find all the interms nodes and link them

    def set_value(self, v):
        self.value = v 

    def display(self): # print out the node nicely on one line  
        if self.is_input: 
            nodeinfo = f"input:\t{str(self.name):5} = {self.value:^4}" 
            print(nodeinfo)
            return 
        elif self.is_output:
            nodeinfo = f"output:\t{str(self.name):5} = {self.value:^4}"
            interm_str = " "
            interm_val_str = " "
            for i in self.interms:
                interm_str += str(i.name)+" "
                interm_val_str += str(i.value)+" "
            nodeinfo += f"as {self.gatetype:>5}"
            nodeinfo += f"  of   {interm_str:20} = {interm_val_str:20}"
        else:# internal nodes   
            nodeinfo = f"wire:  \t{str(self.name):5} = {self.value:^4}"
            interm_str = " "
            interm_val_str = " "
            for i in self.interms:
                interm_str += str(i.name)+" "
                interm_val_str += str(i.value)+" "
            nodeinfo += f"as {self.gatetype:>5}"
            nodeinfo += f"  of   {interm_str:20} = {interm_val_str:20}"
        print(nodeinfo)
        return     

    # calculates the value of a node based on 
    #its gate type and values at interm
    def calculate_value(self):
        TheUcase = 0
        The1case = 0
        The0case = 0
        
        if self.gatetype == "AND":
            for i in self.interms:
                if i.value == "U":
                    TheUcase +=1
                if i.value == "0":
                    The0case +=1
                if i.value== "1":
                    The1case +=1
                if The0case >0:
                    val = "0" 
                if TheUcase ==0 and The0case ==0: # 11
                    val = "1" 
                if The1case !=0 and TheUcase !=0: # 1U/U1
                    val = "U" 
                if The1case ==0 and The0case ==0: # UU 
                    val = "U"             
            self.value = val
            return val
        elif self.gatetype == "Equal":
            for i in self.interms:
                if i.value == "U":
                    val = "U"
                if i.value == "0":
                    val = "0"
                if i.value== "1":
                    val = "1"
            self.value = val
            return val   
        elif self.gatetype == "OR":
            for i in self.interms:
                if i.value == "U":
                    TheUcase +=1
                if i.value == "0":
                    The0case +=1
                if i.value == "1":
                    The1case +=1        
                if The1case >0:
                    val = "1"
                if TheUcase ==0 and The1case==0: #00
                    val = "0"
                #if The1case ==0 and TheUcase!=0: #0U CASE
                    #val = "U"  
                if The0case !=0 and TheUcase!=0: #U0/0U
                    val = "U"    
                if The0case ==0 and The1case==0: #UU
                    val ="U"       
            self.value = val
            return val
        elif self.gatetype == "NAND":
            for i in self.interms:
                if i.value == "U":
                    TheUcase +=1
                if i.value == "0":
                    The0case +=1
                if i.value == "1":
                    The1case +=1        
                if The0case >0:
                    val = "1"
                if TheUcase == 0 and The0case ==0: #11
                    val = "0"     
                if The1case !=0 and TheUcase !=0: #1U/U1
                    val = "U" 
                if The1case ==0 and The0case ==0:#UU
                    val = "U"      
            self.value = val
            return val
        elif self.gatetype == "NOT":
            for i in self.interms:
                if i.value == "0":
                    val= "1"
                elif i.value=="1":
                    val="0"
                elif i.value == "U":
                    val="U"
            self.value = val
            return val     
        elif self.gatetype == "XOR":
            for i in self.interms:
                if i.value == "U":
                    TheUcase +=1
                if i.value == "0":
                    The0case +=1
                if i.value == "1":
                    The1case +=1        
                if TheUcase >0: #FOR ANY INPUT U
                    val = "U"
                if The0case ==0 and TheUcase ==0: #11 
                    val = "0"
                if The1case ==0 and TheUcase ==0: #00
                    val = "0" 
                if The0case !=0 and The1case !=0: #01
                    val = "1"                  
            self.value = val
            return val
        elif self.gatetype == "XNOR":
            for i in self.interms:
                if i.value == "U":
                    TheUcase +=1
                if i.value == "0":
                    The0case +=1
                if i.value == "1":
                    The1case +=1        
                if TheUcase >0: #FOR ANY INPUT U
                    val = "U"
                if The0case ==0 and TheUcase ==0: #11 
                    val = "1"
                if The1case ==0 and TheUcase ==0: #00 
                    val = "1" 
                if The0case !=0 and The1case !=0: #01 
                    val = "0" 
            self.value = val
            return val           
        elif self.gatetype == "NOR":
            val = "1"
            for i in self.interms:
                if i.value == "U":
                    TheUcase +=1
                if i.value == "0":
                    The0case +=1
                if i.value == "1":
                    The1case +=1        
                if The1case >0:
                    val = "0"
                if The1case ==0 and TheUcase==0: #00
                    val = "1"
                if The1case ==0 and The0case==0: #UU
                    val = "U"    
                if The0case !=0 and TheUcase!=0: #0U/U0
                    val = "U"                    
            self.value = val
            return val
        elif self.gatetype == "BUFF":
            val = self.interms[0].value
            self.value = val
            return val            
# Take a line from the circuit file which represents a gatetype operation and returns a node that stores the gatetype
def parse_gate(rawline):
# example rawline is: a' = NAND(b', 256, c')
# should return: node_name = a',  node_gatetype = NAND,  node_innames = [b', 256, c']
    # get rid of all spaces
    line = rawline.replace(" ", "")
    # now line = a'=NAND(b',256,c')

    name_end_idx = line.find("=")
    node_name = line[0:name_end_idx]
    # now node_name = a'

    gt_start_idx = line.find("=") + 1
    gt_end_idx = line.find("(")
    node_gatetype = line[gt_start_idx:gt_end_idx]
    # now node_gatetype = NAND

    # get the string of interms between ( ) to build tp_list
    interm_start_idx = line.find("(") + 1
    end_position = line.find(")")
    temp_str = line[interm_start_idx:end_position]
    tp_list = temp_str.split(",")
    # now tp_list = [b', 256, c]
  
    #node_innames = [i for i in tp_list]
    #now node_innames = [b', 256, c]
    fnode_innames = [i for i in tp_list]
    return node_name, node_gatetype, fnode_innames

# Create circuit node list from input file
def construct_nodelist():
    o_name_list = []

    for line in input_file_values:
        if line == "\n":
            continue

        if line.startswith("#"):
            continue

        # TODO: clean this up
        if line.startswith("INPUT"):
            index = line.find(")")

            name = str(line[6:index])
            n = Node(name, "U", "PI", [])
            n.is_input = True

            node_list.append(n)

        elif line.startswith("OUTPUT"):
            index = line.find(")")
            name = line[7:index]
            o_name_list.append(name)

        else:  # majority of internal gates processed here
            node_name, node_gatetype, fnode_innames = parse_gate(line)
            p= Node(node_name, "U", node_gatetype, fnode_innames)
            p.gate_output = True
            for i in range(len(p.innames)):
              #v=node.name
              w= str(p.innames[i])
              p.innames[i] = p.name +"-"+p.innames[i]
              r = p.innames[i]
              #inputof = node.name        
              n = Node(r, "U", "Equal",w)  
              n.gate_input = True
              node_list.append(n)  
            node_list.append(p)

    for n in node_list:
        if n.name in o_name_list:
            n.is_output = True

    # link the interm nodes from parsing the list of node names (string)
    # example: a = AND (b, c, d)
    # thus a.innames = [b, c, d]
    # node = a, want to search the entire node_list for b, c, d
    
    for node in node_list:
        node.innames = [node.innames] if isinstance(node.innames, str) else node.innames
        for cur_name in node.innames:
            for target_node in node_list:
                if target_node.name == str(cur_name):
                    node.interms.append(target_node)
     
    #for node in node_list:
      #print(node.interms)

    return 

def cloning(node_list):
    cloned_list = []
    cloned_list.extend(node_list) 
    return cloned_list

def fault_list():
    for node in node_list:
      all_Faults.append(node.name + "-0")
      all_Faults.append(node.name + "-1")
    return

def cal_multi_list():
  for i in multi_list:
    faultval = 2**len(i)
    temp=0
    while temp<faultval:
      z = []
      index= 0
      x=bin(temp)[2:].zfill(len(i))
      for item in i:
        if index > len(x)-1:
          break
        z.append(item.name+"-"+x[index])
        index = index + 1
      total_multipleFault.append(z)
      temp+=1

def binMake(n):
    a = []
    global binNum
    binNum = []
    if n < 7:
      for i in range(2**n):
          line = [i//2**j%2 for j in reversed(range(n))]
          a.append(line)
    else:
      for x in range(100):
          line = [x//2**j%2 for j in reversed(range(n))]
          a.append(line) 
    for i in range(len(a)):
      temp_input_list = a[i]
      binNum.append(''.join(str(i) for i in temp_input_list))

    return binNum

def hextobin(seed):
  hexadecimal = seed
  end_length = len(hexadecimal) * 4
  hex_as_int = int(hexadecimal, 16)
  hex_as_binary = bin(hex_as_int)
  padded_binary = hex_as_binary[2:].zfill(end_length)
  return padded_binary
  
def Convert(string): 
    li = list(string) 
    return li 
def listToString(s):  
    str1 = ""  
    for ele in s:  
        str1 += ele   
    return str1        

def lfsr(seed, taps):
    a = []
    temp = []
    shiftRight = []
    temp = Convert(seed)
    a.append(seed)
    while shiftRight != seed:
        shiftRight = Convert(temp)
        for t in taps:
          if t > (len(temp)-1):
            continue
          else:  
            shiftRight[t] = str(int(temp[t-1]) ^ int(temp[7]))
        
        for r in range(0,len(shiftRight)):
          if r in taps:
            continue
          elif r==0:
            (shiftRight[r]) = str(temp[7])
          else:
            (shiftRight[r]) = str(temp[r-1]) 

        temp = shiftRight
        shiftRightstr = listToString(shiftRight)     

        a.append(shiftRightstr)
        if len(a) == 100:
            break
    return a


def LFseed(bSeed,taps,inputlen,inSize,tVsize):

  global lfTV
  if inSize < tVsize:
    lfTV = range (0,inSize)
  else:
    lfTV = range (0, tVsize)
  
  slicedSeed = []
  if inputlen > 8:
     tempSeed = len(bSeed)-4
     while inputlen > tempSeed:
       bSeed+=bSeed
       tempSeed = len(bSeed)
       suffseed = tempSeed % 8
       tempSeed -= suffseed
     final_lfsr = inputlen // 8
     partiallfsr = inputlen % 8
     if partiallfsr == 0:
        lfsrsize = final_lfsr
     else:
        lfsrsize = final_lfsr + 1

     a= 0
     b= 8
     tempcount = 0
     while tempcount != lfsrsize:

        tempdivseed = bSeed[a:b]
        slicedSeed.append(tempdivseed)
        a +=8
        b +=8
        tempcount+=1  
  else:
    lfsrsize = 1
    slicedSeed = range(0, lfsrsize)
    slicedSeed = [bSeed[0:8] for i in slicedSeed]  
  temptvlist = []
  count = 0
  for i in range (len(slicedSeed)):
    lfSRfeed = []
    lfSRfeed = lfsr(slicedSeed[i],taps)
    if count == 0: 

       temptvlist.extend(lfSRfeed)
    else:
      minperiod = min(len(temptvlist),len(lfSRfeed))
      for v in range (0,minperiod):  
        temptvlist[v]+=lfSRfeed[v]
    count+=1  
  
  for i in range(len(temptvlist)):
    temptvlist[i] = temptvlist[i][:inputlen]
  if inSize<tVsize:   
    temptvlist = temptvlist [:inSize] 
  else:
    temptvlist = temptvlist [:tVsize]   
  lfTV = temptvlist 
  return lfTV
print("***************************************************")
print('               ECE-464 Project 3')  
print("Are LFSRs good for covering multiple faults?")
print('***************************************************\n')
print("You can test for a 1000 faults with combination of 2 or 40 faults with combinations of 3 but requires 64 bit Python Sim \nCombination of 2-[(a-0,b-1), Combination of 3-(a-0,b-1,c-0)\n")
print ("-------------------------------------------------------------------\n")

# Main function starts
# Step 1: get circuit file name from command line
wantToInputCircuitFile = str(
    input("Provide a benchfile name (return to accept circuit.bench by default):\n"))

if len(wantToInputCircuitFile) != 0:
    circuitFile = wantToInputCircuitFile
    try:
        f = open(circuitFile)
        f.close()
    except FileNotFoundError:
        print('File does not exist, setting circuit file to default')
        circuitFile = "circuit.bench"
else:
    circuitFile = "circuit.bench"

# Constructing the circuit netlist
file1 = open(circuitFile, "r")
input_file_values = file1.readlines()
file1.close()
node_list = []
total_multipleFault=[]
construct_nodelist()
all_Faults = []
fault_list()
testVec = []


print ("-------------------------------------------------------------------")

print (all_Faults)
print ("\nThere are a total of " + str(len(all_Faults))+ " single faults in the given circuit bench\n") 
print ("------------------------------------------------------------------")
whichCombo = input(
  "Which one do you want to continue with?\n" +  
  "1. Enter '1' for multiple fault list with 1000 faults of combination of 2\n" +
  "2. Enter '2' for multiple fault list with 40 faults of combination of 3 \n")

if whichCombo =='1':
 multi_list = []
 temp_list=[]
 temp_list.extend(combinations(node_list,2))
 multi_list.extend(random.sample(temp_list,250))
elif whichCombo =='2':
 multi_list = []
 temp_list=[]
 temp_list.extend(combinations(node_list,3))
 multi_list.extend(random.sample(temp_list,5))


cal_multi_list()
x = input("Use a static sample list(yes or no)")
if (x == 'yes'):
    static_list = input("Enter a static Sample list")
    total_multipleFault = static_list


print("\nThere are a total of " +str(len(total_multipleFault))+" randomly generated faults of combination 1-3 \n")

printmultiple_faultlist = input("Do you want to print the full multiple fault list? (Enter 'yes' or 'no)\n")
if printmultiple_faultlist=='yes':
  print("\nThe full multiple fault list with "+str(len(total_multipleFault))+", possible faults for the given circuit bench is as follows:\n")
  print(total_multipleFault)

print ("\n-------------------------------------------------------------------")

inputlen = 0   
for node in node_list:
   if node.is_input:
     inputlen +=1

tp_prpg = str(input("\n Press (Enter) for 8-bit LFSR for a circuit\n"))

inputspace = 2**inputlen
tVsize = 100
if tp_prpg == "":
  Seed = input("Enter your choice of Seed in hexadecimal format:\n")
  binarySeed = hextobin(Seed)
  tap = input("Enter the tap Configuartion:\n"+ 
        "Type:\n" +
        "1 for no taps\n" +
        "2 for taps at 2,4,5\n" +
        "3 for taps at 2,3,4\n" + 
        "4 for taps at 3,5,7\n")
  if tap == "1":
    taps = []
    LFseed(binarySeed,taps,inputlen,inputspace,tVsize)
    testVec = lfTV 
  elif tap == "2":
    taps = [2,4,5]
    LFseed(binarySeed,taps,inputlen,inputspace,tVsize)
    testVec = lfTV
  elif tap == "3":
    taps = [2,3,4]
    LFseed(binarySeed,taps,inputlen,inputspace,tVsize)
    testVec = lfTV
  elif tap == "4":
    taps = [3,5,7]
    LFseed(binarySeed,taps,inputlen,inputspace,tVsize)
    testVec = lfTV     

print ("\n-------------------------------------------------------------------")

startBegin = str(input("\nPress Enter to begin fault coverage of test vectors\n"))

if startBegin=="":   
  print("\n Given following test vector list:")
  print(testVec)
  print ("\n-------------------------------------------------------------------")
  print("\nThe fault coverage of the  " + str(len(testVec)) + " Test Vectors in order is as follows:\n")
  alldrep = [] # all faults detected by all tvs with repetition
  alldetected = [] # all faults detected by all tvs without rep. 'D'
  count_plot = 1
  per_plot_list = []
  plot_list = []
  with open("circuit_list.csv", "w+") as file:
    for p in range(len(testVec)):

      unfoundF = [] #faults not detetected 
      foundedF = [] # faults detected 
      currentF = [] # faults detected by current test vector
      goodOutput = [] 
      badOutput = []
      if len(alldetected) == 0:
        print("\nApplying " + testVec[p] + " to the remaining " +str(len(total_multipleFault)) + " faults:")

        if len(total_multipleFault)<=1000:
          print(total_multipleFault)
      else:
        for item in total_multipleFault:
          if item not in alldetected:
            unfoundF.append(item)
        print("\nApplying " + testVec[p] + " to the remaining " +str(len(unfoundF)) + " faults:")
        if len(total_multipleFault)<=1000:
          print(*unfoundF, sep = ",")
        print("\nThe number of faults still undetected are:"+str(len(unfoundF)) )   
#===================================================================================

# This is just calculating the good circuit 
      #clear all good circuit nodes
      for node in node_list:
        node.set_value("U")
   
      line_of_val = testVec[p]
      if len(line_of_val)==0:
         break

      strindex = 0
       # Set value of good circuit input nodes
      for node in node_list:
       if node.is_input:
           if strindex > len(line_of_val)-1:
                break
           node.set_value(line_of_val[strindex])
           strindex = strindex + 1 
           
      # simulation by trying calculating each node's value in the list
      updated_count = 1 #initialize to 1 to enter while loop at least once
      iteration = 0
      while updated_count > 0:
        updated_count = 0
        iteration += 1
        for n in node_list:
            if n.value == "U":
                n.calculate_value()
                if n.value == "0" or n.value == "1":
                    updated_count +=1

        
      #print("\n--- Good circuit Simulation results: ---")
      input_list = [i.name for i in node_list if i.is_input]
      input_val = [i.value for i in node_list if i.is_input]


      output_list = [i.name for i in node_list if i.is_output]
      output_val = [i.value for i in node_list if i.is_output]
      goodOutput = [*output_val]
#===============================================================================
#Calculate all the faults

      for i in multi_list:
       faultcount = 0
       while faultcount< (2**len(i)):
            for node in node_list:
                node.set_value("U")
            strindex = 0
            for node in node_list:
                if node.is_input:
                    if strindex > len(line_of_val)-1:
                        break
                    node.set_value(line_of_val[strindex])
                    strindex = strindex + 1

            strindexs=0
            x=bin(faultcount)[2:].zfill(len(i))
            for item in node_list:
              if item in i:
                if strindexs > len(x)-1:
                  break
                item.set_value(x[strindexs])
                strindexs = strindexs + 1
            
            for node in node_list:
                  if node.value == "U":
                     node.calculate_value()

        
            fault_input_list = [i.name for i in node_list if i.is_input]
            fault_input_val = [i.value for i in node_list if i.is_input]


            fault_output_list = [i.name for i in node_list if i.is_output]
            fault_output_val = [i.value for i in node_list if i.is_output]
            badOutput = [*fault_output_val]

            if goodOutput == badOutput:
                #unfoundF.append(node_list[i].name + "-" + str(node_list[i].value))
                pass
            else:
              comb_list=[]
              for item in i:
                comb_list.append(item.name+"-"+item.value)
              #foundedF.append(node_list[i].name + "-" + str(node_list[i].value))
              foundedF.append(comb_list)

            faultcount += 1
#===================================================================================   
      #currentF = m - foundedF
      for item in foundedF:
        if item not in alldrep:
          currentF.append(item)

      print("\nThe test vector " + testVec[p] + " detects " + str(len(currentF)) + " faults")
      if len(total_multipleFault)<=1000:         
        print (testVec[p], end ="")
        print (":", end="")
        print (*currentF, sep = ",")

      print("\n******************************************************************")

      alldrep.extend(foundedF)
      alldetected.extend(currentF) 

      if p%10 == 0:
        D1 = len(alldetected)
        D2 = len(unfoundF)
        faults = D1+D2
        per_plot = (D1/faults)
        percentage = "{:.2%}".format(per_plot)


print("\n-------------------------------------------------------------------")
print("\n Percentage of multi-faults covered by LFSR")
print(percentage)

print(f"Finished - bye!")