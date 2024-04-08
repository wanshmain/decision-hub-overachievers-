import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session

database = SQL("sqlite:///rules.db")

# Configure application
app = Flask(__name__)


@app.route("/", methods = ['GET', 'POST'])
def homepage():
    if request.method == "GET":
        return render_template("homepage.html")
    
@app.route("/rules", methods = ['GET', 'POST'])
def rules():
    if request.method == "GET": 
       return render_template("rules.html")
    else:
        name = request.form.get("rule") 
        input_text = request.form.get("input")
        if input_text.lower() == "exit":
            return render_template("rules.html") 
        database.execute("INSERT INTO user (name, input) VALUES (?, ?)", name, input_text)
        return render_template("rules.html")

@app.route("/testing", methods = ['GET', 'POST'])
def testing(): 
    statements = []
    if request.method == "POST":     
        name = request.form.get("rule")
        def print_to_list(*args):
            statements.extend(args)
        rules = database.execute("SELECT input FROM user WHERE name = (?)", name)
        x = [y['input'] for y in rules]
        variables = {"baserate": 0, "creditscore": 0, "income": 0, "employment": 0, "interest": 0}
        def test(x, variables):
            def assign(lst, operator):
                key = lst[0]
                value = lst[2]

                if key in variables:
                    if value in variables:
                        if operator(variables[key], variables[value]):
                            return 0
                        else:
                            return 1
                    else:
                        if operator(float(variables[key]), float(value)):
                            return 0
                        else:
                            return 1

            def break_if_statement(input_string):
                if "if" in input_string and "then" in input_string:
                    conditions_part = input_string.split("if")[1].split("then")[0].strip()
                    conditions_list = [condition.strip() for condition in conditions_part.split("and")]
                    return conditions_list
                else:
                    return None

            def check(input_string):
                lst = input_string.split()

                operator = None

                if lst[1] == '>':
                    operator = lambda x, y: x > y
                elif lst[1] == '<':
                    operator = lambda x, y: x < y
                elif lst[1] == '>=':
                    operator = lambda x, y: x >= y
                elif lst[1] == '<=':
                    operator = lambda x, y: x <= y
                elif lst[1] == '=':
                    operator = lambda x, y: x == y
                elif lst[1] == '!=':
                    operator = lambda x, y: x != y
                else:
                    print_to_list("Invalid comparison operator.")
                if operator:
                    x = assign(lst, operator)
                    return x

            for text in x:
                text = text.strip()

                if not text:
                    print_to_list("No rule entered. Please provide a rule.")
                    continue

                words = text.split()
                ls = []
                conditions = break_if_statement(text)

                for word in words:
                    word = word.lower()
                    if word == "if" or word == "then":
                        continue
                    ls.append(word)

                if len(ls) == 3:
                    if ls[2] in variables:
                        variables[ls[0]] = variables[ls[2]]
                        print_to_list(f"{ls[0]} assigned the value {variables[ls[0]]} based on the rule.")
                        print_to_list("Updated list of variables:", variables)
                
                    else:
                        try:
                            variables[ls[0]] = int(ls[2])
                            print_to_list(f"{ls[0]} assigned the value {variables[ls[0]]} based on the rule.")
                            print_to_list("Updated list of variables:", variables)
                
                        except ValueError:
                            try:
                                variables[ls[0]] = float(ls[2])
                                print_to_list(f"{ls[0]} assigned the value {variables[ls[0]]} based on the rule.")
                                print_to_list("Updated list of variables:", variables)
                
                            except ValueError:
                                print_to_list(f"{ls[2]} is not a valid integer or float.")
                else:
                    l = len(conditions)
                    
                    i = 0
                    andop = []
                    while l > 0:
                        TorF = check(conditions[i])
                        i += 1
                        andop.append(TorF)
                        l -= 1

                    flag = 0
                    for element in andop:
                        if element == 1:
                            flag = 1
                            break
                    if flag == 1:
                        print_to_list("Rule Prohibits, Cannot Assign")
                    else:
                        key_1 = ls[-3]
                        value = ls[-1]
                        if key_1 in variables:
                            if value in variables:
                                try:
                                    variables[ls[-3]] = variables[ls[-1]]
                                    print_to_list(f"{ls[-3]} assigned the value {variables[ls[-1]]} based on the rule.")
                                    print_to_list("Updated list of variables:", variables)
                                except KeyError:
                                    try:
                                        variables[ls[-3]] = float(ls[-1])
                                        print_to_list(f"{ls[-3]} assigned the value {ls[-1]} based on the rule.")
                                        print_to_list("Updated list of variables:", variables)
                                    except ValueError:
                                        print(f"{ls[-1]} is not a valid integer or float.")
                            else:
                                try:
                                    variables[ls[-3]] = variables[ls[-1]]
                                    print_to_list(f"{ls[-3]} assigned the value {ls[-1]} based on the rule.")
                                    print_to_list("Updated list of variables:", variables)
                                except KeyError:
                                    try:
                                        variables[ls[-3]] = float(ls[-1])
                                        print_to_list(f"{ls[-3]} assigned the value {ls[-1]} based on the rule.")
                                        print_to_list("Updated list of variables:", variables)
                                    except ValueError:
                                        print_to_list(f"{ls[-1]} is not a valid integer or float.")
                        else:
                            print_to_list(f"{key_1} not found in variables.")

        test(x, variables)
        print_to_list("Final variables after Rule Application:", variables)
        output = []
        input_stringx = str(request.form.get("input"))
        split_values = input_stringx.split(',')
        output = [value.strip() for value in split_values]
        rulejonikala = database.execute("SELECT input FROM user WHERE name = (?) AND input LIKE 'if%'", name)
        y = str(rulejonikala[0]["input"])
        output.append(y) 
        
        test(output, variables)
        print_to_list("Final variables after second test:", variables)
        return render_template("testing.html", statements=statements)          
    else:
        return render_template("testing.html", statements=statements)
    
@app.route("/homepage", methods = ['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("homepage.html")
    else:
        return render_template()
    # Done Finally 