import os,shutil
from includes.lexical import Token
from includes.parsing import compstat
from includes.generator import execute,generator
from includes.assembler import Instruction,passes

def main():
    print("-"*100)

    try:
        for filename in os.listdir('output'):
            file_path = os.path.join('output', filename)
            os.unlink(file_path)
    except:
        os.mkdir("output")

    read = open("read.txt",'r').read();
    read = read.replace("\t","");
    Token.createTokens(read)


    generator.file_writer=open('output/output.txt','w')
    try:
        head = compstat(Token.tokens);
        generator.file_writer.write("program\tSTART\t0\n")
        execute(head)
        generator.pr("")
        [generator.pr(i) for i in generator.words]
        [generator.pr("{}\tRESW\t1".format(i)) for i in generator.reserved_words if(i) in generator.all_loaded]
        #[print(i,generator.all_loaded[i]) for i in generator.all_loaded]
        generator.file_writer.write("\tEND\t0");
        generator.file_writer.close()
        passes('../output/output');


        here = os.path.dirname(os.path.realpath(__file__))
        here = os.path.join(here,'output')
        here = os.path.join(here,'output.html')
        os.system('"'+here+'"')
    except Exception as e:
        #raise
        print(e)

    print("-"*100)


if __name__ == '__main__':
    main()
