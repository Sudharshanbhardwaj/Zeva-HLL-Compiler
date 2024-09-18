from AST import *

class WatGenerator:
    def init(self):
        self.wat_code = []
        self.indent = 0
        self.current_loop_label = None  # Manage current loop for breaks

    def visit_Start(self, node):
        for part in node.parts:
            self.visit(part)
        # self.visit(node.parts)

    def generate_wat(self, node, filename):
        self.visit(node)
        with open(filename, 'w') as file:
            file.write('\n'.join(self.wat_code))

    def visit(self, node):
        method_name = 'visit_' + type(node).name
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).name} method')

    def visit_IntNum(self, node):
        self.wat_code.append(f'{self.indent_str()}i32.const {node.value}')

    def visit_FloatNum(self, node):
        self.wat_code.append(f'{self.indent_str()}f32.const {node.value}')

    def visit_String(self, node):
        # Assuming functionality to handle strings
        pass

    def visit_Block(self, node):
        for stmt in node.stmts:
            self.visit(stmt)

    def visit_UnaryMinus(self, node):
        self.visit(node.expr)
        self.wat_code.append(f'{self.indent_str()}i32.const -1')
        self.wat_code.append(f'{self.indent_str()}i32.mul')

    # def visit_BinExpr(self, node):
    #     self.visit(node.left)
    #     self.visit(node.right)
    #     ops = {"+": "add", "-": "sub", "*": "mul", "/": "div_s"}
    #     if node.op in ops:
    # #         self.wat_code.append(f'{self.indent_str()}i32.{ops[node.op]}')
    # def visit_BinExpr(self, node):
    #     self.visit(node.left)
    #     self.visit(node.right)
    #     ops = {
    #         "+": "add", "-": "sub", "*": "mul", "/": "div_s", "%": "mod",
    #         ">=": "ge_s", "<=": "le_s", "==": "eq", "!=": "ne"
    #     }
    #     if node.op in ops:
    #         self.wat_code.append(f'{self.indent_str()}i32.{ops[node.op]}')

    # def visit_BinExpr(self, node):
    #     # Assuming node.left and node.right are variable names directly or are simple nodes
    #     # that can be resolved to variable names directly
    #     if hasattr(node.left, 'name'):
    #         self.wat_code.append(f'{self.indent_str()}local.get ${node.left.name}')
    #     else:
    #         self.visit(node.left)

    #     if hasattr(node.right, 'name'):
    #         self.wat_code.append(f'{self.indent_str()}local.get ${node.right.name}')
    #     else:
    #         self.visit(node.right)

    #     # Operations dictionary maps the node's op attribute to WASM instructions
    #     ops = {
    #         "+": "add", "-": "sub", "*": "mul", "/": "div_s", "%": "rem_s",
    #         ">=": "ge_s", "<=": "le_s", "==": "eq", "!=": "ne"
    #     }
        
    #     if node.op in ops:
    #         self.wat_code.append(f'{self.indent_str()}i32.{ops[node.op]}')
    #         # self.wat_code.append(f'{self.indent_str()}drop')
    def visit_BinExpr(self, node):
        # Visit left and right nodes to ensure all nested expressions are handled
        self.visit(node.left)
        self.visit(node.right)
        
        # Dictionary mapping higher-level operations to WAT instructions
        ops = {
            "+": "add", "-": "sub", "*": "mul", "/": "div_s", "%": "rem_s",
            ">=": "ge_s", "<=": "le_s", "==": "eq", "!=": "ne"
        }
        
        # Append the operation code
        if node.op in ops:
            self.wat_code.append(f'    i32.{ops[node.op]}')
            # self.wat_code.append('    drop')  # Follow each operation with a drop

    # Additional necessary parts of the visitor pattern
    def visit_Variable(self, node):
        self.wat_code.append(f'    local.get ${node.name}')

    def visit_Number(self, node):
        self.wat_code.append(f'    i32.const {node.value}')        
    # def visit_Id(self, node):
    #     self.wat_code.append(f'{self.indent_str()}get_local ${node.id}')

    # def visit_AssignExpr(self, node):
    #     self.visit(node.value)
    #     self.wat_code.append(f'{self.indent_str()}set_local ${node.id.id}')
    def visit_AssignExpr(self, node):
        self.visit(node.value)
        self.wat_code.append(f'{self.indent_str()}local.set ${node.id.id}')

    def visit_Id(self, node):
        self.wat_code.append(f'{self.indent_str()}local.get ${node.id}')
        
    def initialize_locals(self, variables):
        for var, value in variables.items():
            self.wat_code.append(f'(local ${var} i32)')
            self.wat_code.append(f'i32.const {value}')
            self.wat_code.append(f'local.set ${var}')
    # def visit_ForLoop(self, node):
    #     self.current_loop_label = f"loop_{node.id.id}"
    #     self.wat_code.append(f"(block (loop (label ${self.current_loop_label})")
    #     self.visit(node.range)
    #     self.visit(node.stmt)
    #     self.wat_code.append(f"(br ${self.current_loop_label})")
    #     self.wat_code.append("))")
    #     self.current_loop_label = None

    def visit_ForLoop(self, node):
        loop_label = f"loop_{node.id.id}"
        end_label = f"end_{node.id.id}"
        self.wat_code.append(f"(block ${end_label} (loop ${loop_label}")
        self.visit(node.range)
        self.visit(node.stmt)
        self.wat_code.append(f"br ${loop_label})")
        self.wat_code.append("))")

    def visit_UntilLoop(self, node):
        loop_label = f"loop_{node.line}"
        end_label = f"end_{node.line}"
        self.current_loop_label = loop_label

        self.wat_code.append(f"(block ${end_label} (loop ${loop_label})")
        self.visit(node.cond)
        self.wat_code.append("(i32.eqz)")
        self.wat_code.append(f"(br_if ${end_label})")
        self.visit(node.stmt)
        self.wat_code.append(f"(br ${loop_label})")
        self.wat_code.append("))")
        self.current_loop_label = None

    def visit_IfStmt(self, node):
        self.visit(node.cond)
        self.wat_code.append(f'{self.indent_str()}(if (then')
        self.indent += 1
        self.visit(node.positive)
        self.indent -= 1
        if node.negative.stmts:
            self.wat_code.append('    ) (else')
            self.indent += 1
            self.visit(node.negative)
            self.indent -= 1
        self.wat_code.append('    ))')

    def visit_Out(self, node):
        for arg in node.args:
            self.visit(arg)  # Prepare the argument
            self.wat_code.append(f'{self.indent_str()}call $print')

    def indent_str(self):
        return '    ' * self.indent

    def visit_FnCall(self, node):
        # Visit and push each argument to the stack
        for arg in node.args:
            # Assuming visit is a method to visit any node and handle it accordingly
            self.visit(arg)

        # Generate the call instruction
        # Assuming the function name in WebAssembly is the same as in the source
        # If not, some mapping mechanism might be required
        self.wat_code.append(f'    (call ${node.name})')
    
    def visit_Error(self, node):
        # Assuming that node.message contains the error message as a string
        # This also assumes you have predefined or will define a function $logError that takes a string/message.
        self.wat_code.append(f'    ;; Log an error message')
        self.wat_code.append(f'    (call $logError "{node.message}")')
        self.wat_code.append(f'    unreachable ;; This instruction causes the WebAssembly module to trap')

    def visit_Skip(self, node):
        # Append the WebAssembly nop instruction, which performs no operation.
        self.wat_code.append("    nop")
    
    def visit_Stop(self, node):
        # Ensure that there is a loop context to break out from.
        if not self.loop_labels:  # self.loop_labels should be a list managing current loop contexts.
            raise Exception("Stop statement not within a loop or block")

        # The WebAssembly instruction br is used to perform breaks.
        # Use the label of the nearest enclosing loop.
        # This pops the label assuming we are breaking the current innermost loop.
        loop_label = self.loop_labels.pop()

        # Append the WebAssembly code to break out of the loop.
        self.wat_code.append(f"    br {loop_label}")
    
    def visit_Return(self, node):
        # First, check if there is an expression associated with the return statement.
        if node.expr:
            # Evaluate the expression. The visit method should handle the type of the expression.
            # We assume it leaves the result on the top of the stack.
            self.visit(node.expr)

        # Append the return instruction to the .wat code.
        # The return in WebAssembly will return the top value from the stack to the caller.
        self.wat_code.append('drop')
    
    def visit_Ref(self, node):
        # Assuming node.name is the identifier for the reference
        identifier = node.name

        # Look up the identifier in some form of symbol table or environment
        if identifier in self.symbol_table:
            # Get the value associated with the identifier
            value = self.symbol_table[identifier]
            
            # Return or process the value as needed (example assumes returning the value)
            return value
        else:
            # Handle undefined reference
            raise NameError(f"Reference to undefined identifier '{identifier}'")
    
    def visit_Vector(self, node):
        # Calculate memory requirements: assume each vector element is an i32 (4 bytes)
        element_size = 4  # 4 bytes for each i32
        vector_length = len(node.values)
        total_size = element_size * vector_length
        
        # Emit code to allocate memory for the vector
        self.wat_code.append(f'{self.indent_str()}i32.const {total_size}')
        self.wat_code.append(f'{self.indent_str()}call $allocate_memory')
        
        # The pointer to the start of the allocated memory block is now on the stack.
        # Store it in a temporary local variable for ease of access
        temp_pointer = f"vec_ptr_{len(self.wat_code)}"  # Create a unique local name
        self.wat_code.append(f'{self.indent_str()}local.set ${temp_pointer}')

        # Store each element in the allocated memory
        for index, value in enumerate(node.values):
            # Emit code to evaluate the value if necessary, or directly load constants
            self.visit(value)
            
            # Calculate the address for this element
            offset = index * element_size
            self.wat_code.append(f'{self.indent_str()}local.get ${temp_pointer}')
            self.wat_code.append(f'{self.indent_str()}i32.const {offset}')
            self.wat_code.append(f'{self.indent_str()}i32.add')
            
            # Store the value in memory
            self.wat_code.append(f'{self.indent_str()}i32.store')

        # Finally, leave the base address of the vector on the stack for further use
        self.wat_code.append(f'{self.indent_str()}local.get ${temp_pointer}')

    def visit_String(self, node):
        # Assuming you have a function to allocate memory for strings,
        # e.g., allocate_memory which returns a pointer.
        string_bytes = node.value.encode('utf-8')
        string_length = len(string_bytes)

        # Simulating allocation and memory setup (the specifics depend on your environment)
        # Push the length of the string onto the stack
        self.wat_code.append(f'{self.indent_str()}i32.const {string_length}')
        
        # Simulate calling an allocation function which reserves space and returns a pointer
        self.wat_code.append(f'{self.indent_str()}call $allocate_memory')

        # Assuming the pointer to the newly allocated space is now on the top of the stack,
        # we need to store the string byte by byte.
        for i, byte in enumerate(string_bytes):
            # Stack now has the pointer to memory
            self.wat_code.append(f'{self.indent_str()}i32.const {byte}')  # Push the byte onto the stack
            self.wat_code.append(f'{self.indent_str()}i32.const {i}')  # Offset from the base pointer
            self.wat_code.append(f'{self.indent_str()}i32.add')  # Calculate address
            self.wat_code.append(f'{self.indent_str()}i32.store8')  # Store the byte at the address
    
    # def visit_Main(self, node):
    #     # Start defining the main function, this function could be named _start by convention
    #     # This is typically the entry point used in WebAssembly modules
    #     self.wat_code.append("(func $_start")
    #     self.wat_code.append("(result i32)")  # Assuming main returns an integer

    #     # Initialize any global variables or perform startup tasks
    #     if hasattr(node, 'init'):
    #         self.visit(node.init)  # Assume init is a block of statements for initialization

    #     # Call the main logic of the program
    #     if hasattr(node, 'body'):
    #         self.visit(node.body)  # Assume body contains the main logic of the program

    #     # End the function with a default return value if necessary
    #     self.wat_code.append("i32.const 0")  # Return 0 typically indicates successful execution
    #     self.wat_code.append("return")
    #     self.wat_code.append(")")
        
    #     # Set the export for the start function, so it can be called externally
    #     # This is important for environments like the Web where the WebAssembly module must explicitly export functions
    #     self.wat_code.append("(export '_start' (func $_start))")

    def visit_Main(self, node):
        self.visit(node.body)
        
    def visit_FnCall(self, node):
        # Check if the function being called has been defined
        if node.fn not in self.function_definitions:
            raise TypeError(f"Function {node.fn.id} not defined")
        
        # Retrieve the function definition
        func_def = self.function_definitions[node.fn]
        
        # Check if the number of arguments matches the number of parameters
        if len(node.args) != len(func_def.params):
            raise TypeError(f"Function {node.fn.id} expects {len(func_def.params)} arguments but got {len(node.args)}")

        # Check the type of each argument against its corresponding parameter
        for arg, param in zip(node.args, func_def.params):
            arg_type = self.visit(arg)  # Assuming visit returns the type of the node
            param_type = self.visit(param)  # Assuming the parameters have types to check
            if arg_type != param_type:
                raise TypeError(f"Type mismatch in function call {node.fn.id}: expected {param_type}, got {arg_type}")
    def visit_Func(self, node):
        # Set the current function context to check return statements against the function's declared type
        self.current_function = node

        # Check each parameter for type conflicts, if you have parameter types defined
        for param in node.params:
            self.visit(param)  # Assuming parameters have types to check

        # Now, visit the function body
        self.visit(node.body)

        # Reset the current function context
        self.current_function = None