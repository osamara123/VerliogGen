def get_valid_name(prompt):
    while True:
        name = input(prompt)
        if name.isalpha():
            return name
        else:
            print("Invalid input. Please enter alphabetical characters only.")

def module(name, is_synchronize, inputs, outputs, wires, regs, parameters):
    input_ports = "\n    ".join(f"input [{input_width}-1:0] {input_name}," for input_name, input_width in inputs)
    output_ports = "\n    ".join(f"output [{output_width}-1:0] {output_name}," for output_name, output_width in outputs)
    wire_declarations = "\n    ".join(f"wire [{wire_width}-1:0] {wire_name};" for wire_name, wire_width in wires)
    reg_declarations = "\n    ".join(f"reg [{reg_width}-1:0] {reg_name};" for reg_name, reg_width in regs)
    parameter_declarations = "\n    ".join(f"parameter {param_name} = {param_value};" for param_name, param_value in parameters)

    module_template = f"""
module {name} (
    {input_ports}
    {output_ports}
    """

    if is_synchronize:
        module_template += """     
    input clk,
    input rst
    """

    module_template += f"""
);
    {parameter_declarations}
    {wire_declarations}
    {reg_declarations}
"""

    if is_synchronize:
        module_template += """
    always @(posedge clk) begin
        // sequential circuit
    end
endmodule
"""
    else:
        module_template += """
// combinational circuit
endmodule
"""
    return module_template



def module_tb(name, is_synchronize, inputs, outputs, wires, regs, parameters):
    reg_ports = "\n    ".join(f"reg [{input_width}-1:0] {input_name};" for input_name, input_width in inputs)
    wire_ports = "\n    ".join(f"wire [{output_width}-1:0] {output_name};" for output_name, output_width in outputs)
    wire_declarations = "\n    ".join(f"wire [{wire_width}-1:0] {wire_name};" for wire_name, wire_width in wires)
    reg_declarations = "\n    ".join(f"reg [{reg_width}-1:0] {reg_name};" for reg_name, reg_width in regs)
    parameter_declarations = "\n    ".join(f"parameter {param_name} = {param_value};" for param_name, param_value in parameters)

    module_tb = f"""
module {name}_tb;
    {reg_ports}
"""
    if is_synchronize:
        module_tb += """
    reg clk, rst;
"""

    module_tb += f"""
    {wire_ports}
    {wire_declarations}
    {reg_declarations}
    {parameter_declarations}

    // instantiation
    {name} uut (
"""

    input_inst = "\n        ".join(f".{input_name} ({input_name})," for input_name, _ in inputs)
    output_inst = "\n        ".join(f".{output_name} ({output_name})," for output_name, _ in outputs)
    module_tb += f"        {input_inst}\n        {output_inst}"

    if is_synchronize:
        module_tb += """
        .clk(clk),
        .rst(rst)
    );
"""
    else:
        module_tb += """
    );
"""

    if is_synchronize:
        module_tb += """
    always #5 clk = ~clk;
    initial begin
        clk = 0;
        rst = 1;
        #10;
        rst = 0;
        {input_init}
        #10;
    end
endmodule
"""
    else:
        module_tb += """
    initial begin
        {input_init}
        #10;
    end
endmodule
"""

    input_init = "\n        ".join(f"{input_name} = {input_width}'b0;" for input_name, input_width in inputs)
    module_tb = module_tb.format(input_init=input_init)
    return module_tb


def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)


def main():
    while True:
        try:
            name = get_valid_name("Enter module name: ")
            is_synchronize = input("Is it synchronized (yes, no)? ").lower() == "yes"
        
            # inputs
            num_inputs = int(input("Enter number of inputs: "))
            inputs = []
            for i in range(num_inputs):
                input_name = get_valid_name(f"Enter input name{i + 1}: ")
                input_width = int(input(f"Enter width for input {input_name}: "))
                inputs.append((input_name, input_width))
            
            # wires
            wires = []
            if input('Do you need wire types in your design? (yes, no) ').lower() == 'yes':
                num_wires = int(input('Enter number of wires: '))
                for j in range(num_wires):
                    wire_name = get_valid_name(f"Enter wire name{j + 1}: ")
                    wire_width = int(input(f"Enter width for wire {wire_name}: "))
                    wires.append((wire_name, wire_width))
            
            # regs
            regs = []
            if input('Do you need reg types in your design? (yes, no) ').lower() == 'yes':
                num_regs = int(input('Enter number of regs: '))
                for k in range(num_regs):
                    reg_name = get_valid_name(f"Enter reg name{k + 1}: ")
                    reg_width = int(input(f"Enter width for reg {reg_name}: "))
                    regs.append((reg_name, reg_width))
            
            # parameters
            parameters = []
            if input('Do you need parameters in your design? (yes, no) ').lower() == 'yes':
                num_pars = int(input('Enter number of parameters: '))
                for l in range(num_pars):
                    param_name = get_valid_name(f"Enter parameter name{l + 1}: ")
                    param_value = int(input(f"Enter value for parameter {param_name}: "))
                    parameters.append((param_name, param_value))
            
            # outputs
            num_outputs = int(input("Enter number of outputs: "))
            outputs = []
            for i in range(num_outputs):
                output_name = get_valid_name(f"Enter output name{i + 1}: ")
                output_width = int(input(f"Enter width for output {output_name}: "))
                outputs.append((output_name, output_width))
            
            break
        except ValueError:
            print('Incorrect input. Please try again!')
    
    generated_module = module(name, is_synchronize, inputs, outputs, wires, regs, parameters)
    module_test = module_tb(name, is_synchronize, inputs, outputs, wires, regs, parameters)
    write_file(f"{name}.v", generated_module)
    write_file(f"{name}_tb.v", module_test)
    print('\nModule and testbench are generated successfully!')


if __name__ == "__main__":
    main()