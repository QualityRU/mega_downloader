from mega import Mega
import os

size_file = 512000


def get_dict_login_password(file='loginpassword.txt'):
    dict_account = dict()

    with open(file, 'r') as f:
        for line in f:
            line_split = line.strip().split(':')
            if len(line_split) == 2:
                email, password = line_split[0], line_split[1]
                dict_account[email] = password
    return dict_account


def mega_download(email: str, password: str, size: int):
    mega = Mega()
    m = mega.login(email=email, password=password)
    get_files = m.get_files()

    if not os.path.exists(email):
        os.mkdir(email)
    print(get_files)
    for f in get_files:
        hash_file = get_files.get(f).get('a')
        if 'c' in hash_file.keys():
            if get_files.get(f).get('s') <= size_file:
                file = m.find(get_files.get(f).get('a').get('n'))
                # print(file)
                if file[1].get('meta_mac') == (0, 0):
                    print(email, ': Пропущен файл',
                          file[1].get('a').get('n'), 'так как он пустой!')
                    continue
                m.download(file=file, dest_path=email)
                print(email, ': Скачан файл', file[1].get('a').get('n'))


if __name__ == '__main__':
    login_password = get_dict_login_password('loginpassword.txt')

    for email, password in login_password.items():
        try:
            mega_download(email, password, size_file)
        except Exception as e:
            print('Исключение:\n', e)
