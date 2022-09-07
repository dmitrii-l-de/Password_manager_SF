import json #сохранение данных
import string #генерация строчных констант
import random #для случайной генерации пароля

simbols = string.ascii_letters + string.digits + '!_' # символы которые могут использоваться для генерации пароля
g = 'eyuioa' # гласные для простого пароля
s = 'tlrjxcwdgvbzfpknsmqh' # согласные для простого пароля

# получение данных из файла json
def load_db(filename):
    with open(filename) as file:
        db = json.load(file)

    return db


# сохранение данных в файле и формате json
def safe_db(filename, db):
    with open(filename, 'w') as file:
        json.dump(db, file, indent=2)

# добавляет пароль
def add_pass(db):
    site = input(' Enter website link: ')
    login = input(' Enter login: ')
    password = input(' Enter password: ')

    db.append({
        "login": login,
        "password": password,
        "site": site
    })

# исп для взаимодействия с пользователем. передается предмет для изм и предыдущее знач-е
def change(subject, previous):
    t = input(f' Enter {subject} ({previous}): ')
    if t == '':
        return previous
    else:
        return t

# изменяет запись с паролем
def change_pass(info):
    info['login'] = change('Enter login', info['login'])
    info['password'] = change('Enter password', info['password'])
    info['site'] = change('Enter website link', info['site'])

# берет 2 строки и проверяет есть ли у них общий символ
def compare(s1, s2):
    s1_set = set(s1)
    s2_set = set(s2)
    inter = s1_set.intersection(s2_set)
    return len(inter) > 0

# генерирует случайный легкий пароль
def gen_easy_pass(L):
    res = ''
    for i in range(L - 3):
        if i % 2 == 0:
            res += random.choice(g)
        else:
            res += random.choice(s)
    for i in range(3):
        res += random.choice(string.digits)
    return res


#генерирует случайный сложный пароль по условиям
def gen_pass(L):
    while True:
        res = ''
        for i in range(L):
            res += random.choice(simbols)
        #if compare(res, string.ascii_lowercase) and compare(res, string.ascii_uppercase) and compare(res, string.digits) and compare(res, '!_?'):
        # также, строку выше можно записать по другому.
        bools = [compare(res, string.ascii_lowercase),
                 compare(res, string.ascii_uppercase),
                 compare(res, string.digits) and compare(res, '!_?'),
                 res[0] not in string.ascii_uppercase,

            ]
        if all(bools):
            return res

# добавляет запись с паролем, генерируя его самостоятельно
def add_and_generate(db):
    site = input(' Enter website link: ')
    login = input(' Enter login: ')
    L = int(input(' Enter the password length: '))
    t = input(' Generate a complex password? (y/n): ')
    if 'y' in t.lower():
        password = gen_pass(L)
    else:
        password = gen_easy_pass(L)

    db.append(
        {
        "login": login,
        "password": password,
        "site": site
    }
    )

# выводит строку с паролем
def show(info, num):
    print(f'{num:3} | {info["site"]} | {info["login"]} | {info["password"]}')

# поиск сайтов содержащих нужную строку
def search(db):
    site = input(' Enter website link: ')
    results = []
    for info in db:
        if site in info['site']:
            results.append(info)

    for num, info in enumerate(results):
        show(info, num)

    m = pass_mode()
    if m == '2':
        num = int(input(' Enter the number: '))
        db.remove(results[num])
    elif m =='3':
        num = int(input(' Enter the number: '))
        info = results[num]
        change_pass(info)


# запрашивает режим у пользователя
def pass_mode():
    print(' Mode list: ')
    print(' 1. Exit search ')
    print(' 2. Delete password ')
    print(' 3. Change password ')
    m = input(' Enter the mode number: ')
    return m

# ищет уязвимости если такой пароль уже был
def check(db):
    counter = {}
    for info in db:
        if info['password'] in counter:
            counter[info['password']] += 1
        else:
            counter[info['password']] = 1
        for password, num in counter.items():
            if num > 1:
                print(f'The password "{num}" is not safe it was used on ')
        for info in db:
            if info['password'] == password:
                print(f' Website: {info["site"]:15}, Login: {info["login"]:15}')


# выбор режима работы
def mode():
    print(' Mode list: ')
    print(' 1. Add password')
    print(' 2. Generate password')
    print(' 3. Search password')
    print(' 4. Find vulnerability')
    print(' 5. Close the program')
    m = input(' Enter the mode number: ')
    return m

# основной цикл программы
def loop(filename):
    db = load_db(filename)
    while True:
        m = mode()
        if m == '1':
            add_pass(db)
        elif m == '2':
            add_and_generate(db)
        elif m == '3':
            search(db)
        elif m =='4':
            check(db)
        elif m =='5':
            break
        else:
            print('There is no such mode! ')

    safe_db(filename, db)

loop('user.json')











