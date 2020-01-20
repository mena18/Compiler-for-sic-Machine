from includes.lexical import Token

class generator:
    identifiers = {};
    reserved_words=[];
    words=[];
    all_loaded={};
    counter=1;
    last_loaded=""
    file_writer=""

    def pr(s,new_line="\n"):
        print(s+new_line,end="")
        generator.file_writer.write(s+new_line)

    def load(var,ignore=0):
        if(generator.last_loaded==var and ignore==0):
            return ;
        if(var not in generator.identifiers):
            raise Exception("Variable {} Not defined".format(var));
        generator.pr("\t"+"LDA"+"\t"+generator.identifiers[var])
        generator.last_loaded = var;
        generator.all_loaded[generator.identifiers[var]] = 1

    def store(var):
        generator.declare(var)
        generator.pr("\t"+"STA"+"\t"+generator.identifiers[var])
        generator.last_loaded = var;
        generator.all_loaded[generator.identifiers[var]] = 1


    def declare(a):
        if(a not in generator.identifiers):
            generator.identifiers[a] = "V_"+a
            generator.reserved_words.append("V_"+a)

    def word(value):
        if(value not in generator.identifiers):
            generator.identifiers[value] = "N_"+value
            generator.words.append("{}\tWORD\t{}".format("N_"+value,value))

    def loop_name():
        generator.counter+=1;
        return "LOOP_"+str(generator.counter-1)

    def f_id_id(a,b):
        generator.declare(a);
        generator.load(b);
        generator.store(a);

    def expression(postfix):

        for token in postfix:
            if token.type=="number":
                generator.word(token.desc)
            if(token.type=='identifier' and str(token) not in generator.identifiers):
                raise Exception("variable {} not defined in line {}".format(token.desc,token.line));

        if(len(postfix)==1):
            return str(postfix[0]);





        stack=[]
        last_expression=""
        for token in postfix:
            if(token.type in ("identifier",'number')):
                stack.append(token)
            elif(token.type=="operator"):
                a = stack.pop()
                b = stack.pop()

                if(  not((str(b)==last_expression and token.desc!='^') or (str(a)==last_expression and token.desc in ['+','*'] )  or last_expression=="" ) ):
                    generator.store(last_expression);

                ans = generator.sub_exp(b, token, a);
                last_expression = str(ans)
                if(type(ans)!=Token):
                    ans = Token(ans,-1, type="identifier")
                stack.append(ans)
        last = stack[-1]
        if(last.desc not in generator.identifiers):
            if(last.type=='identifier'):
                generator.declare(stack[-1].desc)
            else:
                generator.word(stack[-1].desc)
        return str(stack[-1]);

    def sub_exp(a,operator,b):
        a=str(a);operator=str(operator);b=str(b);
        exp = a+operator+b

        operators = {'+':"ADD",'-':"SUB",'*':"MUL",'/':"DIV"}

        if(operator=='^'):
            loop = generator.loop_name()
            generator.word('1');
            generator.word('0');

            generator.load("1");
            generator.pr("\tLDX\tN_0")
            generator.pr(loop+"\t"+"MUL\t"+generator.identifiers[a])
            generator.pr("\t"+"TIX\t"+generator.identifiers[b])
            generator.pr("\t"+"JLT\t"+loop)
            generator.all_loaded[generator.identifiers[b]] = 1
            generator.all_loaded[generator.identifiers[a]] = 1
        else:
            if((operator=='+' or operator=='*') and generator.last_loaded == b):
                generator.pr("\t"+operators[operator]+"\t"+generator.identifiers[a])
                generator.all_loaded[generator.identifiers[a]] = 1
            else:
                generator.load(a)
                generator.pr("\t"+operators[operator]+"\t"+generator.identifiers[b])
                generator.all_loaded[generator.identifiers[b]] = 1

        generator.last_loaded = exp;
        return exp;

    def compare_expression(left,middle,right,loop_name):
        if(right not in generator.reserved_words):
            generator.store(right)
        generator.load(left,ignore=1);
        generator.pr("\tCOMP\t{}".format(generator.identifiers[right]))
        if(middle=='=='):
            generator.pr("\tJLT\t{}".format(loop_name))
            generator.pr("\tJGT\t{}".format(loop_name))
        elif(middle==">"):
            generator.pr("\tJLT\t{}".format(loop_name))
            generator.pr("\tJEQ\t{}".format(loop_name))
        elif(middle=="<"):
            generator.pr("\tJGT\t{}".format(loop_name))
            generator.pr("\tJEQ\t{}".format(loop_name))
        elif(middle=="!="):
            generator.pr("\tJEQ\t{}".format(loop_name))
        elif(middle==">="):
            generator.pr("\tJLT\t{}".format(loop_name))
        elif(middle=="<="):
            generator.pr("\tJGT\t{}".format(loop_name))



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
        ex=generator.expression(head.right)
        generator.f_id_id(left,ex)


    elif(head.type=="if_statement"):
        execute(head.left) # the expression
        execute(head.right);    # the body of loop
        generator.pr(head.left.loop_name) # the place to jump in for loop

    elif(head.type=='if_expression'):
        head.loop_name = generator.loop_name()
        left = generator.expression(head.left)
        right = generator.expression(head.right)
        generator.compare_expression(left,str(head.middle),right,head.loop_name);


    elif(head.type=="while_statement"):
        execute(head.left) # the expression
        execute(head.right);    # the body of loop
        generator.pr("\tJ\t{}".format(head.left.start_loop))
        generator.pr(head.left.end_loop) # the place to jump in for loop


    elif(head.type=='while_expression'):
        head.start_loop = generator.loop_name()
        head.end_loop = generator.loop_name()

        generator.pr(head.start_loop)
        left = generator.expression(head.left)
        right = generator.expression(head.right)

        generator.compare_expression(left,str(head.middle),right,head.end_loop);
