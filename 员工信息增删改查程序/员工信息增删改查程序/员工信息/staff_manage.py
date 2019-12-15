from tabulate import tabulate
import os
TABLE_FILE = "staff_table"
COLUMNS = ['id', 'name', 'age', 'phone', 'dept', 'enrolled_date']


def print_log(msg, log_type='info'):
    if log_type == 'info':
        print("\033[32;1m%s\033[0m" % msg)
    elif log_type == 'error':
        print("\033[31;1m%s\033[0m" % msg)


def load_table(table_file):
    """
    加载员工信息表，并转成指定格式
    :param table_file:
    :return:
    """
    data = {

    }
    for i in COLUMNS:
        data[i] = []
    f = open(table_file, "r")
    for line in f:
        staff_id, name, age, phone, dept, enrolled_date = line.strip().split(",")
        data['id'].append(staff_id)
        data['name'].append(name)
        data['age'].append(age)
        data['phone'].append(phone)
        data['dept'].append(dept)
        data['enrolled_date'].append(enrolled_date)
    return data

def save_table():
    """
    把内存数据存回硬盘
    :return:
    """
    f = open(TABLE_FILE, "w", encoding="utf-8")
    for index, val in enumerate(STAFF_DATA[COLUMNS[0]]):
        row = [str(val)]
        for col in COLUMNS[1:]:
            row.append(str(STAFF_DATA[col][index]))
        raw_row = ",".join(row)
        f.write(raw_row + '\n')
    f.close()
    # os.rename("%s_new" % TABLE_FILE, TABLE_FILE)


STAFF_DATA = load_table(TABLE_FILE)     # 程序已启动就有了


def op_gt(column, condtion_val):
    """

    :param column: eg.age
    :param condtion_val: eg.22
    :return:[[id,name,age,phone]...]
    """
    matched_records = []
    for index, val in enumerate(STAFF_DATA[column]):
        if float(val) > float(condtion_val):    # 匹配上了
            record = []
            for col in COLUMNS:
                record.append(STAFF_DATA[col][index])
            matched_records.append(record)
    return matched_records


def op_lt(column, condtion_val):
    """

    :param column:
    :param condtion_val:
    :return:
    """
    matched_records = []
    for index, val in enumerate(STAFF_DATA[column]):
        if float(val) < float(condtion_val):  # 匹配上了
            record = []
            for col in COLUMNS:
                record.append(STAFF_DATA[col][index])
            matched_records.append(record)
    return matched_records


def op_eq(column, condtion_val):
    matched_records = []
    for index, val in enumerate(STAFF_DATA[column]):
        if val == condtion_val:  # 匹配上了
            record = []
            for col in COLUMNS:
                record.append(STAFF_DATA[col][index])
            matched_records.append(record)
    return matched_records


def op_like(column, condtion_val):
    matched_records = []
    for index, val in enumerate(STAFF_DATA[column]):
        if condtion_val in val:  # 匹配上了
            record = []
            for col in COLUMNS:
                record.append(STAFF_DATA[col][index])
            matched_records.append(record)
    return matched_records


def syntax_where(clause):
    """
    解析where条件，并过滤数据
    :param clause: eg. age>22
    :return:
    """
    operators = {
        '>': op_gt,
        '<': op_lt,
        '=': op_eq,
        'like': op_like,
    }
    for op_key, op_func in operators.items():
        if op_key in clause:
            column, val = clause.split(op_key)
            matched_data = op_func(column.strip(), val.strip())  # 查询数据
            return matched_data
    else:   # 只有在for执行完成且没有break的情况下，才执行
        print_log("语法错误:where条件只能支持[>,<,=,like]", "error")


def syntax_find(data_set,query_clause):
    """
    解析查询语句并从data_set中打印指定的列
    :param data_set:
    :param query_clause: find name, age from staff_table where age > 22
    :return:
    """
    filter_col_tmp = query_clause.split("from")[0][4:].split(',')
    filter_cols = [i.strip() for i in filter_col_tmp]   # 干净的columns
    if '*' in filter_cols[0]:
        print(tabulate(data_set, headers=filter_cols, tablefmt="grid"))
    else:
        reformat_data_set = []
        for row in data_set:
            filtered_vals = []   # 把要打印的字段放到列表里统一打印
            for col in filter_cols:
                col_index = COLUMNS.index(col)  # 拿到列的索引，依次取出每条记录里的对应的索引的值
                filtered_vals.append(row[col_index])
            reformat_data_set.append(filtered_vals)
        print(tabulate(reformat_data_set, headers=filter_cols, tablefmt="grid"))
    print_log("匹配到%s条数据！" % len(data_set))


def syntax_del(data_set, matched_records):
    pass


def syntax_add(query_clause, matched_data):
    """

    :param query_clause:
    :param matched_data:
    :return:
    """
    filter_col_tmp = matched_data.split("staff_table")[1][1:].split(',')
    print_log(matched_data)
    column_vals = [col.strip() for col in filter_col_tmp]
    # print('cols',column_vals)           # add staff_table Mosson,18,13678789527,IT,2018-12-11
    if len(column_vals) == len(COLUMNS[1:]):  # 不包含id,id是自增
        # find max id first , and then plus one , becomes the  id of this new record
        init_staff_id = 0
        for i in STAFF_DATA['id']:
            if int(i) > init_staff_id:
                init_staff_id = int(i)
        init_staff_id += 1  # 当前最大id再+1
        STAFF_DATA['id'].append(init_staff_id)

        for index, col in enumerate(COLUMNS[1:]):
            STAFF_DATA[col].append(column_vals[index])
        print(tabulate(STAFF_DATA, headers=COLUMNS, tablefmt="grid"))
        save_table()
        print_log("成功添加1条纪录到staff_table表")

    else:
        print_log("提供的字段数据不足，必须字段%s" % COLUMNS[1:], 'error')
        return


def syntax_update(data_set, query_clause):
    """

    :param data_set:
    :param query_clause: update saff_table set age = 25
    :return:
    """
    formula_raw = query_clause.split('set')
    if len(formula_raw) > 1:   # 有关键字
        col_name, new_val = formula_raw[1].strip().split('=')
        # 循环data_set,取到每条记录的id，拿着这个id到STAFF_DATA['id']里找对应的id的索引，
        # 再拿这个索引，去STAFF_DATA['age']列表里，改变对应索引的值
        for matched_row in data_set:
            staff_id = matched_row[0]
            staff_id_index = STAFF_DATA['id'].index(staff_id)
            STAFF_DATA[col_name][staff_id_index] = new_val
        print(tabulate(STAFF_DATA, headers=COLUMNS, tablefmt="grid"))
        save_table()   # 把修改后的数据刷到硬盘上
        print_log("成功修改%s条数据！" % len(data_set))
    else:
        print_log("语法错误：未检测到set关键字！", "error")


def syntax_parser(cmd):
    """
    解析语句，并执行
    :return
    """
    syntax_list = {
        'find': syntax_find,
        'del': syntax_del,
        'update': syntax_update,
        'add': syntax_add
    }
    # find name, age from staff_table where age > 22
    if cmd.split()[0] in ('find', 'add', 'del', 'update') and "staff_table" in cmd:

        if 'where' in cmd:
            query_clause, where_clause = cmd.split('where')
            matched_records = syntax_where(where_clause)
        else:
            matched_records = []
            for index, staff_id in enumerate(STAFF_DATA["id"]):
                record = []
                for col in COLUMNS:
                    record.append(STAFF_DATA[col][index])
                matched_records.append(record)
            query_clause = cmd
        cmd_action = query_clause.split()[0]
        if cmd_action in syntax_list:
            syntax_list[cmd_action](matched_records, query_clause)
    else:
        print_log("语法错误：\n[find\\add\\del\\update][column1,..]from[staff_table][where][column][>,..][condtion]", "error")


def main():
    """
    让用户输入语句，并执行
    :return
    """
    while True:
        cmd = input("[staff_table]：").strip()
        if not cmd:
            continue
        syntax_parser(cmd.strip())


main()  # start program