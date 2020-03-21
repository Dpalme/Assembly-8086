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

function LOG_ERROR(error){
    LOG.value = LOG.value + error + "\n";
    console.log(error);
}

function END_PROGRAM(){
    RUN = false;

    val_string = ""
    for(key in VAL){ val_string += key + " : " + VAL[key] + "\n"; }
    LOG_ERROR("REGISTERS:\n" + val_string);
    stack_string = "";
    STACK.forEach(element =>{
        stack_string += element + "\n";
    });
    LOG_ERROR("STACK:\n" + stack_string);
}

function ERROR() {
    RUN = false;
    LOG_ERROR("FATAL ERROR ON LINE " + (CURRENT_LINE + 1));
    LOG_ERROR(COMMANDS[CURRENT_LINE]);
    LOG_ERROR("");
    END_PROGRAM();
}

function MOV() {
    if(VAL["SP"] in VAL) {
        VAL[VAL["SP"]] = parseInt(VAL["IP"]);
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function ADD() {
    if(VAL["SP"] in VAL) {
        VAL[VAL["SP"]] += parseInt(VAL["IP"]);
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function SUB() {
    if(VAL["SP"] in VAL) {
        VAL[VAL["SP"]] -= parseInt(VAL["IP"]);
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function INC() {
    if(VAL["SP"] in VAL) {
        VAL[VAL["SP"]] += 1;
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function DEC() {
    if(VAL["SP"] in VAL) {
        VAL[VAL["SP"]] -= 1;
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function MUL() {
    if(VAL["SP"] in VAL) {
        VAL['AX'] *= parseInt(VAL[VAL["SP"]]);
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function DIV() {
    if(VAL["SP"] in VAL) {
        AX = parseInt(VAL['AX'])
        variable = parseInt(VAL[VAL['SP']])
        VAL['AX'] = Math.floor(AX / variable);
        VAL['DX'] = AX % variable;
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function CMP() {
    if(VAL["SP"] in VAL){
        if(VAL[VAL["SP"]] == parseInt(VAL["IP"])){VAL["ZF"] = 1;}
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function JE(){
    if(VAL["SP"] in JUMP_POINTS){
        if(VAL["ZF"] == 1){
            NEXT_LINE = JUMP_POINTS[VAL["SP"]];
            VAL["ZF"] = 0;
        }
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function JNE(){
    if(VAL["SP"] in JUMP_POINTS){
        if(VAL["ZF"] == 0){NEXT_LINE = JUMP_POINTS[VAL["SP"]];}
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function JMP(){
    if(VAL["SP"] in JUMP_POINTS){
       NEXT_LINE = JUMP_POINTS[VAL["SP"]];
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function POP(){
    if(VAL["SP"] in VAL){
        VAL[VAL["SP"]] = STACK.pop();
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function PUSH(){
    if(VAL["SP"] in VAL) {
        STACK.push(VAL[VAL["SP"]]);
    } else{
        LOG_ERROR(VAL["SP"] + " does not exist.");
        ERROR();
    }
}

function RET(){
    RUN = false;
}

function INT(){
    VAL['SP'] = 0;
    VAL['IP'] = 0;
}

function main() {
    FILE = document.getElementById("file");
    LOG = document.getElementById("log");
    LOG.value = "";
	STACK = [];
	VAL = {"AX": 0, "BX": 0, "CX": 0, "DX": 0, "ZF": 0, "SP": 0, "IP": 0};
	CURRENT_LINE = 0;
	NEXT_LINE = 1;
	RUN = true;

	LINES = FILE.value.split("\n");
	COMMANDS = [];
	JUMP_POINTS = {};
	LINES.forEach(line => {
		commands = [];
		line.split(" ").forEach(command => {
			if(command != "") {
				if(command.includes(":")) {
					JUMP_POINTS[command.split(":")[0]] = LINES.indexOf(line);
				}
				commands.push(command);
			}
		});
		COMMANDS.push(commands);
	});

	function run_line(line) {
        line = COMMANDS[line];

        if(line != undefined){
            if(line.length != 0) {
                if(line[0].includes(":")) {
                    if(line.length == 2) {
                        if(line[1] in FUNCTIONS) {
                            FUNCTIONS[line[1]]();
                        } else{
                            LOG_ERROR("NO SUCH FUNCTION" + line[1]);
                            ERROR();
                        }
                    } else{
                        if(line[2].includes(",")) {
                            vars = line[2].split(",");
                            VAL["SP"] = vars[0];
                            VAL["IP"] = vars[1];
                        } else{
                            VAL["SP"] = line[2];
                        }
                        if(line[1] in FUNCTIONS) {
                            FUNCTIONS[line[1]]();
                        } else{
                            LOG_ERROR("NO SUCH FUNCTION" + line[1]);
                            ERROR();
                        }
                    }
                } else{
                    if(line.length == 1) {
                        if(line[0] in FUNCTIONS) {
                            FUNCTIONS[line[0]]();
                        } else{
                            LOG_ERROR("NO SUCH FUNCTION" + line[1]);
                            ERROR();
                        }
                    } else{
                        if(line[1].includes(",")) {
                            vars = line[1].split(",");
                            VAL["SP"] = vars[0];
                            VAL["IP"] = vars[1];
                        } else{
                            VAL["SP"] = line[1];
                        }
                        if(line[0] in FUNCTIONS) {
                            FUNCTIONS[line[0]]();
                        } else{
                            LOG_ERROR("NO SUCH FUNCTION" + line[1]);
                            ERROR();
                        } 
                    }
                }
            }
        }

		CURRENT_LINE = NEXT_LINE;
		NEXT_LINE += 1;
    }
    CALLS = 0;

	while(RUN){
        if(CURRENT_LINE < COMMANDS.length) {
            run_line(CURRENT_LINE);
            CALLS += 1;
        }else{
            LOG_ERROR("NEXT LINE IS OUT OF INDEX");
            ERROR();
        }
        if(CALLS > 200){
            LOG_ERROR("MAX CALLS REACHED");
            ERROR();
        }
    }
    
    END_PROGRAM();
}
