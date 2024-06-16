import numpy as np
def socreboard (instructions):
    table1 = []
    table2 = []
    table3 = []
    clock=0#用于标记算法进行到的周期
    #instructions=[]
    #将指令状态表进行初始化
    instructions_status = []
    instructions_status = np.zeros((len(instructions), 4), dtype=int)
    #print(instructions_status)
    #设置部件状态表
    component_status = []
    for _ in range(5):
        row = ['no']+['']*8
        component_status.append(row)
    #print(component_status)
    #设置寄存器状态表
    register_status = []
    register_status = {
        'F0': '', 'F2': '', 'F4': '', 'F6': '', 'F8': '', 'F10': '', 'F12': '', 'F14': '',
        'F16': '', 'F18': '', 'F20': '', 'F22': '', 'F24': '', 'F26': '', 'F28': '', 'F30': ''
    }
    #print(register_status)
    #用于标记指令是否被发射
    sign = np.zeros(len(instructions))
    #print(sign)

    #用于记录已经发射的指令的条数
    instructions_count = 0

    #判断指令是否可以流出
    if instructions_count < len(instructions) and sign[instructions_count] == 0:
        op = instructions[instructions_count][0]
        des = instructions[instructions_count][1]
        on1 = instructions[instructions_count][2]
        on2 = instructions[instructions_count][3]
        if op == 'load':#若确定load指令可以流出，在issue函数之中无需判断
            if component_status[0][0] == 'no' and register_status[des] == '':
                sign[instructions_count] = 1
                instructions_count += 1
        elif op == 'mult':
            if (component_status[1][0] == 'no' or component_status[2][0] == 'no') and register_status[des] == '':
                sign[instructions_count] = 1
                instructions_count += 1
        elif op == 'add' or op == 'sub':
            if component_status[3][0] == 'no' and register_status[des] == '':
                sign[instructions_count]=1
                instructions_count += 1
        elif op == 'divd':
            if component_status[4][0] == 'no' and register_status[des] == '':
                sign[instructions_count] = 1
                instructions_count += 1
        run = 0#用于标记正在运行当中的指令
        for i in run:
            if sign[i] == 1:
                if instructions_status[i][0] == 0:
                    issue(i,clock,instructions,instructions_status,component_status,register_status)
                elif instructions_status[i][1] == 0:
                    read_operands(i,clock,instructions,instructions_status,component_status,register_status)
                elif instructions_status[i][2] == 0:
                    execute(i,clock,instructions,instructions_status,component_status,register_status)
                elif instructions_status[i][3] == 0:
                    write_back(i,clock,instructions,instructions_status,component_status,register_status)
    table1.append(instructions_status)
    table2.append(component_status)
    table3.append(register_status)
    return table1,table2,table3

def issue(run,clock,instructions,instructions_status,component_status,register_status):
    op = instructions[run][0]
    des = instructions[run][1]
    on1 = instructions[run][2]
    on2 = instructions[run][3]
    if op == 'load':
        #if component_status[0][0]=='no':
        instructions_status[run][0] = clock
        component_status[0][0] = 'yes'
        component_status[0][1] = op
        component_status[0][2] = des
        component_status[0][4] = on2
        if register_status[on2]:
            component_status[0][6] = register_status[on2]
            component_status[0][8] = 'no'
        elif register_status[on2] == '':
            component_status[0][8] = 'yes'
        register_status[des][0] = 'integer'

    elif op == 'mult':
        flag = 0#作为指令流入乘法部件的标志，防止多次流出

        if component_status[1][0] == 'no':
            flag = 1
            instructions_status[run][0] = clock
            component_status[1][0] = 'yes'
            component_status[1][1] = op
            component_status[1][2] = des
            component_status[1][3] = on1
            component_status[1][4] = on2
            if register_status[on1]:#判断第一个操作数是否就绪
                component_status[1][5] = register_status[on1]
                component_status[1][7] = 'no'
            elif register_status[on1] == '':
                component_status[1][7] = 'yes'

            if register_status[on2]:#判断第二个操作数是否就绪
                component_status[1][6] = register_status[on2]
                component_status[1][8] = 'no'
            elif register_status[on2] == '':
                component_status[1][8] = 'yes'

        elif component_status[2][0] == 'no' and flag == 0:
            instructions_status[run][0] = clock
            component_status[2][0] = 'yes'
            component_status[2][1] = op
            component_status[2][2] = des
            component_status[2][3] = on1
            component_status[2][4] = on2
            if register_status[on1]:
                component_status[2][5] = register_status[on1]
                component_status[2][7] = 'no'
            elif register_status[on1] == '':
                component_status[2][7] = 'yes'

            if register_status[on2]:
                component_status[2][6] = register_status[on1]
                component_status[2][6] = 'no'
            elif register_status[on2] == '':
                component_status[2][6] = 'yes'

    elif op == 'add' or op == 'sub':
        # if component_status[3][0] == 'no':
            instructions_status[run][0] = clock
            component_status[3][0] = 'yes'
            component_status[3][1] = op
            component_status[3][2] = des
            component_status[3][3] = on1
            component_status[3][4] = on2
            if register_status[on1]:
                component_status[3][5] = register_status[on1]
                component_status[3][7] = 'no'
            elif register_status[on1] == '':
                component_status[3][7] = 'yes'

            if register_status[on2]:
                component_status[3][6] = register_status[on1]
                component_status[3][6] = 'no'
            elif register_status[on2] == '':
                component_status[2][6] = 'yes'
    elif op == 'divd':
        # if component_status[4][0] == 'no':
            instructions_status[run][0] = clock
            component_status[4][0] = 'yes'
            component_status[4][1] = op
            component_status[4][2] = des
            component_status[4][3] = on1
            component_status[4][4] = on2
            if register_status[on1]:
                component_status[4][5] = register_status[on1]
                component_status[4][7] = 'no'
            elif register_status[on1] == '':
                component_status[4][7] = 'yes'

            if register_status[on2]:
                component_status[4][6] = register_status[on2]
                component_status[4][6] = 'no'
            elif register_status[on2] == '':
                component_status[4][6] = 'yes'
def read_operands(run,clock,instructions,instructions_status,component_status,register_status):
    op = instructions[run][0]
    des = instructions[run][1]
    on1 = instructions[run][2]
    on2 = instructions[run][3]
    if register_status[on1] == '' and register_status[on2] == '':#表示可以读取操作数
        instructions_status[run][1] = clock
        for i in range(5):
            if component_status[i][1] == op:
                component_status[i][5] = ''
                component_status[i][6] = ''
    elif register_status[on1] == 'no' and register_status[on2] == '':
        pass
    elif register_status[on1] == '' and register_status[on2] == 'no':
        pass
    elif register_status[on1] == 'no' and register_status[on2] == 'no':
        pass

def execute(run,clock,instrcutions,instrcutions_status,component_status,register_status,exe_clock):

    if exe_clock:
        exe_clock -= 1
    if exe_clock == 0:
        instrcutions_status[run][2] = clock

def write_back(run,clock,instructions,instructions_status,component_status,register_status,exe_clock):
    des = instructions[run][1]
    pause = 0
    for _ in range(run):
        if sign[instructions] == 1 and (instructions_status[i][1] == 0 or instructions_status[i][1] == clock):
            if instructions[1] == (instructions[i][2] or instructions[i][3]):
                pause = 1

    if pause == 0:
        instructions_status[run][3] = clock
        component_status = ['no']+['']*8
        register_status[des] = ''

if __name__ == "__main__":
    print("请输入指令：")
    ins = input()
    table1,table2,table3 = socreboard(ins)
    for i in range(clock):
        print(table1,table2,table3)













