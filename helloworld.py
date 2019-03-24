"""
Implements a simple Hello World grammar
"""
from lark import Lark
hello_grammar = """
statement: instruction options text | instruction text
instruction: COMMAND TIMES | COMMAND
options: OPT+
COMMAND: "repeat" | "print"
OPT: "p"
TIMES: /0|[1-9]\d*/i
WORD: /[a-zA-z](.)*\w*[^']/
text: "'" WORD "'"
%import common.WS
%ignore WS
"""

instructions_set = {
   "repeat":0,
   "print":1
}

def repeat(times = 1, options = [""], text=""):
    """Execute REPEAT instruction
    Keyword arguments:
    times   -- times of repetition (default 1)
    options -- list of printing options (default [""])
    text    -- text to be printed (default "")
    """
    if times<=0:
        raise Exception("TIMES should be a positive value. TIMES value was: {}".format(times))
    if ("p" in options):
        for i in range(1,times):
                print(text)
    else:
        txt = ""
        for i in range(1,times):
            txt += text
        print(txt)

def exec(t):
    """Form a lark tree into a command
    Calls the proper function
    """
    for found in t.find_data("instruction"):
        for child in found.children:
            if (child.type == "COMMAND"):
                instruction = str(child)
            if (child.type == "TIMES"):
                times = int(child)
    opts = []
    for found in t.find_data("options"):
        for child in found.children:
            opts.append(str(child))
    text = ""
    for found in t.find_data("text"):
        for child in found.children:
            text = text + str(child)
    if (instructions_set.get(instruction)==0):
        repeat(times, opts, text)
    elif(instructions_set.get(instruction)==1):
        print(text)
    else:
        raise Exception("Not able to parse this instruction")

def main():
    parser=Lark(hello_grammar, start="statement")
    t = parser.parse("repeat 10 p 'hello world!!!'")
    try:
        exec(t)
    except Exception as error:
        print("An error occured: ")
        print(error)

if __name__ == "__main__":
    main()
