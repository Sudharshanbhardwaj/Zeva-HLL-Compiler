        				                	 **ZEVA Syntax**

Basic Types (numbers, booleans, strings):    

	Declaration format: var <type> 
	
	var <type>  x= <data>; @ we have to always end a statement with a semicolon(;)
	
	<type> :=int @integer (1,2)
	
	|str @string (“compiler”)
	
	|bool @boolean (true,false)

	var str s;
	
	s.substr(start,length); for string slicing 
	
	var str c;

	s.con(c); @for concatenating two strings we have to give as string_1.con(string2)

	zout (x);	 @prints x;

unary-operator ::= 

		   ++ @increment by 1
                   | — @ decrement by 1

binary-operator ::= 	
			
   			+ @addition
		        | - @subtraction	  
		        | * @multiplication
		        | / @division
		        | % @remainder
	  		| @ power
		        |== @comparision of identifier with the required  value
		        |<  @less than symbol
		        |>  @greater than symbol
		        |<= @less than equal symbol
	            |>= @greater than symbol
		        |!= @not equal

@ single line comment 

Identifiers: alphanumeric
             
Compound Types :

              tuple  <Identifier>=(data); @they are immutable
	 
              list   <Identifier>=();      @ all the three have 0 based indexing
!!!
             For both list some basic operations are applied
	     
             <Identifier>.add(data); @adds data to the compound type
	     
             <Identifier>.delete; @removes the last data of the compound type
	     
             l_size=<Identifier>.size;
	     
             var <type> a=<identifier>[1]; @ for accessing the second element in the array or tuple here type is the type
	     
             <Identifier>.front; @ gives the first element of the compound type
	     
             <Identifier>.rear; @giving the last element of the compound type
	     
!!!
          
Conditionals : (for every individual block of conditional statement it ends with a semi colon)

            if (@condition)
            begin
                 @code
            end
            elif(@condition)
            begin
                 @code
            end
            else
            begin
                 @code
            end;
	    
@nested if statements 

        if(@condition) 
            begin
                 @code 
                  if(@condition2)
                  begin
                        @code
                   end;
            elif(@condition)
				begin
					@code
				end
            else
				begin
					@code
				end

        end;

Loops : (For every individual block of while ends with a semi colon)

           while(condition)
          	begin
                 @code
            end;
	    
  @ we can also use nested loops
  
         while(condition)
          begin
                 @code
                  while(condition)
                  begin
                         @code
                  end

          end;
	  

	     
Functions : (For everyindividual loack function ends with a semi colon)
           
	   return; @ returns the element given there
           func myfunction(arguments) @example myfunction(int x,int y)
           begin
                 @function body
             return data;
            end;
            myfunction(x,y); @ for calling function again anywhere after the function declaration


Closures : 

             func myfunction(int x,int y)
             begin 
                   var x=5;
                   var y= 6;
                   func myFunction(int a)
                   begin
                         var a=7;
                        @function body
                        var int output=x;
						x=y+a;
                        return output;
                   end;
                   return myFunction;
              end;
	      
Mutable variables : 

             var <type> | lists @ these are mutable variables
	     
Exceptions : (Each exception statement itself is in a block and ends with a Semicolon)

            begin 
			  try  
                @ try the case 
                @if fails throw the exception

              except(exception)
               
                @do the code given here
            end;
             

BNF

   <program> ::= <statement>*

	<statement> ::= <variable_declaration>| <assignment> | <conditional> | <loop> | <function> | <try-catch>|<print_statement>|<mutable_variable_declaration>
	
	 <variable_declaration> ::= {‘var:’ <type> <identifier> ‘=’ <expression> ‘;’} +  {‘tuple’ <identifier> ‘=’ <expression> ‘;’} + {‘array’ <identifier> ‘=’ <expression> ‘;’} + {‘tuple’ <identifier> ‘=’ <expression> ‘;’}
	
	<assignment> ::= <identifier> "=" <expression> ‘;’
	
	<conditional> ::= {{"if" <expression> "begin" <statement> “end”}* "else" “begin” <statement> “end”} +
			{"if" <expression> "begin" <statement> “end” {"elif" “begin” <statement> “end”}* "else" “begin” <statement> “end”}
	
	<loop> ::= "while" <expression> “begin” <statement> “end”
	 
	<function> ::= <type>|tuple|list|array|void  <identifier> "(" <identifier-list>? ")" "begin" <statement>* “return” <expression> “;” "end" | <function>
	
	<try-except> ::= "try" "begin" <statement>* "end" "except" "(" <identifier> ")" "begin" <statement>* "end"
	
	<print_statement> ::= 'zout' '(' expression ');'
	
	<mutable_variable_declaration> ::= “var:”  <type>| “list” <identifier> '=' <expression> ';' 
	
	<expression> ::= <number> | <boolean> | <string> |unary_operation| <identifier> | "(" <expression> ")"
	|< function_call> | <list_operation> | <array_operation> |< member_access>|<term> { <binary_operator> <term> }*
	
	<unary-operator> ::= ++ 
	                   | — 
	                   | & 
	                   | - r
	                   | ~ 
	                   | ! 
	
	<binary-operator> ::= +
			        | -
			        | *
			        | /
			        | %
			        |==
			        |<
			        |>
			        |<=
		                     |>=
	
	<term> ::= <factor> { <binary_operator>  <factor> }*
	
	<factor> ::= <number> | <boolean> | <string> | <identifier> | "(" <expression> ")"
	
	<identifier-list> ::= <identifier> { "," <identifier> }*
	
	<list_operation> ::=< identifier> '.' ('add' '(' expression ')' | 'size' '(' ')' | '[' expression ‘]’ | 'head' '(' ')' | 'tail' '(' ')') 
	
	<array_operation> ::= <identifier> '.' ('add' '(' expression ')' | 'size' '(' ')' |'[' expression ‘]’ | 'head' '(' ')' | 'tail' '(' ')') 
	
	<member_access> ::= <identifier> '.' <identifier>
	
	<identifier> ::= <letter> { <letter> | <digit> }*
	
	<number> ::= <digit>+
	
	<boolean> ::= "true" | "false"
	
	<string> ::= '"' { <character> }* '"'
	
	<letter> ::= "a" | "b" | "c" | ... | "z" | "A" | "B" | "C" | ... | "Z"
	
	<digit> ::= "0" | "1" | "2" | ... | "9"
	
	<character> ::= <letter> | <digit> | <special-character>
	
	<special-character> ::= " " | "!" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "," | "-" | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "\\" | "]" | "^" | "_" | "`" | "{" | "|" | "}" | "~"


Context Free Grammar

	Basic Types:

	  	S -> D=K
	   	D -> varI|id
	    	I ->int|bool|string|char|T.F
	    	K -> [a-z]*|true|false|[0-9]*|id.T
	     	id ->[a-z]+[_|[0-9]|[a-z]]*
	     	T -> con(id)|substring([0-9]+, [0-9]*)
	      	int ->[0-9]+
		bool ->true|false
		string ->[a-z]+[[0-9]|[a-z]]*
		char ->a|b|....|z

	unary operator:
	 
	  	S -> I++ | I--;
	 	I ->[a-z]+[_|[0-9]|[a-z]]*
 

 	Binary Operator :
 
		 S ->IOI
		 I ->[a-z]+[_|[0-9]|[a-z]]*
		 O -> +|-|*|/|%|==|<|>|>=|<=|!=
 
 	Compound types :
  
		 S -> TI=(D)
		 T ->tuple|list
		 I ->[a-z]+[_|[0-9]|[a-z]]*
		 D -> [K [,K]]
		 K ->int|bool|string|char
		 int ->[0-9]+
		 bool ->true|false
		 string ->[a-z]+[[0-9]|[a-z]]*
		 char ->a|b|....|z
   
 	Compound type Operations : 
  
		  S ->IL|M
		  M ->I=S
		  L ->.add(K)|.T()
		  T ->size|delete|front|rear
		  I ->[a-z]+[_|[0-9]|[a-z]]*
		  K ->int|bool|string|char
		  int ->[0-9]+
		  bool ->true|false
    
    	Conditionals :

	 	  stmt -> matched_stmt | open_stmt
  		  matched_stmt -> if expr begin matched_stmt end else begin matched_stmt end
	 	  open_stmt -> if expr begin stmt end | if expr begin open_smt else begin open_stmt end 
     		  expr -> ( bool | id == K )
	 	  id ->[a-z]+[_|[0-9]|[a-z]]*
	 	  K ->int|bool|string|char
		  int ->[0-9]+
		  bool ->true|false
    		  string ->[a-z]+[[0-9]|[a-z]]*
		  char ->a|b|....|z
    
         Exceptions:

	  	  S -> try begin main end excpet begin main end
     
