import numpy as np
from copy import deepcopy
def socreboard (instructions):
    table1 = []
    table2 = []
    table3 = []
    clock = 1#用于标记算法进行到的周期
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
    # for _ in range(5):
    #     row = ['no']+['']*8
    #     component_status.append(row)
    #print(component_status)
    #设置寄存器状态表
    register_status = {}
    register_status = {
        'F0': '', 'F2': '', 'F4': '', 'F6': '', 'F8': '', 'F10': ''}
    #print(register_status)
    #用于标记指令是否被发射
    sign = np.zeros(len(instructions))
    #print(sign)

    #用于记录已经发射的指令的条数
    instructions_count = 0
    # print(component_status[0])
    # print(instructions)
    finish_all_instructions = 0
    while not finish_all_instructions:
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
                # 获取第一行的字符串
                # 去除多余的单引号和空格，并使用 split() 方法分割字符串

                if component_status[0][1] == 'no' and register_status[des] == '':
                    sign[instructions_count] = 1
                    instructions_count += 1
                    # print(first_row_elements[1])
            elif op == 'mult':
                second_row = component_status[1][0]
                second_row_elements = second_row.strip().replace("'", "").split()
                third_row = component_status[2][0]
                third_row_elements = third_row.strip().replace("'", "").split()

                if (second_row_elements[1] == 'no' or third_row_elements[1] == 'no') and register_status[des] == '':
                    sign[instructions_count] = 1
                    instructions_count += 1
            elif op == 'add' or op == 'sub':
                fourth_row = component_status[3][0]
                fourth_row_elements = fourth_row.strip().replace("'", "").split()
                if fourth_row_elements[1] == 'no' and register_status[des] == '':
                    sign[instructions_count]=1
                    instructions_count += 1
            elif op == 'divd':
                fifth_row = component_status[3][0]
                fifth_row_elements = fifth_row.strip().replace("'", "").split()
                if fifth_row_elements[1] == 'no' and register_status[des] == '':
                    sign[instructions_count] = 1
                    instructions_count += 1
        print(instructions_count)

        # run = 0#用于标记正在运行当中的指令
        # i = 0
        for i in range(instructions_count-1):
            if sign[i] == 1:
                if instructions_status[i][0] == 0:
                    issue(i, clock, instructions, instructions_status, component_status, register_status)
                elif instructions_status[i][1] == 0:
                    read_operands(i, clock, instructions, instructions_status, component_status, register_status)
                elif instructions_status[i][2] == 0:
                    execute(i, clock, instructions, instructions_status, component_status, register_status)
                elif instructions_status[i][3] == 0:
                    write_back(i, clock, instructions, instructions_status, component_status, register_status)
        clock += 1
        print(clock)
        print(instructions_status)
        table1 = instructions_status
        table2 = component_status
        table3 = register_status

        print("指令状态表")
        print("instruction                    issue     read     execution     write")
        for j in range(n):
            print(instructions[j][0] + '  ' + instructions[j][1] + '  ' + instructions[j][2] + '  ' + instructions[j][3])
            print(table1[j])

        print("功能部件状态表")
        print("部件名称   busy   op     Fi     Fj     Fk     Qj     Qk     Rj     Rk     ")
        for i in range(len(table2)):

            print("{:<10}".format(table2[i][0])+"{:<7}".format(table2[i][1])+"{:<7}".format(table2[i][2])+"{:<7}".format(table2[i][3])+"{:<7}".format(table2[i][4])+"{:<7}".format(table2[i][5])+"{:<7}".format(table2[i][6])+"{:<7}".format(table2[i][7])+"{:<7}".format(table2[i][8])+"{:<7}".format(table2[i][9]))

        print("寄存器状态表")
        # for dict in table3:
        #     print(dict.keys())
        #     print(dict.values())
        # for key in table3.keys():
        #     print(key, end=' ')
        # print()
        # 遍历值
        # for value in table3.values():
        #     print(value, end=' ')

        #print table*3

        #loop end
        return table1, table2, register_status, clock

def issue(run,clock,instructions,instructions_status,component_status,register_status):
    op = instructions[run][0]
    des = instructions[run][1]
    on1 = instructions[run][2]
    on2 = instructions[run][3]
    if op == 'load':
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
            if register_status[on1]: #判断第一个操作数是否就绪
                component_status[1][5] = register_status[on1]
                component_status[1][7] = 'no'
            elif register_status[on1] == '':
                component_status[1][7] = 'yes'

            if register_status[on2]: #判断第二个操作数是否就绪
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

def execute(run,clock,instrcutions,instrcutions_status,component_status,register_status):
    op = instrcutions [run][0]
    if op == 'load':
        exe_clock = 1
    elif op == 'mult':
        exe_clock = 10
    elif op == 'add' or op == 'sub':
        exe_clock = 2
    elif op == 'divd':
        exe_clock = 40
    if exe_clock:
        exe_clock -= 1
    if exe_clock == 0:
        instrcutions_status[run][2] = clock

def write_back (run, clock, instructions, instructions_status, component_status, register_status, exe_clock) :
    des = instructions[run][1]
    pause = 0
    i = 0
    for i in range(run):
        if instructions_status[i][1] == 0 or instructions_status[i][1] == clock :
            if instructions[i][1] == (instructions[i][2] or instructions[i][3]):
                pause = 1
        # if sign[instructions] == 1 and (instructions_status[i][1] == 0 or instructions_status[i][1] == clock):
        #     if instructions[1] == (instructions[i][2] or instructions[i][3]):
        #         pause = 1
    if pause == 0:
        instructions_status[run][3] = clock
        component_status = ['no']+['']*8
        register_status[des] = ''


    #release reg

if __name__ == "__main__":
    # print("请输入要执行指令的条数：")
    # n = int(input())
    # print("请输入要执行的指令：")
    n=6
    ins = [['0']*4]*n
    ins = [['load','F6','34','R2'],['load', 'F2','45','R3'],['mult','F0','F2','F6'],['sub','F8','F6','F2'],['divd','F10','F8','F6'],['add','F6','F10', 'F2']]
    # for i in range(n):
    #     ins[i] = input().split(" ")
    socreboard(ins)
    # print("指令状态表")
    # print("instruction                    issue     read     execution     write")
    # j = 1
    # for j in range(n):
    #     print(ins[j][0]+'  '+ins[j][1]+'  '+ins[j][2] + '  ' + ins[j][3])
    #     # print(table1[j])
    #
    # print("功能部件状态表")
    # print("部件名称     ","busy     ","op     ","Fi     ","Fj     ",'Fk     ','Qj     ','Qk     ','Rj     ','Rk     ')
    # # print(table2)
    # # 遍历每个子列表
    # # 遍历每个子列表
    # # 遍历每个子列表
    # for sublist in table2:
    #     for item in sublist:
    #         for all in item:
    #             print(all)
    #             print()
    # print("寄存器状态表")
    # # for dict in table3:
    # #     print(dict.keys())
    # #     print(dict.values())
    # for key in table3.keys():
    #     print(key,end=' ')
    # print()
    # # 遍历值
    # for value in table3.values():
    #     print(value,end=' ')












