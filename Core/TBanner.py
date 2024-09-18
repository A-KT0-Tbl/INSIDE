from colorama import Fore



_banner = '''
    _____   _______ ________  ______
   /  _/ | / / ___//  _/ __ \/ ____/
   / //  |/ /\__ \ / // / / / __/   
 _/ // /|  /___/ // // /_/ / /___   
/___/_/ |_//____/___/_____/_____/
'''



def banner(host, port):
    '''Вывод баннера с ссылкой'''

    print(Fore.GREEN + _banner)
    print(f'Перейдите по http://{host}:{port}')