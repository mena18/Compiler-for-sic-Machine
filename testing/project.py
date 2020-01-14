class Basic:
    keyword = ['if', 'for', 'while']
    operator = ['+', '-', '*', '/', '%', '^', '=','&','|' ,'==', '>', '<', '++', '--', '+=', '-=','&&','||']
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

    def delimiter_end(self):
        open = self.desc;
        close="}"
        if(open=='('):close=")"
        c=1;
        for i in Token.tokens[self.counter+1:]:
            if(i.desc==open):c+=1
            if(i.desc==close):c-=1
            if(c==0):return Token.tokens[self.counter+1:i.counter]

        return 0;

    # static function
    def find(arr,find):
        index=0;
        for i in arr:
            if(i.desc==find):
                return index;
            index+=1;
        return 0;

    def print_all():
        for i in Token.tokens:
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
    middle=None
    right=None


    def __init__(self,tokens):
        fir_semi = Token.find(tokens,';')
        self.type="compstat"
        if(fir_semi==len(tokens)-1):
            self.desc = "stat"
            self.left=None;
            self.middle=stat(tokens[:-1]);
            self.right=None;
        else:
            self.desc = "compstat"
            self.left = stat(tokens[0:fir_semi])
            self.right = compstat(tokens[fir_semi+1:])


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
        if(len(right)>1):
            self.desc="id_exp";
            self.right=expression(right).middle;
        elif(right.type=="number"):
            self.desc="id_num"
            self.right=right;
        elif(right.type=="identifier"):
            self.desc="id_id"
            self.right=right;




def execute(head):
    if(head.type=='compstat'):
        if(head.desc=='compstat'):
            execute(head.left)
            execute(head.right)
        elif(head.desc=='stat'):
            execute(head.middle)

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

class expression:
    type="expression"
    middle=[]
    priority = {
    "(":0,
    "+":1,
    "-":1,
    "*":1,
    "/":1,
    "^":2
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

def main():
    read = open("read.txt","r").read();
    read = read.replace("\n","");
    Token.createTokens(read)
    Token.print_all();

    head = compstat(Token.tokens);
    execute(head)
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
