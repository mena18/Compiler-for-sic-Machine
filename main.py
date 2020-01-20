import os
from includes.lexical import Token
from includes.parsing import compstat
from includes.generator import execute,generator
from includes.assembler import Instruction,passes

def main():
    print("-"*100)

    read = open("read.txt",'r').read();
    read = read.replace("\t","");
    Token.createTokens(read)

    try:
        os.mkdir("output")
    except:
        pass
    generator.file_writer=open('output/output.txt','w')
    try:
        head = compstat(Token.tokens);
        generator.file_writer.write("program\tSTART\t0\n")
        execute(head)
        generator.pr("")
        [generator.pr(i) for i in generator.words]
        [generator.pr(i) for i in generator.reserved_words]
        generator.file_writer.write("\tEND\t0");
        generator.file_writer.close()
        passes('../output/output');
    except Exception as e:
        #raise
        print(e)

    print("-"*100)

if __name__ == '__main__':
    main()
