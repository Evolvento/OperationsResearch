from prettytable import PrettyTable


table = PrettyTable()
f = open("result.txt", "w")


def Input(restrictions, variables):
    array = list(map(str, str(input("Введите целевую функцию: ")).split()))
    for j in range(len(array)):
        if array[j] == '+':
            continue
        if array[j] == '-':
            array[j + 1] = ''.join([array[j], array[j + 1]])
            continue
        if array[j].find("x") == 0:
            multipliers[int(array[j][array[j].find("x") + 1:])] = float(1)
        elif array[j].find("x") == 1 and array[j][0] == '-':
            multipliers[int(array[j][array[j].find("x") + 1:])] = float(-1)
        else:
            multipliers[int(array[j][array[j].find("x") + 1:])] = float(array[j][:array[j].find("x")])

    for i in range(restrictions):
        array = list(map(str, str(input("Введите ограничение: ")).split()))
        simplex_table[i][0] = float(array[-1])
        for j in range(len(array) - 1):
            if array[j] == '+':
                continue
            if array[j] == '-':
                array[j + 1] = ''.join([array[j], array[j + 1]])
                continue
            if array[j] == '<=' or array[j] == '>=' or array[j] == '=':
                inequalities.append(array[j])
                continue
            if array[j].find("x") == 0:
                simplex_table[i][int(array[j][array[j].find("x") + 1:])] = float(1)
            elif array[j].find("x") == 1 and array[j][0] == '-':
                simplex_table[i][int(array[j][array[j].find("x") + 1:])] = float(-1)
            else:
                simplex_table[i][int(array[j][array[j].find("x") + 1:])] = float(array[j][:array[j].find("x")])



def Adding_New_Variables(restrictions, F_max):
    global multipliers
    global basis
    extended_form_variables = 0
    artificial_variables = []
    for i in range(len(inequalities)):
        if inequalities[i] != '=':
            extended_form_variables += 1
        if inequalities[i] == '>=':
            artificial_variables.append(i)
    
    new_variables = extended_form_variables + len(artificial_variables)
    single_array = [0 for _ in range(new_variables)]

    for i in range(restrictions):
        simplex_table[i] = simplex_table[i] + single_array
        if inequalities[i] == '<=':
            simplex_table[i][-new_variables + i] = 1.0
        if inequalities[i] == '>=':
            simplex_table[i][-new_variables + i] = -1.0

    for i in range(len(artificial_variables)):
        simplex_table[artificial_variables[i]][-1 - i] = 1.0

    M = 10**4
    if F_max: M = -10**4
    multipliers += ([0 for _ in range(extended_form_variables)] + [M for _ in range(len(artificial_variables))])
    for i in range(restrictions):
        for j in range(len(simplex_table[i]) - new_variables, len(simplex_table[i])):
            if simplex_table[i][j] == 1.0:
                basis.append(j)


def Filling_Index_String(restrictions):
    for i in range(len(multipliers)):
        for j in range(restrictions):
            index_string[i] += (simplex_table[j][i] * multipliers[basis[j]])
        index_string[i] -= multipliers[i]


def Selecting_Guiding_Column(F_max) -> int:
    global there_negatives
    element_line = 0
    index_element = 0
    for i in range(1, len(index_string)):
        if F_max:
            if index_string[i] < element_line:
                element_line = index_string[i]
                index_element = i
        else:
            if index_string[i] > element_line:
                element_line = index_string[i]
                index_element = i
    if index_element == 0:
        there_negatives = False
    return index_element


def Selecting_Guiding_Line(restrictions) -> int:
    min_element_column = 10**10
    index_min_element = 0
    for i in range(restrictions):
        if simplex_table[i][guide_column] > 0:
            elem = simplex_table[i][0] / simplex_table[i][guide_column]
            if 0 <= elem < min_element_column:
                min_element_column = elem
                index_min_element = i
    return index_min_element


variables = int(input("Введите кол-во переменных: "))
restrictions = int(input("Введите кол-во ограничений: "))
F_max = True
multipliers = [0 for j in range(variables + 1)]
simplex_table = [[0 for j in range(variables + 1)] for i in range(restrictions)]
inequalities = []
basis = []
there_negatives = True
Input(restrictions, variables)
Adding_New_Variables(restrictions, F_max)
index_string = [0 for i in range(len(multipliers))]
Filling_Index_String(restrictions)
guide_column = Selecting_Guiding_Column(F_max)
guide_line = Selecting_Guiding_Line(restrictions)
interation = 0
while there_negatives:
    interation += 1
    guide_line = Selecting_Guiding_Line(restrictions)
    guide_elem = simplex_table[guide_line][guide_column]
    table.clear()
    table.add_rows(simplex_table)
    table.padding_width = 1
    table.header = False
    table.add_row(index_string)
    f.write(f"\n\n Таблица на {interation} итерации")
    f.write(f"\nКоэфициенты ццелевой функции: {multipliers}")
    f.write(f'\n{table}')
    f.write("\nБазисные переменные:")
    f.write(f'\n{basis}')
    basis[guide_line] = guide_column

    new_simplex_table = [0 for x in range(restrictions)]
    for i in range(restrictions):
        new_simplex_table[i] = [0 for x in range(len(simplex_table[i]))]
        if i == guide_line:
            new_simplex_table[guide_line] = [x/guide_elem for x in simplex_table[guide_line]]
    for i in range(restrictions):
        if i != guide_line:
            for j in range(len(simplex_table[i])):
                new_simplex_table[i][j] = simplex_table[i][j] - (new_simplex_table[guide_line][j] * simplex_table[i][guide_column])
    simplex_table = new_simplex_table
    index_string = [0 for i in range(len(multipliers))]
    Filling_Index_String(restrictions)       
    guide_column = Selecting_Guiding_Column(F_max)

F = 0
for i in range(restrictions):
    F += (new_simplex_table[i][0] * multipliers[basis[i]])

f.write(f'\nОтвет: F = {F}')
f.close()

# 10
# 6
# x10
# 3x1 + 5x4 + 4x7 - x10 >= 0
# x2 + 6x5 + 3x8 - x10 >= 0
# 4x3 + 2x6 + 5x9 - x10 >= 0
# x1 + x2 + x3 <= 1
# x4 + x5 + x6 <= 1
# x7 + x8 + x9 <= 1