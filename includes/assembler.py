table_head = """
<!DOCTYPE html>
<html>
<head>
<style>

.red{
    color:red;
}
.blue{
    color:blue;
}

table {
  align:center;
  text-align:center;
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

table td, table th {
  border: 1px solid #ddd;
  padding: 8px;
  font-size:25px;
}

.div{
	margin: auto;
  	width: 65%;
}

.height{margin-top: 150px;}

table tr:nth-child(even){background-color: #f2f2f2;}

table tr:hover {background-color: #ddd;}

table th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: center;
  background-color: white;
  color: black;
  font-size:20px;
}
</style>
</head>
<body>
<div class="height">
<div class="div" >
<table align="center">
  <tr>
    <th>Location</th>
    <th>Label</th>
    <th>Instruction</th>
    <th>operand</th>
    <th>object code</th>
  </tr>


    """
reserved_words = {
    'ADD': '18',
    'AND': '40',
    'COMP': '28',
    'DIV': '24',
    'J': '3C',
    'JEQ': '30',
    'JGT': '34',
    'JLT': '38',
    'JSUB': '48',
    'LDA': '00',
    'LDCH': '50',
    'LDL': '08',
    'LDX': '04',
    'MUL': '20',
    'OR': '44',
    'RD': 'D8',
    'RSUB': '4C',
    'STA': '0C',
    'STCH': '54',
    'STL': '14',
    'STSW': 'E8',
    'STX': '10',
    'SUB': '1C',
    'TD': 'E0',
    'TIX': '2C',
    'WD': 'DC'
}

import os

class Instruction:
    location=""
    label=""
    mnemonic = ""
    operand=""
    opcode=""
    blank=False

    def __init__(self,arr):
        self.location=""
        self.opcode=""
        self.label = arr[0]
        self.mnemonic = arr[1]
        self.operand = arr[2]
        if(self.mnemonic == self.operand and self.mnemonic==""):
            self.blank=True

    def __str__(self):
        return "\t".join([self.location,self.label,self.mnemonic,self.operand,self.opcode])

    def set_location(self,var):
        self.location = (hex(var)[2:]).rjust(4,'0')


class passes:

    def __init__(self,file_name): #constructor
        self.file_content = [] # array  of object of type instruction
        self.symbolic_table = {}
        self.location = 0
        self.program_code=[]
        self.here = os.path.dirname(os.path.abspath(__file__))
        self.file_name = os.path.join(self.here,file_name)

        f = open(self.file_name+".txt", "r")
        reading = f.read().split('\n')
        for ins in reading:
            arr = ins.split('\t')
            if(len(arr)==1 and arr[0][0:4]=="LOOP"):
                self.file_content.append(Instruction( [arr[0],"",""] ))
            elif(len(arr)==3):
                cur_instruction = Instruction(arr);
                self.file_content.append(cur_instruction)



        if(self.file_content[0].label != 'START'):
            self.location=0
        else:
            self.location = int(self.file_content[0].operand,16)

        f.close()

        self.assemble_print();

    def pass1(self):
        for instruction in self.file_content[1:-1]:



            instruction.set_location(self.location);
            #print(("-"*100)+"\n"+str(instruction)+"\n"+("-"*100))
            if(instruction.label!=""):
                self.symbolic_table[ instruction.label ] = instruction.location;


            if(instruction.blank):
                continue

            elif(instruction.mnemonic in reserved_words or instruction.mnemonic == "WORD"): #example ['LOOP','LDA','VAR']
                self.location += 3

            elif(instruction.mnemonic=="RESW"):
                self.location+=3*int(instruction.operand)

            elif(instruction.mnemonic=="RESB"):
                self.location+=int(instruction.operand)

            elif(instruction.mnemonic=="BYTE"):
                if(instruction.operand[0]=='C'):
                    self.location+=len(instruction.operand)-3
                else:
                    self.location+=1
            else:
                print("some this wrong in that line \t",instruction)
                del self;

    def pass2(self):
        for instruction in self.file_content[1:-1]:

            if(instruction.blank):
                continue

            elif (instruction.operand.find(",") > 0): # if it's indexed ['loc','label','LDA','alpha,x']
                alpha,x = instruction.operand.split(',')
                mnemonic_opcode = reserved_words[instruction.mnemonic]
                address = (hex(  int(self.symbolic_table[alpha],16) + 32768)[2:]).rjust(4,'0')
                instruction.opcode = mnemonic_opcode + address

            elif(instruction.mnemonic in reserved_words): #example ['loc','label','LDA','var']
                mnemonic_opcode = reserved_words[instruction.mnemonic]
                address=self.symbolic_table[instruction.operand]
                instruction.opcode = mnemonic_opcode + address

            elif(instruction.mnemonic == "RESW" or instruction.mnemonic == "RESB"):
                continue;

            elif(instruction.mnemonic == "WORD"):
                instruction.opcode = (hex(int(instruction.operand))[2:]).rjust(6,'0')

            elif(instruction.mnemonic == "BYTE"):

                if(instruction.operand[0]=='C'):
                    for i in instruction.operand[2:-1]: # c'eof'  ignoring c'  and '
                        instruction.opcode+=hex(ord(i))[2:]
                else:
                    instruction.opcode = instruction.operand[2:-1]
            else:
                print("some this wrong in that line \t",instruction)
                del self;


        for i in self.symbolic_table:
            print(i,self.symbolic_table[i])
        print("\n\n")
        for i in self.file_content:
            print(i)
        print("\n\n")


    def object_program(self): # geting the object program
        length = self.location - int(self.file_content[1].location,16)
        H = ["H",(self.file_content[0].label).ljust(6," ")[0:6] , self.file_content[0].operand.rjust(6,'0') , hex(length)[2:].rjust(6,'0')]
        E = ["E",self.file_content[0].operand.rjust(6,'0')]

        self.program_code.append(H)

        length=0
        T=[]
        start=0
        for instruction in self.file_content[1:-1]:
            if(length==0):
                start = instruction.location.rjust(6,'0')

            if(instruction.blank):
                continue;

            elif(instruction.opcode==''): # when we meet resw or resb
                if(length>0):
                    self.program_code.append(  ["T",start,hex(length//2)[2:].rjust(2,"0")]  +  T);
                    T=[]
                    length=0;
                continue;

            if(length+len(instruction.opcode)<=60):
                length+=len(instruction.opcode)
                T.append(instruction.opcode);
            else:
                self.program_code.append(  ["T",start,hex(length//2)[2:].rjust(2,"0")]  +  T);
                length=len(instruction.opcode)
                T=[instruction.opcode];
                start = instruction.location.rjust(6,'0')

        if(length>0):
            self.program_code.append(  ["T",start,hex(length//2)[2:].rjust(2,"0")]  +  T);
        self.program_code.append(E)

        for i in self.program_code:
            print("^".join(i))


    def span(self,op,c): # for printing table only  [ hello ->  <span class='red' >hello</span>
        color="red";
        if(c%2==1):
            color='blue';
        return '<span class="{}">{}</span>'.format(color,op)

    def print_files(self):
        symbolic_file = open(self.file_name + '_symbolicTable.txt',"w")
        for i,j in self.symbolic_table.items():
            symbolic_file.write(i+"\t"+j+"\n")

        output_file = open(self.file_name + "_output.txt","w")
        for i in self.file_content:
            output_file.write( str(i) + "\n")

        object_program_file = open(self.file_name + "_object_program.txt","w")
        for i in self.program_code:
            object_program_file.write("^".join(i) + "\n")


        html_file = open(self.file_name + ".html","w")
        html_file.write(table_head);
        for instruction in self.file_content:
            html_file.write("<tr>")
            html_file.write("<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>".format(
            instruction.location,
            instruction.label,
            instruction.mnemonic,
            instruction.operand,
            instruction.opcode,
            ));
            html_file.write("</tr>")
        html_file.write("</table>")


        for line in self.program_code:
            color=0
            html_file.write("<h2>")
            cont=[]
            for op in line:
                cont.append(self.span(op,color))
                color+=1
            html_file.write("^".join(cont))
            html_file.write("</h2>")


        html_file.write("</body></html>");



    def assemble_print(self):
        self.pass1()
        self.pass2()
        self.object_program()
        self.print_files()
