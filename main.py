import numpy as np
def issue(run,clock,instructions,instructions_status,component_status,register_status):
    op = instructions[run][0]
    des = instructions[run][1]
    on1 = instructions[run][2]
    on2 = instructions[run][3]
    if op == 'load':
        instructions_status[run][0] = clock
        component_status[0][1] = 'yes'
        component_status[0][2] = op
        component_status[0][3] = des
        component_status[0][5] = on2

        if on2 not in register_status:
            component_status[0][9] = 'yes'
        elif register_status[on2]:
            component_status[0][7] = register_status[on2]
            component_status[0][9] = 'no'
        elif register_status[on2] == '':
            component_status[0][9] = 'yes'
        register_status[des] = 'integer'

    elif op == 'mult':
        flag = 0#作为指令流入乘法部件的标志，防止多次流出

        if component_status[1][1] == 'no':
            flag = 1
            instructions_status[run][0] = clock
            component_status[1][1] = 'yes'
            component_status[1][2] = op
            component_status[1][3] = des
            component_status[1][4] = on1
            component_status[1][5] = on2
            if register_status[on1]: #判断第一个操作数是否就绪
                component_status[1][6] = register_status[on1]
                component_status[1][8] = 'no'
            elif register_status[on1] == '':
                component_status[1][8] = 'yes'

            if register_status[on2]: #判断第二个操作数是否就绪
                component_status[1][7] = register_status[on2]
                component_status[1][9] = 'no'
            elif register_status[on2] == '':
                component_status[1][9] = 'yes'
            register_status[des] = 'mult1'

        elif component_status[2][1] == 'no' and flag == 0:
            instructions_status[run][0] = clock
            component_status[2][1] = 'yes'
            component_status[2][2] = op
            component_status[2][3] = des
            component_status[2][4] = on1
            component_status[2][5] = on2
            if register_status[on1]:
                component_status[2][6] = register_status[on1]
                component_status[2][8] = 'no'
            elif register_status[on1] == '':
                component_status[2][8] = 'yes'

            if register_status[on2]:
                component_status[2][7] = register_status[on2]
                component_status[2][9] = 'no'
            elif register_status[on2] == '':
                component_status[2][9] = 'yes'
            register_status[des] = 'mult2'

    elif op == 'add' or op == 'sub':
        # if component_status[3][0] == 'no':
            instructions_status[run][0] = clock
            component_status[3][1] = 'yes'
            component_status[3][2] = op
            component_status[3][3] = des
            component_status[3][4] = on1
            component_status[3][5] = on2
            if register_status[on1]:
                component_status[3][6] = register_status[on1]
                component_status[3][8] = 'no'
            elif register_status[on1] == '':
                component_status[3][8] = 'yes'


            if register_status[on2]:
                component_status[3][7] = register_status[on2]
                component_status[3][9] = 'no'
            elif register_status[on2] == '':
                component_status[3][9] = 'yes'
            register_status[des] = 'add'

    elif op == 'divd':
        # if component_status[4][0] == 'no':
            instructions_status[run][0] = clock
            component_status[4][1] = 'yes'
            component_status[4][2] = op
            component_status[4][3] = des
            component_status[4][4] = on1
            component_status[4][5] = on2
            if register_status[on1]:
                component_status[4][6] = register_status[on1]
                component_status[4][8] = 'no'
            elif register_status[on1] == '':
                component_status[4][8] = 'yes'

            if register_status[on2]:
                component_status[4][7] = register_status[on2]
                component_status[4][9] = 'no'
            elif register_status[on2] == '':
                component_status[4][9] = 'yes'
            register_status[des] = 'divide'
def read_operands(run,clock,instructions,instructions_status,component_status,register_status):
    op = instructions[run][0]
    des = instructions[run][1]
    on1 = instructions[run][2]
    on2 = instructions[run][3]

    if op == 'load':
        if (component_status[0][9] == 'yes' and component_status[0][8] == '') or \
                (component_status[0][9] == '' and component_status[0][8] == 'yes') or \
                (component_status[0][9] == '' and component_status[0][8] == '') or \
                (component_status[0][9] == 'yes' and component_status[0][8] == 'yes'):
            instructions_status[run][1] = clock

    elif op == 'mult':
        if component_status[1][3] == des and component_status[1][4] == on1 and component_status[1][5] == on2:
            if component_status[1][8] == 'yes' and component_status[1][9] == 'yes':
                # component_status[1][6] = ''
                # component_status[1][7] = ''
                # component_status[1][8] = 'no'
                # component_status[1][9] = 'yes'
                instructions_status[run][1] = clock

        elif component_status[2][3] == des and component_status[2][4] == on1 and \
                component_status[2][5] == on2:
            if component_status[2][8] == 'yes' and component_status[2][9] == 'yes':
                # component_status[2][6] = ''
                # component_status[2][7] = ''
                # component_status[2][8] = 'no'
                # component_status[2][9] = 'yes'
                instructions_status[run][1] = clock

    elif op == 'sub' or op == 'add':
        if component_status[3][8] == 'yes' and component_status[3][9] == 'yes':
            # component_status[3][6] = ''
            # component_status[3][7] = ''
            # component_status[3][8] = 'no'
            # component_status[3][9] = 'yes'
            instructions_status[run][1] = clock

    elif op == 'divd':
        if component_status[4][8] == 'yes' and component_status[4][9] == 'yes':
            # component_status[4][6] = ''
            # component_status[4][7] = ''
            # component_status[4][8] = 'no'
            # component_status[4][9] = 'yes'
            instructions_status[run][1] = clock

    # elif register_status[on1] != '' and register_status[on2] == '':
    #     pass
    # elif register_status[on1] == '' and register_status[on2] != '':
    #     pass
    # elif register_status[on1] != '' and register_status[on2] != '':
    #     pass

def execute(run,clock,instrcutions,instrcutions_status,component_status,register_status):
    op = instrcutions[run][0]
    des = instrcutions[run][1]
    on1 = instrcutions[run][2]
    on2 = instrcutions[run][3]
    if op == 'load' and exe_clock[run] == '':
        exe_clock[run] = latetime[0]
        # exe_clock[run] = 1
        component_status[0][9] = 'no'

    if op == 'mult'and exe_clock[run] == '':
        exe_clock[run] = latetime[1]
        # exe_clock[run] = 10
        if component_status[1][3] == des and component_status[1][4] == on1 and \
                component_status[1][5] == on2:
            component_status[1][8] = 'no'
            component_status[1][9] = 'no'
        if component_status[2][3] == des and component_status[2][4] == on1 and \
                component_status[2][5] == on2:
            component_status[2][8] = 'no'
            component_status[2][9] = 'no'

    if exe_clock[run] == '' and (op == 'add' or op == 'sub'):
        exe_clock[run] = latetime[2]
        # exe_clock[run] = 2
        component_status[3][8] = 'no'
        component_status[3][9] = 'no'

    if op == 'divd' and exe_clock[run] == '':
        exe_clock[run] = latetime[3]
        # exe_clock[run] = 40
        component_status[4][8] = 'no'
        component_status[4][9] = 'no'

    if exe_clock[run] != 0:
        exe_clock[run] -= 1
    if exe_clock[run] == 0:
        instrcutions_status[run][2] = clock

def write_back (run, clock, instructions, instructions_status, component_status, register_status) :
    op = instructions[run][0]
    des = instructions[run][1]
    on1 = instructions[run][2]
    on2 = instructions[run][3]
    pause = 0
    for i in range(run):
        if instructions_status[i][1] == 0 or instructions_status[i][1] == clock:
            if instructions[run][1] == instructions[i][2] or instructions[run][1] == instructions[i][3]:
                pause = 1

    if pause == 0:
        instructions_status[run][3] = clock
        for i in range(len(component_status)):
            if op == 'mult' and des == component_status[i][3] and on1 == component_status[i][4] and on2 == component_status[i][5]:
                component_status[i] = [component_status[i][0]] + ['no']+['']*8
            if op != 'mult' and des == component_status[i][3]:
                component_status[i] = [component_status[i][0]] + ['no']+['']*8
        for i in range(5):
            if component_status[i][6] == register_status[des] and component_status[i][1] == 'yes':
                component_status[i][6] = ''
                component_status[i][8] = 'yes'
            if component_status[i][7] == register_status[des] and component_status[i][1] == 'yes':
                component_status[i][7] = ''
                component_status[i][9] = 'yes'
        register_status[des] = ''




def socreboard (instructions):
    table1 = []
    table2 = []
    table3 = []
    clock = 1   #用于标记算法进行到的周期
    #instructions=[]
    #将指令状态表进行初始化
    instructions_status = []
    instructions_status = np.zeros((len(instructions), 4), dtype=int)
    #print(instructions_status)
    #设置部件状态表
    component_status = [["integer","no",'','','','','','','',''],
                        ["mult1","no",'','','','','','','',''],
                        ["mult2","no",'','','','','','','',''],
                        ["add","no",'','','','','','','',''],
                        ["divide","no",'','','','','','','','']
                        ]
    register_status = {}
    register_status = {'F0': '', 'F2': '', 'F4': '', 'F6': '', 'F8': '', 'F10': ''}
    #用于标记指令是否被发射
    sign = np.zeros(len(instructions))

    #用于记录已经发射的指令的条数
    instructions_count = 0
    # print(component_status[0])
    # print(instructions)
    finish_all_instructions = 1
    # print(len(instructions))
    while finish_all_instructions:
        #判断指令是否可以流出
        if instructions_count < len(instructions) and sign[instructions_count] == 0:
            op = instructions[instructions_count][0]
            # print(op)
            des = instructions[instructions_count][1]
            # print(des)
            on1 = instructions[instructions_count][2]
            # print(on1)
            on2 = instructions[instructions_count][3]
            # print(on2)
            if op == 'load': #若确定load指令可以流出，在issue函数之中无需判断
                if component_status[0][1] == 'no' and register_status[des] == '':
                    sign[instructions_count] = 1
                    instructions_count += 1
                    # exe_clock = 1
                    # print(first_row_elements[1])
            elif op == 'mult':
                # second_row = component_status[1]
                # second_row_elements = second_row.strip().replace("'", "").split()
                # third_row = component_status[2]
                # third_row_elements = third_row.strip().replace("'", "").split()

                if (component_status[1][1] == 'no' or component_status[2][1] == 'no') and register_status[des] == '':
                    sign[instructions_count] = 1
                    instructions_count += 1
                    # exe_clock = 10

            elif op == 'add' or op == 'sub':
                # fourth_row = component_status[3][0]
                # fourth_row_elements = fourth_row.strip().replace("'", "").split()
                if component_status[3][1] == 'no' and register_status[des] == '':
                    sign[instructions_count]=1
                    instructions_count += 1
                    # exe_clock = 2

            elif op == 'divd':
                # fifth_row = component_status[3][0]
                # fifth_row_elements = fifth_row.strip().replace("'", "").split()
                if component_status[4][1] == 'no' and register_status[des] == '':
                    sign[instructions_count] = 1
                    instructions_count += 1
                    # exe_clock = 40

        # run = 0#用于标记正在运行当中的指令
        for i in range(instructions_count):
            if sign[i] == 1:
                if instructions_status[i][0] == 0:
                    issue(i, clock, instructions, instructions_status, component_status, register_status)


        for i in range(instructions_count):
            if sign[i] == 1:
                if instructions_status[i][0] == clock:
                    continue
                if instructions_status[i][1] == 0 and instructions_status[i][0] != 0:
                    read_operands(i, clock, instructions, instructions_status, component_status, register_status)

        for i in range(instructions_count):
            if sign[i] == 1:
                if instructions_status[i][1] == clock:
                    continue
                if instructions_status[i][2] == 0 and instructions_status[i][1] != 0 and instructions_status[i][0] != 0:
                    execute(i, clock, instructions, instructions_status, component_status, register_status)

        for i in range(instructions_count):
            stall = 0
            if sign[i] == 1:
                if instructions_status[i][2] == clock:
                    continue
                if instructions_status[i][3] == 0 and instructions_status[i][2] != 0 and instructions_status[i][1] != 0 and instructions_status[i][0] != 0:
                    # for j in range(instructions_count):
                    #     if sign[j] == 1 and (instructions_status[j][1] == 0 or instructions_status[j][1] == clock):  # 如果前面执行的指令有没有读源操作数的，就可能有WAR相关
                    #         if instructions[j][2] == instructions[i][1] or instructions[j][3] == instructions[i][1]:
                    #             stall = 1
                    # if stall == 0:
                    write_back(i, clock, instructions, instructions_status, component_status, register_status)

        print("cycle:",end='')
        print(clock)
        clock += 1
        # instructions_status[len(instructions)-1][3] = 1
        table1 = instructions_status
        table2 = component_status
        table3 = register_status

        print("--------------------指令状态表--------------------")
        print("instruction         issue     read     execution     write")
        for j in range(n):
            print("{:<5}".format(instructions[j][0])+ "{:<5}".format(instructions[j][1]) + "{:<5}".format(instructions[j][2]) + "{:<5}".format(instructions[j][3]), end=' ')
            print("{:<10}".format(table1[j][0]),"{:<10}".format(table1[j][1]),"{:<10}".format(table1[j][2]),"{:<10}".format(table1[j][3]))

        print("--------------------功能部件状态表--------------------")
        print("部件名称        busy        op        Fi        Fj        Fk        Qj        Qk        Rj        Rk        ")
        for i in range(len(table2)):

            print("{:<15}".format(table2[i][0])+"{:<11}".format(table2[i][1])+"{:<10}".format(table2[i][2])+"{:<10}".format(table2[i][3])+"{:<10}".format(table2[i][4])+"{:<10}".format(table2[i][5])+"{:<10}".format(table2[i][6])+"{:<10}".format(table2[i][7])+"{:<10}".format(table2[i][8])+"{:<10}".format(table2[i][9]))

        print("--------------------寄存器状态表--------------------")
        # print(table3)
        # for i in range(len(register_status)):
        #     print(register_status.keys())
        #     print(register_status.values())
        for key in table3.keys():
            print("{:<10}".format(key), end=' ')
        print()
        # 遍历值
        for value in table3.values():
            print("{:<10}".format(value), end=' ')
        print('\n')
        if instructions_count == len(instructions):
            for i in range(len(instructions)):
                if instructions_status[i][3] == 0:
                    finish_all_instructions = 1
                    break
                else:
                    finish_all_instructions = 0

if __name__ == "__main__":
    latetime=[0,0,0,0]
    print("请输入不同指令类型的延迟时间")
    print("load指令:")
    latetime[0] = int(input())
    print("mult指令:")
    latetime[1] = int(input())
    print("add/sub指令:")
    latetime[2] = int(input())
    print("divd指令:")
    latetime[3] = int(input())
    print("请输入要执行指令的条数：")
    n = int(input())
    print("请输入要执行的指令：")
    # n=2
    ins = [['0']*4]*n
    exe_clock = [''] * len(ins)
    # ins = [ ['load', 'F2', 'R3', 'F8'],['add', 'F2', 'F6', 'F4']]
    for i in range(n):
        ins[i] = input().split(" ")
    socreboard(ins)












