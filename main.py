class Basic:
    keyword = ['if', 'for', 'while']
    comparison = ["==",">","<","<=","!=",'>=']
    operator = ['+', '-', '*', '/', '%', '^', '=','&','|' ,'==', '>', '<','!', '++', '--', '+=','!=', '-=','&&','||','>=','<=']
    delimiter = {
    '(':"open",
    ')':"close",
    '[':"open",
    ']':"close",
    '{':"open",
    '}':"close",
    ';':'end'
          }

class Token:
    total_counter=0;
    counter=0;
    type = ''
    desc = ''
    tokens = []

    def __init__(self, word,type=""):
        self.desc = word
        self.counter=Token.total_counter
        Token.total_counter+=1;
        if(type!=""):
            self.type=type;
        elif word in Basic.keyword:
            self.type = 'keyword'
        elif word in Basic.operator:
            self.type = 'operator'
        elif word in Basic.delimiter:
            self.type = Basic.delimiter[word]
        elif word.isdigit():
            self.type = 'number'
        elif Token.isIdentifier(word):
            self.type = 'identifier'
        else:
            # IDENTIFIER ERROR .. FIRST DIGIT IS NUMBER | USING KEYWORD | USING OPERATOR | USING DELIMITER
            print('Error')
            exit()

    def createTokens(code):
        word = ''
        for char in code:
            if char in Basic.operator or char in Basic.delimiter or char==' ':
                if(len(Token.tokens)>0 and word=="" and (Token.tokens[-1].desc+char) in Basic.operator):
                    Token.tokens[-1].desc+=char;
                    continue;
                if word != '':
                    Token.tokens.append(Token(word.strip()))
                if char!=' ':
                    Token.tokens.append(Token(char))
                word = ''
                continue
            word += char
        if(word):
            Token.tokens.append(Token(word.strip()))

    def isIdentifier(id):
        if id in Basic.keyword:
            return 0
        if id[0].isdigit():
            return 0
        for char in id:
            if char in Basic.operator or char in Basic.delimiter:
                return 0
        return 1


    def seperate(tokens,s):
        if(s==';'):
            for index,token in enumerate(tokens):
                if(token.desc==";"):
                    if(index==len(tokens)-1):
                        return tokens[:-1],[]
                    return tokens[:index],tokens[index+1:]

            print("ERROR ; not found");
            exit();
        elif(s=='}'):
            left,next = Token.bracket_end(tokens,'(',')')
            right,next2 = Token.bracket_end(tokens[next:],'{','}')

            if(next2 >= len(tokens[next:])):
                return left,right,[]
            return left,right,tokens[next+next2:]

    def bracket_end(tokens,op,clo):
        c=0;
        for index,token in enumerate(tokens):
            if(token.desc==op):c+=1
            if(token.desc==clo):c-=1
            if(c==0):
                return tokens[1:index],index+1
        print("ERROR END of Bracket not found")
        exit();

    def full_delimiter_body(self):
        left,next = self.bracket_end('(',')')
        right,next2 = Token.tokens[next].bracket_end('{','}')

        return left,right

    # static function
    def find(arr,find):
        index=0;
        for i in arr:
            if(i.desc in find):
                return index;
            index+=1;
        return 0;

    def print_all(tokens):
        for i in tokens:
            if(i.desc==';'):
                print(';')
            else:
                print(i,end="")
        print()

    def __str__(self):
        return self.desc


class compstat:
    type=""
    desc=""
    left=None
    right=None


    def __init__(self,tokens):
        self.type="compstat"
        tok = tokens[0];


        if(tok.desc=='if'):
            left,right,cont = Token.seperate(tokens[1:],'}');
            self.desc="if_comp";
            self.left = if_statement(left,right)
            if(cont):
                self.right = compstat(cont);

        elif(tok.desc=='while'):
            left,right,cont = Token.seperate(tokens[1:],'}');
            self.desc="while_comp";
            self.left = while_statement(left,right)
            if(cont):
                self.right = compstat(cont);

        elif(tok.desc=='for'):
            left,right,cont = Token.seperate(tokens[1:],'}');
            self.desc="for_comp";
            self.left = loop_statement(left,right)
            if(cont):
                self.right = compstat(cont);

        else:
            left,right = Token.seperate(tokens,';');
            self.desc = "stat_comp"
            self.left = stat(left)
            if(right):
                self.right = compstat(right)


    def __str__(self):
        return (self.type)

class stat:
    type=""
    desc=""
    left=None
    middle=None
    right=None

    def __init__(self,tokens):
        self.type="stat"
        self.desc="assignment"
        self.middle = assstat(tokens[0],'=',tokens[2:])


class assstat:
    type=""
    desc=""
    left=None
    middle=None
    right=None

    def __init__(self,left,middle,right):
        self.type="assstat"
        self.left=left;
        self.middle=middle;
        self.desc="id_exp";
        self.right=expression(right).middle;


def execute(head):
    if(head.type=='compstat'):
        execute(head.left)
        if(head.right!=None):
            execute(head.right)

    elif(head.type=='stat'):
        execute(head.middle)

    elif(head.type=='assstat'):
        left=str(head.left)
        right=str(head.right)
        if(head.desc=='id_num'):
            assembler.f_id_num(left,right)
        elif(head.desc=='id_id'):
            assembler.f_id_id(left,right)
        elif(head.desc=="id_exp"):
            ex=assembler.expression(head.right)
            assembler.f_id_id(left,ex)

    elif(head.type=="if_statement"):
        execute(head.left) # the expression
        execute(head.right);    # the body of loop
        print(head.left.loop_name,end="\n") # the place to jump in for loop

    elif(head.type=='if_expression'):
        left = assembler.expression(head.left)
        right = assembler.expression(head.right)
        assembler.compare_expression(left,str(head.middle),right,head.loop_name);


    elif(head.type=="while_statement"):
        execute(head.left) # the expression
        execute(head.right);    # the body of loop
        print("\tJ\t{}".format(head.left.start_loop))
        print(head.left.end_loop,end="\n") # the place to jump in for loop


    elif(head.type=='while_expression'):
        print(head.start_loop,end="")
        left = assembler.expression(head.left)
        right = assembler.expression(head.right)

        assembler.compare_expression(left,str(head.middle),right,head.end_loop);


class assembler:
    identifiers = {};
    reserved_words=[];
    words=[];
    counter=1;

    def declare(a):
        if(a not in assembler.identifiers):
            assembler.identifiers[a] = "V_"+a
            assembler.reserved_words.append("{}\tRESW\t1".format("V_"+a))

    def word(value):
        if(value not in assembler.identifiers):
            assembler.identifiers[value] = "N_"+value
            assembler.words.append("{}\tWORD\t{}".format("N_"+value,value))

    def loop_name():
        assembler.counter+=1;
        return "LOOP_"+str(assembler.counter-1)

    def f_id_num(a,b):
        assembler.declare(a);
        assembler.word(b);
        print("\t"+"LDA"+"\t"+assembler.identifiers[b])
        print("\t"+"STA"+"\t"+assembler.identifiers[a])

    def f_id_id(a,b):
        assembler.declare(a);
        print("\t"+"LDA"+"\t"+assembler.identifiers[b])
        print("\t"+"STA"+"\t"+assembler.identifiers[a])

    def expression(postfix):
        stack=[]
        for token in postfix:
            if(token.type in ("identifier",'number')):
                stack.append(token)
            elif(token.type=="operator"):
                a = stack.pop()
                b = stack.pop()
                ans = assembler.sub_exp(b,token,a);
                if(type(ans)!=Token):
                    ans = Token(ans,type="identifier")
                stack.append(ans)

        last = stack[-1];

        if(last.desc not in assembler.identifiers):
            if(last.type=='identifier'):
                assembler.declare(stack[-1].desc)
            else:
                assembler.word(stack[-1].desc)
        return str(stack[-1]);

    def sub_exp(a,operator,b):
        if(a.type=="number"):
            assembler.word(a.desc)
        if(b.type=="number"):
            assembler.word(b.desc)

        a=str(a);operator=str(operator);b=str(b);
        exp = a+operator+b
        """ check in expression already evaluated """
        if(exp in assembler.identifiers):
            return exp;
        operators = {'+':"ADD",'-':"SUB",'*':"MUL",'/':"DIV"}
        assembler.declare(exp)
        if(operator=='^'):
            loop = assembler.loop_name()
            assembler.word('1');
            assembler.word('0');

            print("\tLDA\tN_1")
            print("\tLDX\tN_0")
            print(loop+"\t"+"MUL\t"+assembler.identifiers[a])
            print("\t"+"TIX\t"+assembler.identifiers[b])
            print("\t"+"JLT\t"+loop)
            return exp;


        print("\t"+"LDA"+"\t"+assembler.identifiers[a])
        print("\t"+operators[operator]+"\t"+assembler.identifiers[b])
        print("\t"+"STA"+"\t"+assembler.identifiers[exp])
        return exp;

    def compare_expression(left,middle,right,loop_name):
        print("\tLDA\t{}".format(assembler.identifiers[left]))
        print("\tCOMP\t{}".format(assembler.identifiers[right]))
        if(middle=='=='):
            print("\tJLT\t{}".format(loop_name))
            print("\tJGT\t{}".format(loop_name))
        elif(middle==">"):
            print("\tJLT\t{}".format(loop_name))
            print("\tJEQ\t{}".format(loop_name))
        elif(middle=="<"):
            print("\tJGT\t{}".format(loop_name))
            print("\tJEQ\t{}".format(loop_name))
        elif(middle=="!="):
            print("\tJEQ\t{}".format(loop_name))
        elif(middle==">="):
            print("\tJLT\t{}".format(loop_name))
        elif(middle=="<="):
            print("\tJGT\t{}".format(loop_name))






class expression:
    type="expression"
    middle=[]
    priority = {
    "(":0,
    "+":1,
    "-":1,
    "*":2,
    "/":2,
    "^":3
    }
    def __init__(self,tokens):
        self.type="expression"
        stack = []
        postfix = []
        for token in tokens:
            if(token.type in ("identifier",'number')):
                postfix.append(token)
            elif(token.type == 'open'):
                stack.append(token)
            elif(token.type=="close"):
                while(len(stack)>0):
                    c=stack.pop()
                    if(c.type=="open"):
                        break;
                    postfix.append(c)

            elif(token.type=="operator"):
                while(len(stack)>0):
                    if(expression.priority[stack[-1].desc]>=expression.priority[token.desc]):
                        c = stack.pop()
                        postfix.append(c)
                    else:
                        break;
                stack.append(token)
        while(len(stack)>0):
            c=stack.pop();
            postfix.append(c)

        #for i in postfix:
        #    self.middle.append(str(i))
        self.middle = postfix


class if_statement:
    type=""
    desc=""
    left=None
    right=None

    def __init__(self,left,right):
        self.type="if_statement"
        self.left = if_expression(left);
        self.right = compstat(right);


class while_statement:
    type=""
    desc=""
    left=None
    right=None

    def __init__(self,left,right):
        self.type="while_statement"
        self.left = while_expression(left);
        self.right = compstat(right);



class if_expression:
    type=""
    desc=""
    left=""
    right=""
    loop_name=""
    middle=""
    def __init__(self,infix):
        self.type="if_expression"
        self.loop_name = assembler.loop_name()
        sep = Token.find(infix,Basic.comparison)
        self.middle = infix[sep];
        self.left  = expression(infix[0:sep]).middle
        self.right = expression(infix[sep+1:]).middle

class while_expression:
    type=""
    desc=""
    left=""
    right=""
    start_loop = ""
    end_loop = ""
    middle=""
    def __init__(self,infix):
        self.type="while_expression"
        self.start_loop = assembler.loop_name()
        self.end_loop = assembler.loop_name()
        sep = Token.find(infix,Basic.comparison)
        self.middle = infix[sep];
        self.left  = expression(infix[0:sep]).middle
        self.right = expression(infix[sep+1:]).middle



class loop_expression:
    def __init__(self,infix):
        print("loop expression not completed yet");


class loop_statement:
    type=""
    desc=""
    left=None
    right=None

    def __init__(self,left,right):
        self.type="for_statement"




def main():
    read = open("read.txt","r").read();
    read = read.replace("\n","");
    read = read.replace("\t","");
    Token.createTokens(read)

    head = compstat(Token.tokens);
    execute(head)
    print()
    [print(i) for i in assembler.words]
    [print(i) for i in assembler.reserved_words]

def main2():
    read = open("read.txt","r").read();
    read = read.replace("\n","");

    Token.createTokens(read)
    for i in Token.tokens:
        if(i.desc==';'):
            print(';')
        else:
            print(i,end="")
    print("hello")
    ex = expression(Token.tokens);
    for i in ex.middle:
        print(i)

main()
