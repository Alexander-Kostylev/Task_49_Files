'''
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной

Д/З:
"Дополнить справочник возможностью копирования данных из одного файла в другой.
Пользователь вводит номер строки, которую необходимо перенести из одного файла в другой."
(должен получиться новый файл .csv с одной записью из текущего файла с номерами)
'''

from os.path import exists
from os import listdir
from csv import DictReader, DictWriter


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt


files_name = list(filter(lambda f: f.endswith("csv"), listdir(path='.')))


# Ввод данных для базы данных
def get_info():
    is_valid_first_name = False
    while not is_valid_first_name:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Не валидное имя")
            else:
                is_valid_first_name = True
        except NameError as err:
            print(err)
            continue

    is_valid_last_name = False
    while not is_valid_last_name:
        try:
            last_name = input("Введите фамилию: ")
            if len(last_name) < 2:
                raise NameError("Не валидноя фамилия")
            else:
                is_valid_last_name = True
        except NameError as err:
            print(err)
            continue

    is_valid_phone = False
    while not is_valid_phone:
        try:
            phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Неверная длина номера")
            else:
                is_valid_phone = True
        except ValueError:
            print("Не валидный номер!!!")
            continue
        except LenNumberError as err:
            print(err)
            continue

    return [first_name, last_name, phone_number]


# Создание нового файла
def create_file(file_name):
    # with - Менеджер контекста
    with open(file_name, "w", encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()


# фукция прочтения файла => возвращаем список словарей
def read_file(file_name):
    with open(file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


# Фукция записи файла
# Реализована проверка на наличие телефона в базе
def write_file(file_name, lst):
    res = read_file(file_name)
    for el in res:
        if el["Телефон"] == str(lst[2]):
            print("Такой телефон уже есть")
            return
    obj = {"Имя": lst[0], "Фамилия": lst[1], "Телефон": lst[2]}
    res.append(obj)
    with open(file_name, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)


# Если файла для копирования нет, то создаем файл.
# Копируем с помощью функции "read_file" данные для дальнейшего копирования (копируется список)
# Для копирования необходимо указать строку из ходного файла которую хотим скопировать
# Проверяем наличие данной строки в исходном файле, если такой строки нет то копирования не будет
# Производим копирование данных в новый файл с помощью функции "write_file".
def copy_file(name_original_file, name_copy_file):
    if not exists(name_copy_file):
        create_file(name_copy_file)
    temp = read_file(name_original_file)
    num_str_for_copy = int(input('Укажите номер стоки для копирования: '))
    if (num_str_for_copy - 1) >= len(temp):
        print("Строки с таким номером нет в исходном файле")
        return
    write_file(name_copy_file, list(temp[num_str_for_copy - 1].values()))


# Алгоритм работы программы
def main():
    while True:
        print("Команды:\n'q' - Выход из программы \n'w' - запись в файл \n'r' - чтение из файла \n'c' - копировать")
        command = input("Введите команду: ")
        if command == 'q':
            break
        elif command == 'w':
            if len(files_name) == 0:
                print('Файлы отсутствуют!')
            else:
                print(files_name)
            temp_file_write = input('Укажите имя файла в который необходимо записать данные: ')
            if not exists(temp_file_write):
                create_file(temp_file_write)
            write_file(temp_file_write, get_info())
        elif command == 'r':
            print(f'Файлы доступные для чтения : {files_name}')
            temp_file_read = input('Укажите имя файла для чтения: ')
            if not exists(temp_file_read):
                print("Файл отсутствует. Создайте его")
                continue
            data = read_file(temp_file_read)
            for n in range(len(data)):
                print(f'Строка № {n + 1}: ', end='')
                print(*list(data[n].values()))
                print()

        elif command == 'c':
            print(f'Файлы доступные для копирования : {files_name}')
            temp_file_copy = input('Укажите имя исходного файла для копирования: ')
            if not exists(temp_file_copy):
                print("Отсутствует исходный файл. Создайте его")
                continue
            copy_file_name = input("Укажите имя для файла копирования, с указанием .csv: ")
            copy_file(temp_file_copy, copy_file_name)


# С этого места идет начало программы
main()
