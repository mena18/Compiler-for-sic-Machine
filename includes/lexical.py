class Basic:
    keyword = ['if', 'for', 'while']
    comparison = ["==", ">", "<", "<=", "!=", '>=']
    operator = ['+', '-', '*', '/', '%', '^', '=', '&', '|', '==', '>', '<', '!', '++', '--', '+=', '!=', '-=', '&&',
                '||', '>=', '<=']
    delimiter = {
        '(': "open",
        ')': "close",
        '[': "open",
        ']': "close",
        '{': "open",
        '}': "close",
        ';': 'end'
    }
    error = ['!', '@', '$', '&', '~', '`']

class Token:
    total_counter = 0;
    counter = 0;
    type = ''
    desc = ''
    tokens = []
    line=-1;

    def __init__(self, word,line, type=""):
        self.desc = word
        self.counter = Token.total_counter
        Token.total_counter += 1;
        self.line = line;
        if (type != ""):
            self.type = type;
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
        code2 = Token.deleteSpaces(code)
        Token.checkCode(code2)
        code2 = Token.deleteComment(code2)
        lines=1;
        for char in code2:
            if char == '\n':
                lines+=1;
                continue;
            if char in Basic.operator or char in Basic.delimiter or char == ' ':
                if (len(Token.tokens) > 0 and word == "" and (Token.tokens[-1].desc + char) in Basic.operator):
                    Token.tokens[-1].desc += char
                    continue;
                if word != '':
                    Token.tokens.append(Token(word.strip(),lines))
                if char != ' ':
                    Token.tokens.append(Token(char,lines))
                word = ''
                continue
            word += char
        if (word):
            Token.tokens.append(Token(word.strip(),lines))
#el 2kwas , el comment, el semicolon

    def deleteSpaces(code):
        finalCode = ''
        i = 0
        length = len(code)
        while(i<length):
            if code[i] == '#':
                finalCode += code[i]
                i += 1
                while i < length and code[i] != '#':
                    finalCode += code[i]
                    i += 1
                if i >= length:
                    break
                finalCode += code[i]
                i += 1
                while i < length and code[i] == ' ' or code[i] == '\t':
                    i += 1
                continue
            finalCode += code[i]
            i += 1

        return finalCode

    def checkCode(code):
        if len(code) == 0:
            exit()
        line = 1;
        if code[0].isdigit():
            print('Syntax Error In Line  ' + str(line))
            exit()
        count = 0
        for i in range(0, len(code)):
            if code[i] == '\n':
                line += 1
            if code[i] == '#':
                count += 1
            if i != len(code) - 1 and count % 2 == 0 and code[i] == '#' and code[i+1] == ';':
                print("Syntax Error In Line  " + str(line))
                exit()
            elif i != len(code) - 1 and code[i] == ';' and code[i+1] == ';':
                print('Syntax Error In Line  ' + str(line))
                exit()
        if count % 2 != 0:
            print('Syntax Error Check Number Of "#"')
            exit()
        arr_brackets = []
        line = 1
        for char in code:
            if char == '\n':
                line += 1
            elif char == '(' or char == '[' or char == '{':
                arr_brackets.append(char)
                arr_brackets.append(line)
            elif char == ')' or char == ']' or char == '}':
                if(len(arr_brackets)==0):
                    print("Syntax Error : Can't find opening bracket for line ",line)
                    exit()
                l = arr_brackets.pop()
                brack = arr_brackets.pop()
                if( ( brack=='(' and char == ')' ) or (brack=='{' and char == '}' ) or (brack=='[' and char == ']' )    ):
                    continue
                else:
                    print("Syntax Error : closing bracket dosen't match Lines({},{})".format(l,line))
                    exit()



    def deleteComment(code):
        finalCode = ''
        flag = 1
        for i in range(0, len(code)):
            if flag == 1 and code[i] == '#':
                flag = 0
            elif flag == 0 and code[i] == '#':
                flag = 1
            if flag == 0 or code[i] == '#':
                continue
            finalCode += code[i]
        return finalCode

    def isIdentifier(id):
        if id[0].isdigit():
            return 0
        for char in id:
            if char in Basic.operator or char in Basic.delimiter or char in Basic.error:
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
            print(i.desc)
        print()

    def print_with_lines():
        for i in tokens:
            print(i.desc,i.line,sep="\t")
        print()

    def __str__(self):
        return self.desc
