# encoding: UTF-8
"""
Author: Diego Palmerín Bonada

Inverse Compiler for Assembly 8086 which executes programs written for
Assembly 8086 on Python.

Change the file variable to whichever file you want to run or modify the
given Test.txt file.
"""

from sys import stdout, stderr, exit

# Intialize global variables
file = 'Test.txt'
STACK = []
VAL = {'AX': 0, 'BX': 0, 'CX': 0, 'DX': 0, 'ZF': 0, 'SP': 0, 'IP': 0}
CURRENT_LINE = 0
NEXT_LINE = 1
RUN = True


# Assembly 8086 Functions
def MOV():
    """Following the format 'MOV VAL['SP'],VAL['IP']' it assigns the value of
    VAL['IP'] to the variable VAL['SP']."""

    try:
        VAL[VAL['SP']] = int(VAL['IP'])
    except KeyError:
        stderr.write('ERROR ASSIGNING %s TO %s ON LINE %d\n' %
                     (str(VAL['IP']), str(VAL['SP']), CURRENT_LINE))
        quit()


def ADD():
    """Following the format 'ADD VAL['SP'],VAL['IP']' it adds the value of
    VAL['IP'] to the variable VAL['SP']."""

    try:
        VAL[VAL['SP']] += VAL['IP']
    except KeyError:
        stderr.write('ERROR ADDING %s TO %s ON LINE %d\n' %
                     (str(VAL['IP']), str(VAL['SP']), CURRENT_LINE))
        quit()


def SUB():
    """Following the format 'SUB VAL['SP'],VAL['IP']' it subtracts the value of
    VAL['IP'] from the variable VAL['SP']."""

    try:
        VAL[VAL['SP']] -= VAL['IP']
    except KeyError:
        stderr.write('ERROR SUBSTRACTING %s FROM %s ON LINE %d\n' %
                     (str(VAL['IP']), str(VAL['SP']), CURRENT_LINE))
        quit()


def INC():
    """Following the format 'INC VAL['SP']' it adds 1 to the value of
    VAL['SP']."""

    try:
        VAL[VAL['SP']] += 1
    except KeyError:
        stderr.write('ERROR INCREASING %s ON LINE %d\n' %
                     (str(VAL['SP']), CURRENT_LINE))
        quit()


def DEC():
    """Following the format 'DEC VAL['SP']' it subtracts 1 from the value of
    VAL['SP']."""
    try:
        VAL[VAL['SP']] -= 1
    except KeyError:
        stderr.write('ERROR DECREASING %s ON LINE %d\n' %
                     (str(VAL['SP']), CURRENT_LINE))
        quit()


def DIV():
    """Following the format 'DIV VAL['SP']' it assigns the value of AX /
    VAL['SP'] to AX and the modulus of AX % VAL['SP'] to DX."""

    try:
        VAL['AX'], VAL['DX'] = VAL['AX'] // VAL[VAL['SP']],
        VAL['AX'] % VAL[VAL['SP']]
    except KeyError:
        stderr.write('ERROR DIVIDING AX BY %s ON LINE %d\n' %
                     (str(VAL['SP']), CURRENT_LINE))
        quit()
    except ZeroDivisionError:
        stderr.write('DIVISION BY ZERO ON LINE %d\n' % CURRENT_LINE)
        quit()


def MUL():
    """Following the format 'MUL VAL['SP']' it assigns the value of AX *
    VAL['SP'] to AX."""

    try:
        VAL['AX'] = VAL['AX'] * VAL[VAL['SP']]
    except KeyError:
        stderr.write('ERROR MULTIPLYING AX BY %s ON LINE %d\n' %
                     (str(VAL['SP']), CURRENT_LINE))
        quit()
    except TypeError:
        stderr.write('ERROR MULTIPLYING AX BY %s ON LINE %d\n' %
                     (str(VAL['SP']), CURRENT_LINE))
        quit()


def CMP():
    """Following the format 'CMP VAL['SP'],VAL['IP']' it assigns the value of
    1 to ZF if they are equal and 0 if they are not."""

    global VAL
    if VAL[VAL['SP']] == int(VAL['IP']):
        VAL['ZF'] = 1
    else:
        VAL['ZF'] = 0


def JE():
    """Following the format 'JE VAL['SP']' it jumps to the given line if the
    value of ZF is 1."""

    global NEXT_LINE
    try:
        if VAL['ZF'] == 1:
            NEXT_LINE = JUMP_POINTS[VAL['SP']]
            VAL['ZF'] = 0
    except KeyError:
        stderr.write('ERROR JUMPING TO %s ON LINE %d\n' %
                     (VAL['SP'], CURRENT_LINE))


def JNE():
    """Following the format 'JNE VAL['SP']' it jumps to the line with the tag
    VAL['SP'] if the value of ZF is 0."""

    global NEXT_LINE
    try:
        if VAL['ZF'] == 0:
            NEXT_LINE = JUMP_POINTS[VAL['SP']]
    except KeyError:
        stderr.write('ERROR JUMPING TO %s ON LINE %d\n' %
                     (VAL['SP'], CURRENT_LINE))


def JMP():
    """Following the format 'JMP VAR' it jumps to the line with the tag
    VAR."""

    global NEXT_LINE
    try:
        NEXT_LINE = JUMP_POINTS[VAL['SP']]
    except KeyError:
        stderr.write('ERROR JUMPING TO %s ON LINE %d\n' %
                     (VAL['SP'], CURRENT_LINE))


def PUSH():
    """Following the format 'PUSH VAR' it adds to the Stack the value of
    VAR."""

    STACK.append(VAL[VAL['SP']])


def POP(var):
    """Following the format 'POP VAR' it removes and returns the given value
    from the Stack."""

    STACK[var].pop()


def RET():
    """Following the format 'RET' it stops program execution."""
    global RUN
    RUN = False


def INT():
    """Following the format 'INT VAR' resets the base variables to 0."""
    VAL['SP'] = 0
    VAL['IP'] = 0


def quit():
    """Prints Jump Points, Stack and Values before exiting the program"""

    global RUN
    stdout.write("\nJump Points: %s\nStack: %s\nVALUES: %s\n" %
                 (str(JUMP_POINTS), str(STACK), str(VAL))
                 )
    exit(1)


def runLine(line):
    global RUN, NEXT_LINE, CURRENT_LINE

    commands = line.split()
    # Checks if the line has code to parse.
    if commands:
        # Checks if the line has a tag
        if commands[0].endswith(':'):
            # Checks if the tag is the only statement
            if len(commands) != 1:
                try:
                    VAL['SP'], VAL['IP'] = commands[2].split(",")
                except ValueError:
                    VAL['SP'] = commands[2]
                try:
                    FUNCTIONS[commands[1]]()
                except KeyError:
                    stderr.write("%s IS NOT A KNOWN FUNCTION. LINE %d\n" %
                                 (commands[1], CURRENT_LINE))
                    quit()
        else:
            # Checks if the line is a single commmand
            if len(commands) == 1:
                try:
                    FUNCTIONS[commands[0]]()
                except KeyError:
                    stdout.write('FUNCTION %s REQUIRES ARGUMENT, LINE %d\n' %
                                 commands[0], CURRENT_LINE)
                    quit()
            else:
                try:
                    VAL['SP'], VAL['IP'] = commands[1].split(",")
                except ValueError:
                    VAL['SP'] = commands[1]
                try:
                    FUNCTIONS[commands[0]]()
                except KeyError:
                    stderr.write("\n%s IS NOT A KNOWN FUNCTION. LINE %d\n" %
                                 (commands[0], CURRENT_LINE))
                    quit()
    CURRENT_LINE = NEXT_LINE
    NEXT_LINE += 1
    if CURRENT_LINE == len(LINES):
        RUN = False


# Dictionary to translate string commands into function calls
FUNCTIONS = {'MOV': MOV, 'ADD': ADD, 'PUSH': PUSH, 'SUB': SUB, 'INC': INC,
             'DEC': DEC, 'MUL': MUL, 'DIV': DIV, 'CMP': CMP, 'JE': JE,
             'JNE': JNE, 'JMP': JMP, 'POP': POP, 'RET': RET, 'INT': INT}

# Opens the file to run and assigns the file lines to an array
LINES = open(file, 'r').readlines()

# Looks for all tags and marks the line's they're on JUMP_POINTS
JUMP_POINTS = {line[0:line.index(':')]: number
               for number, line in enumerate(LINES) if line.find(':') != -1}

while RUN:
    runLine(LINES[CURRENT_LINE])

stdout.write("\nPROGRAM FINISHED WITHOUT ERRORS\n")
quit()
