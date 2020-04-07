# encoding: UTF-8
"""
Author: Diego Palmerín Bonada

Compiler from Assembly 8086 to Python.
"""

from sys import stdout, stderr, exit

# Global variables
FILE = open('Prueba.txt', 'r')
STACK = []
VAL = {'AX': 0, 'BX': 0, 'CX': 0, 'DX': 0, 'ZF': 0, 'SP': 0, 'IP': 0}
CURRENT_LINE = 0
NEXT_LINE = 1
RUN = True


def MOV():
    """Following the format 'MOV VAL['SP'],VAL['IP']' it assigns the value of
    VAL['IP'] to the variable VAL['SP']."""

    try:
        VAL[VAL['SP']] = int(VAL['IP'])
    except KeyError:
        stderr.write('ERROR ASSIGNING %s TO %s ON LINE %d\n' %
                     (str(VAL['IP']), str(VAL['SP']), CURRENT_LINE))
        quit()
    except ValueError:
        stderr.write('%s IS NOT A NUMBER. LINE %d\n' %
                     (str(VAL['IP']), CURRENT_LINE))
        quit()


def ADD():
    """Following the format 'ADD VAL['SP'],VAL['IP']' it adds the value of
    VAL['IP'] to the variable VAL['SP']."""

    try:
        VAL[VAL['SP']] += int(VAL['IP'])
    except KeyError:
        stderr.write('ERROR ASSIGNING %s TO %s ON LINE %d\n' %
                     (str(VAL['IP']), str(VAL['SP']), CURRENT_LINE))
        quit()
    except ValueError:
        stderr.write('%s IS NOT A NUMBER. LINE %d\n' %
                     (str(VAL['IP']), CURRENT_LINE))
        quit()


def SUB():
    """Following the format 'SUB VAL['SP'],VAL['IP']' it subtracts the value of
    VAL['IP'] from the variable VAL['SP']."""

    try:
        VAL[VAL['SP']] -= int(VAL['IP'])
    except KeyError:
        stderr.write('ERROR ASSIGNING %s TO %s ON LINE %d\n' %
                     (str(VAL['IP']), str(VAL['SP']), CURRENT_LINE))
        quit()
    except ValueError:
        stderr.write('%s IS NOT A NUMBER. LINE %d\n' %
                     (str(VAL['IP']), CURRENT_LINE))
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
        AX = int(VAL['AX'])
        variable = int(VAL[VAL['SP']])
        VAL['AX'], VAL['DX'] = AX // variable, AX % variable
    except KeyError:
        stderr.write('ERROR DIVIDING AX BY %s ON LINE %d\n' %
                     (str(VAL['SP']), CURRENT_LINE))
        quit()
    except ZeroDivisionError:
        stderr.write('DIVISION BY ZERO ON LINE %d\n' % CURRENT_LINE)
        quit()
    except ValueError:
        stderr.write('%s IS NOT A NUMBER. LINE %d\n' %
                     (str(VAL['SP']), CURRENT_LINE))
        quit()


def MUL():
    """Following the format 'MUL VAL['SP']' it assigns the value of AX *
    VAL['SP'] to AX."""

    try:
        VAL['AX'] *= int(VAL[VAL['SP']])
    except KeyError:
        stderr.write('ERROR MULTIPLYING AX BY %s ON LINE %d\n' %
                     (str(VAL['SP']), CURRENT_LINE))
        quit()
    except TypeError:
        stderr.write('ERROR MULTIPLYING AX BY %s ON LINE %d\n' %
                     (str(VAL['SP']), CURRENT_LINE))
        quit()
    except ValueError:
        stderr.write('%s IS NOT A NUMBER. LINE %d\n' %
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
    if VAL['SP'] in JUMP_POINTS:
        if VAL['ZF'] == 1:
            NEXT_LINE = JUMP_POINTS[VAL['SP']]
            VAL['ZF'] = 0
    else:
        stderr.write('JUMP POINT %s DOES NOT EXIST. LINE %d\n' %
                     (VAL['SP'], CURRENT_LINE))


def JNE():
    """Following the format 'JNE VAL['SP']' it jumps to the line with the tag
    VAL['SP'] if the value of ZF is 0."""

    global NEXT_LINE
    if VAL['SP'] in JUMP_POINTS:
        if VAL['ZF'] == 0:
            NEXT_LINE = JUMP_POINTS[VAL['SP']]
    else:
        stderr.write('JUMP POINT %s DOES NOT EXIST. LINE %d\n' %
                     (VAL['SP'], CURRENT_LINE))


def JMP():
    """Following the format 'JMP VAR' it jumps to the line with the tag
    VAR."""

    global NEXT_LINE
    if VAL['SP'] in JUMP_POINTS:
        NEXT_LINE = JUMP_POINTS[VAL['SP']]
    else:
        stderr.write('JUMP POINT %s DOES NOT EXIST. LINE %d\n' %
                     (VAL['SP'], CURRENT_LINE))


def PUSH():
    """Following the format 'PUSH VAR' it adds to the Stack the value of
    VAR."""

    STACK.append(int(VAL[VAL['SP']]))


def POP():
    """Following the format 'POP VAR' it removes and returns the top value
    from the Stack."""

    VAL[VAL['SP']] = STACK.pop()


def RET():
    """Following the format 'RET' it stops program execution."""
    global RUN
    RUN = False


def INT():
    """Following the format 'INT VAR' resets the base variables to 0."""
    VAL['SP'] = 0
    VAL['IP'] = 0


def quit():
    """Prints Jump Points, Stack and Values and exits the program"""

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
        if ':' in commands[0]:
            # Checks if the tag is the only statement
            if len(commands) != 1:
                if ',' in commands[2]:
                    VAL['SP'], VAL['IP'] = commands[2].split(",")
                else:
                    VAL['SP'] = commands[2]

                if commands[1] in FUNCTIONS:
                    FUNCTIONS[commands[1]]()
                else:
                    stderr.write("\n%s IS NOT A KNOWN FUNCTION. LINE %d\n" %
                                 (commands[1], CURRENT_LINE))
                    quit()
        else:
            # Checks if the line is a single commmand
            if len(commands) == 1:
                if commands[0] in FUNCTIONS:
                    FUNCTIONS[commands[0]]()
                else:
                    stderr.write("\n%s IS NOT A KNOWN FUNCTION. LINE %d\n" %
                                 (commands[0], CURRENT_LINE))
                    quit()
            else:
                if ',' in commands[1]:
                    VAL['SP'], VAL['IP'] = commands[1].split(",")
                else:
                    VAL['SP'] = commands[1]

                if commands[0] in FUNCTIONS:
                    FUNCTIONS[commands[0]]()
                else:
                    stderr.write("\n%s IS NOT A KNOWN FUNCTION. LINE %d\n" %
                                 (commands[0], CURRENT_LINE))
                    quit()

    CURRENT_LINE = NEXT_LINE
    NEXT_LINE += 1
    if CURRENT_LINE == len(LINES):
        RUN = False


FUNCTIONS = {'MOV': MOV, 'ADD': ADD, 'PUSH': PUSH, 'SUB': SUB, 'INC': INC,
             'DEC': DEC, 'MUL': MUL, 'DIV': DIV, 'CMP': CMP, 'JE': JE,
             'JNE': JNE, 'JMP': JMP, 'POP': POP, 'RET': RET, 'INT': INT}


LINES = FILE.readlines()

# Establece JUMP_POINTS
JUMP_POINTS = {line[0:line.index(':')]: number
               for number, line in enumerate(LINES) if ':' in line}

while RUN:
    runLine(LINES[CURRENT_LINE])

stdout.write("\nPROGRAM FINISHED WITHOUT ERRORS\n")
quit()
