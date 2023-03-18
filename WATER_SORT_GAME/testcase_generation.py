
from random import randint
def generate(filename, num_color):
    
    str_color = 'qwertyuiop[]asdfghjkl;zxcvbnm,/<>?:}{|=-!@#$%^&*()_`~+QWERTYUIOPASDFGHJKLZXCVBNM'

    str_color = str_color[0:num_color]
    # str_color = str_color[0:randint(10,len(str_color))]

    num_color = len(str_color)
    num_cups = num_color
    capacity = randint(4, 6)
    list_char = [x for x in str_color] * capacity
    with open(filename, 'w') as f:
        num_cups = num_color + randint(2, 12)
        f.writelines([str(num_cups) + '\n', str(capacity)])
        while len(list_char) > 0:
            #len_cup = randint(0, capacity)
            len_cup = capacity
            if (len_cup == 0):
                f.write('\n')
            for j in range(len_cup):
                if j != 0:
                    f.write(' ')
                else:
                    f.write('\n')
                index = randint(0, len(list_char) * 10000) % len(list_char)
                f.write(str(list_char[index]))
                list_char.pop(index)




