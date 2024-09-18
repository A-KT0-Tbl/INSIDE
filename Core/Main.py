from flet import *
from time import sleep
from random import choice

from Core.Config import *
from Core.Run import start_async_attacks
from Core.Attack.Services import urls
from Core.Attack.Feedback_Services import feedback_urls
from Core.TBanner import banner



color = check_config()['color']



def main(page: Page):
    '''Окно бомбера'''

    page.window_center()
    page.title = 'INSIDE'
    page.scroll = 'adaptive'
    page.auto_scroll = True
    page.window_width = 450
    page.window_height = 720
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.theme_mode = check_config()['theme']
    page.window_maximizable = False
    page.window_resizable = False
    change_config('attack', 'False')



    def type_attack_change(e):
        '''Тип атаки'''

        change_config('type_attack', f'{type_attack.value}')



    def feedback_change(e):
        '''Включение/выключение сервисов обратной связи'''

        change_config('feedback', f'{feedback.value}')



    def theme_change(e):
        '''Смена темы'''

        page.theme_mode = 'dark' if page.theme_mode == 'light' else 'light'
        page.update()
        change_config('theme', f'''{page.theme_mode}''')



    def color_change(e):
        '''Смена цвета'''

        _color = [MY_COLOR, 'red', 'pink', 'WHITE', 'black', 'purple', 'indigo', 'blue', 'cyan', 'teal', 'green', 'lime', 'yellow', 'amber', 'orange', 'brown', 'bluegrey', 'grey']
        global color
        color = choice(_color)
        banner.controls = [Text(spans=[TextSpan('INSIDE', TextStyle(size=95, foreground=Paint(color=color, stroke_width=9, stroke_join='round', style='stroke')))], font_family='Consolas'), Text(spans=[TextSpan('INSIDE', TextStyle(size=95, color=color))], font_family='Consolas')]
        
        number.border_color=color
        number.cursor_color=color
        number.focused_border_color=color
        number.selection_color=color
        number.label_style=TextStyle(color=color)

        replay.border_color=color
        replay.cursor_color=color
        replay.focused_border_color=color
        replay.selection_color=color
        replay.label_style=TextStyle(color=color)

        type_attack.border_color=color
        type_attack.label_style=TextStyle(color=color)

        feedback.active_color=color

        attack_button.color=color

        page.clean()
        ADD()
        change_config('color', f'{color}')



    def error(message, reason='Ошибка'):
        '''Окно с ошибкой'''

        def button_cancel(e):
            error_message.open = False
            page.update()

        error_message = AlertDialog(title=Text(reason, color=color, size=30, text_align='center', font_family='Consolas'), content=Text(message, font_family='Consolas'), actions=[TextButton('ОКЕЙ', on_click=button_cancel, style=ButtonStyle(color=color))], actions_alignment='end')

        page.dialog = error_message
        error_message.open = True
        page.update()



    def start_attack():
        '''Запуск атаки'''

        def button_cancel(e):
            attack_window.open = False
            page.update()

        attack_window = AlertDialog(modal=True, title=Text('Атака запущена...', color=color, size=30, text_align=TextAlign.CENTER), content=ProgressBar(width=325, color=color), actions=[TextButton('Закрыть', width=90, height=40, on_click=button_cancel, style=ButtonStyle(color=color))], actions_alignment='end', open=True)

        page.dialog = attack_window
        page.update()

        change_config('attack', 'True')
        start_async_attacks(number.value, replay.value)
        change_config('attack', 'False')
        attack_window.open = False
        page.update()



    def confirmation():
        '''Окно с подтверждением атаки'''

        def button_cancel(e):
            confirmation_window.open = False
            page.update()

        def button_continue(e):
            confirmation_window.open = False
            page.update()
            sleep(1)
            start_attack()    


        confirmation_window = AlertDialog(modal=True, title=Text('Внимание!', color=color, size=30, text_align='center'), content=Text('После запуска атаки и мгновенной\nеё отмены, процесс запуска будет необратим, и атака в любом случае\nбудет выполнена до конца!\n\nПродолжить?'), actions=[TextButton('НЕТ', on_click=button_cancel, style=ButtonStyle(color=color)), TextButton('ДА', on_click=button_continue, style=ButtonStyle(color=color))], actions_alignment='end', open=True)
        page.dialog = confirmation_window
        page.update()



    def checking_values(e):
        '''Проверка вводимых данных'''

        if number.value:
            try:
                int(number.value)
                if number.value.isdigit() == True:
                    if replay.value:
                        try:
                            int(replay.value)
                            if replay.value.isdigit() == True:
                                if int(replay.value) > 0 and int(replay.value) < 51:
                                    if check_config()['attack'] == 'False':
                                        confirmation()
                                    else:error('Слишком много атак, подождите!')
                                else:
                                    error('Введите количество кругов, от 1 до 50!')
                                    replay.focus()
                            else:
                                error('Введите количество кругов без каких либо символов!')
                                replay.focus()
                        except:
                            error('Введите количество кругов!')
                            replay.focus()
                    else:
                        error('Введите количество кругов!')
                        replay.focus()
                else:
                    error('Введите номер без каких либо символов!')
                    number.focus()
            except:
                error('Введите корректный номер!')
                number.focus()
        else:
            error('Введите атакующий номер!')
            number.focus()



    def information(e):
        '''Кнопка с информацией о бомбере'''

        def button(e):
            information_window.open = False
            page.update()

        information_window = AlertDialog(content=Text(f'''Сервисов - {len(urls("12345"))}\nRU - {sum(1 for i in urls("12345") if i["info"]["country"] == "RU")}   |   UZ - {sum(1 for i in urls("12345") if i["info"]["country"] == "UZ")}   |   ALL - {sum(1 for i in urls("12345") if i["info"]["country"] == "ALL")}\n\nФидбек Сервисов - {len(feedback_urls("12345"))}\nRU - {sum(1 for i in feedback_urls("12345") if i["info"]["country"] == "RU")}   |   UZ - {sum(1 for i in feedback_urls("12345") if i["info"]["country"] == "UZ")}   |   ALL - {sum(1 for i in feedback_urls("12345") if i["info"]["country"] == "ALL")}\n\nВсего - {len(urls("12345")) + len(feedback_urls("12345"))}''', text_align='center', size=17, font_family='Consolas'), title=Text(f'''INSIDE V{VERSION}''', text_align='center', size=40, color=color, font_family='Consolas'), open=True, actions=[TextButton('ОКЕЙ', width=110, height=50, on_click=button, style=ButtonStyle(color=color))], actions_alignment='end')

        page.dialog = information_window
        page.update()



    # Баннер
    banner = Stack([Text(spans=[TextSpan('INSIDE', TextStyle(size=95, foreground=Paint(color=color, stroke_width=9, stroke_join='round', style='stroke')))], font_family='Consolas'), Text(spans=[TextSpan('INSIDE', TextStyle(size=95, color=color))], font_family='Consolas')])

    # Ввод номера
    number = TextField(label='Введите номер без знака "+"', width=275, text_align='center', border_radius=40, border_color=color, cursor_color=color, focused_border_color=color, autofocus=True, selection_color=color, label_style=TextStyle(color=color))

    # Ввод кол-ва кругов
    replay = TextField(label='Круги', width=131, text_align='center', border_radius=40, border_color=color, cursor_color=color, focused_border_color=color, selection_color=color, value='1', label_style=TextStyle(color=color))

    # Тип атаки
    type_attack = Dropdown(label='Тип атаки', hint_text='Выберите тип атаки', options=[dropdown.Option('MIX'), dropdown.Option('SMS'), dropdown.Option('CALL')], width=131, border_radius=40, alignment=alignment.bottom_center, border_color=color, value=check_config()['type_attack'], label_style=TextStyle(color=color), on_change=type_attack_change)

    # Сервисы обратной связи
    feedback = Switch(label='Сервисы обратной связи (?)', value=True if check_config()['feedback'] == 'True' else False, width=280, active_color=color, on_change=feedback_change, tooltip='Сервисы, которые оставляют заявки (по типу подключения\nинтернета или взятия кредита) на разных сайтах. Будьте осторожны\nпри использовании данной функции!')

    # Запуск атаки
    attack_button = ElevatedButton(content=Text('Атака', size=25), on_click=checking_values, width=190, height=60, color=color, url=URL_CHANNEL, autofocus=True)



    def ADD():
        '''Добавление всех элементов'''

        page.add(
                Text('\n', size=6),
                banner,
                Text('\n', size=12),
                number,
                Row([type_attack, replay],alignment='CENTER'),
                feedback,
                attack_button,
                Text('\n', size=12),
                Row([IconButton(icon='telegram', icon_size=48, tooltip='Канал', url='https://t.me/+z4L61XedSVllODAy', icon_color=color),
                    IconButton(icon='telegram', icon_size=48, tooltip='Владелец', url='https://t.me/A_KTO_Tbl', icon_color=color),
                    IconButton(icon='attach_money', icon_size=48, tooltip='Донат', url='https://www.donationalerts.com/r/inside_forever', icon_color=color),
                    IconButton(icon='info', icon_size=48, tooltip='Информация', icon_color=color, on_click=information)], alignment='CENTER'),
                Row([IconButton(icon='color_lens_sharp', icon_size=48, tooltip='Цвет (рандом)', icon_color=color, on_click=color_change),
                    IconButton(icon='mode_night', icon_size=48, tooltip='Тема', on_click=theme_change, icon_color=color)], alignment='CENTER'))
    ADD()



def Start(web=True):
    if web:
        host, port = '127.0.0.1', 9876
        banner(host, port)
        app(main, view='web_browser', host=host, port=port)
    else:
        app(main)

