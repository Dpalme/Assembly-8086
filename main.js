FUNCTIONS = {
    "MOV": MOV,
    "ADD": ADD,
    "PUSH": PUSH,
    "SUB": SUB,
    "INC": INC,
    "DEC": DEC,
    "MUL": MUL,
    "DIV": DIV,
    "CMP": CMP,
    "JE": JE,
    "JNE": JNE,
    "JMP": JMP,
    "POP": POP,
    "RET": RET,
    "INT": INT
};

function LOG_ERROR(error) {
    ERROR_CONSOLE = document.getElementById("errors");
    ERROR_CONSOLE.value += error + "\n";
    console.log(error);
}

function END_PROGRAM() {
    RUN = false;
    UPDATE_OUTPUT();
}

function UPDATE_OUTPUT() {
    stack_string = ""
    for (key in VAL) {
        document.getElementById(key).value = VAL[key]
    }
    STACK.forEach(element => {
        stack_string += element + "\n";
    });
    STACK_DOC.value = stack_string + "\n";
}

function ERROR() {
    RUN = false;
    LOG_ERROR("FATAL ERROR ON LINE " + (CURRENT_LINE + 1));
    LOG_ERROR(COMMANDS[CURRENT_LINE]);
    END_PROGRAM();
}

function MOV() {
    if (VAL["SP"] in VAL) {
        VAL[VAL["SP"]] = parseInt(VAL["IP"]);
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function ADD() {
    if (VAL["SP"] in VAL) {
        VAL[VAL["SP"]] += parseInt(VAL["IP"]);
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function SUB() {
    if (VAL["SP"] in VAL) {
        VAL[VAL["SP"]] -= parseInt(VAL["IP"]);
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function INC() {
    if (VAL["SP"] in VAL) {
        VAL[VAL["SP"]] += 1;
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function DEC() {
    if (VAL["SP"] in VAL) {
        VAL[VAL["SP"]] -= 1;
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function MUL() {
    if (VAL["SP"] in VAL) {
        VAL['AX'] *= parseInt(VAL[VAL["SP"]]);
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function DIV() {
    if (VAL["SP"] in VAL) {
        AX = parseInt(VAL['AX'])
        variable = parseInt(VAL[VAL['SP']])
        VAL['AX'] = Math.floor(AX / variable);
        VAL['DX'] = AX % variable;
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function CMP() {
    if (VAL["SP"] in VAL) {
        if (VAL[VAL["SP"]] == parseInt(VAL["IP"])) {
            VAL["ZF"] = 1;
        }
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function JE() {
    if (VAL["SP"] in JUMP_POINTS) {
        if (VAL["ZF"] == 1) {
            NEXT_LINE = JUMP_POINTS[VAL["SP"]];
            VAL["ZF"] = 0;
        }
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function JNE() {
    if (VAL["SP"] in JUMP_POINTS) {
        if (VAL["ZF"] == 0) {
            NEXT_LINE = JUMP_POINTS[VAL["SP"]];
        }
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function JMP() {
    if (VAL["SP"] in JUMP_POINTS) {
        NEXT_LINE = JUMP_POINTS[VAL["SP"]];
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function POP() {
    if (VAL["SP"] in VAL) {
        VAL[VAL["SP"]] = STACK.pop();
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function PUSH() {
    if (VAL["SP"] in VAL) {
        STACK.push(VAL[VAL["SP"]]);
    } else {
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function RET() {
    RUN = false;
}

function INT() {
    VAL['SP'] = 0;
    VAL['IP'] = 0;
}

function main() {
    FILE = document.getElementById("file");
    STACK_DOC = document.getElementById("stack");
    STACK_DOC.value = "";
    MAX_CALLS = document.getElementById("max_calls").value;
    STACK = [];
    VAL = {
        "AX": 0,
        "BX": 0,
        "CX": 0,
        "DX": 0,
        "ZF": 0,
        "SP": 0,
        "IP": 0
    };
    CURRENT_LINE = 0;
    NEXT_LINE = 1;
    RUN = true;

    LINES = FILE.value.split("\n");
    COMMANDS = [];
    JUMP_POINTS = {};
    LINES.forEach(line => {
        commands = [];
        line.split(" ").forEach(command => {
            if (command != "") {
                if (command.includes(":")) {
                    JUMP_POINTS[command.split(":")[0]] = LINES.indexOf(line);
                } else {
                    commands.push(command.split(' ').join(''));
                }
            }
        });
        // Make sure there where no whitespaces between arguments
        if (commands.length > 2) {
            LOG_ERROR("ERROR PARSING LINE [" + commands.join(' ') + "]\nMAKE SURE THERE ARE NO WHITESPACES BETWEEN ARGUMENTS");
            END_PROGRAM();
        }
        COMMANDS.push(commands);
    });

    function run_line(line) {
        line = COMMANDS[line];

        if (line != undefined) {
            if (line.length != 0) {
                if (line.length == 1) {
                    if (line[0] == 'RET') {
                        FUNCTIONS[line[0]]();
                    } else if(!line[0] in FUNCTIONS) {
                        LOG_ERROR("NO SUCH FUNCTION" + line[1]);
                        ERROR();
                    } else {
                        LOG_ERROR("THE FUNCTION " + line[1] + " REQUIRES ARGUMENTS");
                        ERROR();
                    }
                } else {
                    if (line[1].includes(",")) {
                        vars = line[1].split(",");
                        VAL["SP"] = vars[0].trim();
                        VAL["IP"] = vars[1].trim();
                    } else {
                        VAL["SP"] = line[1];
                    }
                    if (line[0] in FUNCTIONS) {
                        FUNCTIONS[line[0]]();
                    } else {
                        LOG_ERROR("NO SUCH FUNCTION" + line[1]);
                        ERROR();
                    }
                }
            }
        }

        CURRENT_LINE = NEXT_LINE;
        NEXT_LINE += 1;
    }
    CALLS = 0;

    while (RUN) {
        if (CURRENT_LINE < COMMANDS.length) {
            run_line(CURRENT_LINE);
            CALLS += 1;
        } else {
            LOG_ERROR("NEXT LINE IS OUT OF INDEX");
            ERROR();
        }
        if (CALLS > MAX_CALLS) {
            LOG_ERROR("MAX CALLS REACHED");
            END_PROGRAM();
        }
    }

    END_PROGRAM();
}