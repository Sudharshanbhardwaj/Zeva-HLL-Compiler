from lexer import *

def main():

    text = open("test_cases/test2.zeva","r").read()
    # text = "2 + 3 "

    lexer = Lexer(text)
    Token = lexer.get_token()
    k=open("Output.txt","w")
  
    while Token.type != EOF:
        # print(Token.value, Token.type)
        k.write(Token.type)
        k.write("\n")
        Token = lexer.get_token()
    print(Token.value, Token.type)         # to check EOF

main()