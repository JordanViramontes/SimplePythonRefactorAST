import ast
import astor
import yaml

# CREDIT: I used help from a stack exchange form for setting up astor:
# https://stackoverflow.com/questions/36022935/rewriting-code-with-ast-python 

filePath = "simple_comparison.py"
    with open(file_path, "r") as file:
        example = file.read()  # Save the file's content as a string

tree = ast.parse(example)

# Useful classes in Python AST module for analysis and editing:
# - ast.NodeTransformer
# - ast.NodeVisitor
# - ast.Compare
# - ast.Eq
# - ast.NotEq
# - ast.If
# - ast.dump

# Define a custom NodeVisitor to check for comparison nodes

for node in ast.walk(tree):
    if isinstance(node, ast.If):
        # Bool that tells us if we should switch for later
        shouldSwitch = False
        
        # see if we are dealing with a comparison
        if isinstance(node.test, ast.Compare):
            # Check if we have a NotEQ by iterating over ops
            for op in node.test.ops:
                if (isinstance(op, ast.NotEq)):
                    shouldSwitch = True

        # check if we have a corresponding else block 
        if node.orelse:
            if (shouldSwitch):
                # swap the op (wowie it rhymes!)
                node.test.ops = [ast.Eq()]

                ifLines = []
                elseLines = []

                # get lines of code from each block
                for statement in node.body:
                    ifLines.append(statement)
                for statement in node.orelse:
                    elseLines.append(statement)
                
                # swap lines of code
                node.body = []
                node.orelse = []                
                for statement in ifLines:
                    node.orelse.append(statement)
                for statement in elseLines:
                    node.body.append(statement)

# YAML dump
data = {
    "refactored_py": tree  # Store the AST as a string
}

# Write the data to a YAML file
with open("output.yaml", "w") as file:
    yaml.dump(data, file, default_flow_style=False, indent=2)


# print(ast.dump(tree, indent=4))
print(ast.unparse(tree))
