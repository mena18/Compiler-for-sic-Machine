from includes.lexical import Token,Basic

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
        self.middle = assstat(tokens[0],tokens[1],tokens[2:])


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
        if(left.type!='identifier' or middle.desc!='='):
            raise Exception("Syntax error in line {}\nnot valid statement".format(left.line));
        self.right=expression(right).middle;





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
        if(len(tokens)==0):
            raise Exception("Syntax error expression can't be empty ");


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
    def __init__(self, infix):
        self.type="if_expression"
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
        sep = Token.find(infix,Basic.comparison)
        self.middle = infix[sep];
        self.left  = expression(infix[0:sep]).middle
        self.right = expression(infix[sep+1:]).middle
