class Basic:
    keyword = ['int', 'if', 'for', 'while']
    operator = ['+', '-', '*', '/', '%', '^', '=','&','|' ,'==', '>', '<', '++', '--', '+=', '-=','&&','||']
    delimiter = ['(', ')', '[', ']', '{', '}', ';']

class Token:
    total_counter=0;
    counter=0;
    type = ''
    desc = ''
    tokens = []

    def __init__(self, word):
        self.desc = word
        self.counter=Token.total_counter
        Token.total_counter+=1;
        if word in Basic.keyword:
            self.type = 'keyword'
        elif word in Basic.operator:
            self.type = 'operator'
        elif word in Basic.delimiter:
            self.type = 'delimiter'
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


    def __str__(self):
        return self.desc


Token.createTokens("for(int i=0;i<5;i++){if(a==b){print(hello world)}}")

one = Token.tokens[16];
for i in one.delimiter_end():
    print(i)
