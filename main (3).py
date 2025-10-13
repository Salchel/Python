import random
import time
from random import randint
import threading #ФУНКЦИЯ МНОГОПОТОЧНОСТИ
from random import choice
from rich.console import Console

characters = {
    'Майк Эрмантраут': 'Помнит все результаты Супербоула и самых ценных игроков с 1980 года. \nМожет рассказать статистику любой игры, но это ни разу не помогло в расследованиях. Раньше работал во Флориде',
    'Вероника Чейз': 'Может определить сорт бурбона по запаху, посетив 127 винокурен на "Бурбонной тропе" в Кентукки. \nВпечатляет на вечеринках, бесполезна в работе.'
}
characters_list = list(characters.keys())

count_for_character = 0 #НЕОБХОДИМО ДЛЯ ПРОВЕРКИ ВЫБОРА ПЕРСОНАЖА РАНЕЕ
count_for_levels = 0 

levels = {
    'Задание 1': 'Доступно',
    'Задание 2': 'Доступно',
    'Задание 3': 'Недоступно'
}

password = randint(1000, 9999)

console = Console() #Создание функции для красивого вывода тексста
def type_print(text, style="bold blue", delay=0.0125):
    for char in text:
        console.print(char, style=style, end="")
        time.sleep(delay)
    console.print()  # Перевод строки в конце


for key in levels.keys(): #ПОДСЧЕТ ВСЕХ УРОВНЕЙ
     count_for_levels += 1

def check_levels(): #ПРОВЕРКА ДОСТУПНОСТИ УРОВНЯ
    for key, value in levels.items():
        if value == 'Доступно':
            type_print(f'{key} - Доступно')
        else:
            type_print(f'Следующее задание недоступно')
        


def update_lvl(pass_lvl, number_lvl): #ОБНОВЛЕНИЯ СЛОВАРЯ С ЛВЛАМИ
     match pass_lvl:
        case 1: 
          type_print("Задание пройдено. Доступно следующее задание")
          if levels[f'Задание {number_lvl + 1}'] == 'Доступно':
              pass
          elif levels[f'Задание {number_lvl + 1}'] == 'Недоступно':
              levels[f'Задание {number_lvl  + 1}'] = 'Доступно'
        case 0:
             type_print("Задание провалено, пройдите его заново")


def see_lvl(things): #ФУНКЦИЯ ПЕРЕБИРАЕТ ВСЕ ПРЕДМЕТЫ ДОСТУПНЫЕ ДЛЯ ВЗАИМОДЕЙСТВИЯ НА ЛОКАЦИИ
    score = 0
    type_print('Найдено:')
    for _ in things:
        score += 1
        type_print(f'{score}) {_.title()}')

def take_thing(thing): #ДОБАВЛЕНИЕ ПРЕДМЕТА В ИНВЕНТАРЬ ИГРОКА
    type_print(f'{thing.title()} - добавлено в инвентарь')
    return thing

def see_inventory(inventory): #ПОКАЗ ИНВЕНТАРЯ
    score = 0
    if len(inventory) == 0:
        type_print('Инвентарь пуст')
    
    else:
        type_print('Инвентарь')
        for _ in inventory:
            score += 1
            print(f'{score + 1}) {_.title()}')

def check_answer(a, b, user_answer, result_list): #Функция для проверки ответа в отдельном потоке
    if user_answer == a + b:
        result_list[0] = True
    else:
        result_list[0] = False

def need_for_speed(choose_level, user_answer, result_list):
    if choose_level[user_answer - 1] == 0:
        result_list[0] = True

    else:
        result_list[0] = False

def labirint_game(lifes): #2 УРОВЕНЬ ЛАБИРИНТ В ПОДВАЛЕ
    type_print('\nВашей задачей является найти электрощиток идя по плану')
    type_print('Также в каком-то из ходов может быть ловушка, так что будте аккуратны')
    type_print('Достуные команды для управления: "w", "a", "s", "d"')
    while True:
        type_print('Вы находитесь на *')
        type_print('Выберите действие: ')
        choose_gamer_main = input()
        if choose_gamer_main == 'w':
            type_print('Вы наткнулись на систему сигнализации\n-1 жизнь')
            lifes += -1
        match choose_gamer_main:
            case 'a':
                while True:
                    type_print('Доступны команды ("w", "d"): ')
                    choose_gamer = input()
                    if choose_gamer == 'd':
                        break
                    if choose_gamer == 'w':
                        type_print('Вы пришли в тупик.')
            case 'd':
                while True:
                    type_print('Перед вами две двери с помощью "1", "2" выберите дверь')
                    choose_gamer = input()
                    if choose_gamer == '1':
                        type_print('Тупик')
                    if choose_gamer == '2':
                        type_print('Поздравляю вы нашли щиток и обесточили все здание')
                        type_print('Pадание пройдено!')
                        return 1
                    if choose_gamer == 'a':
                        break
                    if choose_gamer == 'w':
                        type_print('Тупик')
                    if choose_gamer == 'd':
                        type_print('Тупик')
                    if choose_gamer == 's':
                        break
            case 's':
                type_print('Задание провалено\n-1 жизнь')

        if lifes == 0:
            type_print('Все жизни потрачены')
            type_print('|---------|')
            type_print('|GAME OVER|')
            type_print('|---------|')
            return 0


def dowland_level(level, character): #САМИ УРОВНИ
    
    #1 УРОВЕНЬ
    processing_lvl_1 = 0 #флаг для цикла while на первом уровне(осмотр комнат))
    level_1 = 0 #флаг для работы цикла 1 уровня(заход в квартиру)
    inventary_for_1lvl = []
    run_level_1 = True
    step = 0 #ХОДЫ В 1 ЗАДАНИИ
    bedroom_space = ['кровать', 'стол', 'гардероб', 'сейф']
    kitchen_space = ['обеденный стол','холодильник','раковина','мусорное ведро']
    bathroom_space = ['раковина','полка с лекарствами', 'корзина для белья', 'душевая кабина']

    #2 УРОВЕНЬ
    run_level_2 = True
    lifes = 3

    #3 УРОВЕНЬ
    choise_1 = [0, 0, 1]
    choise_2 = [0, 1, 0]
    choise_3 = [0, 1, 1]
    choise_4 = [1, 0, 0]
    choise_5 = [1, 1, 0]
    choise_list = [choise_1, choise_2, choise_3, choise_4, choise_5]

    if level == 1:
        type_print('Загрузка задания 1...\n')
        time.sleep(3)
        type_print('На этом уровне вы можете использовать такие команды, как: \n1. see - осмотреться в текущей комнате. \n2. back - выйти из режима осмотра. \n3. open - открыть инвентарь(доступно только в коридоре).')
        type_print('На прохождение данного уровня выделяется 40 шагов. При несоблюдении этого условия игра завершится.')
        time.sleep(2)
        type_print(f'Вы - детектив под именем {characters_list[character - 1]}, которого заказывают только в тех случаях, когда иного варианта нет.\n')
        time.sleep(1)
        type_print(f'--Задание 1--')
        type_print('В деле указано, что обвиняемым является некий мистер *ДАННЫЕ ПОВРЕЖДЕНЫ* Филлипс. \nДанный гражданин утверждает, что у него украли ключи. В дполнении указано, что главным подозреваемым является жена пострадавшего, миссис *ДАННЫЕ ЗАШИФРОВАНЫ* Филлипс.')
        type_print('Ваша задача: Найти ключ и открыть сейф.')

        type_print('Подъехав к дому Филлипсов вас встречает мр.Филлипс. Подходя к двери, вы заметили в окне миссис Филипс.')
        type_print('Войдя на порог, в доме вы увидели перед собой 3 двери. Слева от вас стояли мистер и миссис Филипс.')
        type_print('Что вы хотите сделать? \n1. Узнать мнение супругов. \n2. Войти в дом.')
        
        while run_level_1 == True:
            choose_gamer = input()
            clue = 0
            if choose_gamer == '1':
                type_print('Чье именно вы хотите узнать мнение? (вписать словом) \n1.Муж - husband \n2.Жена - wife ')
            elif choose_gamer == 'wife':
                type_print('*ДАННЫЕ ПОВРЕЖДЕНЫ* считает, что это я взяла этот грёбанный ключ. Мы из-за этого уже неделю даже в одной комнате находиться не можем. Надеюсь, что вы найдете этот ключ.\n')
            elif choose_gamer == 'husband':
                type_print("Я уверен, что именно *ДАННЫЕ ПОВРЕЖДЕНЫ* украла ключ. Она вечно думает, что я что-то скрываю от неё, представляете? \nВ последний раз она вообще обвинила меня в измене, из-за чег мы и поругались. Надеюсь, вы сможете найти ключ.")
            elif choose_gamer == '2':
                type_print("Вы вошли в дом.\n")
                type_print("Вы вошли в коридор. Перед собой вы видите три двери, которые ведут на кухню, в ванную и спальню.")
                
                while level_1 == 0:
                    processing_lvl_1 = 0
                    type_print('Вы в коридоре. Вы можете пойти в: \nКухню(a) \nСпальню(w) \nВанную(d)')
                    choose_gamer = input()
                    step += 1
                    if choose_gamer == 'w':
                        type_print('\nВы вошли в спальню')
                        time.sleep(2)
                        
                        #СПАЛЬНЯ
                        while processing_lvl_1 == 0:
                            type_print('Войдя в спальню, вы наблюдаете сильный беспорядок. \nДоступные команды: \nsee - осмотреть спальню. \ns - вернуться в коридор.')
                            choose_gamer = input()
                            step += 1
                            if choose_gamer == 'see':
                                see_lvl(bedroom_space)
                                
                                while True:
                                    type_print('\nПри беглом осмотре, вы замечаете незаправленную кровать, беспорядок на столе, относительно новый гардероб и сам сейф. \nЧто именно вы хотите осмотреть? (back - Для выхода из режима осмотра.)')
                                    choose_gamer = input()
                                    step += 1

                                    match choose_gamer:
                                        case '1':
                                            type_print('Приблизившись к кровати, вы замечаете прикроватный столик, на котором лежат 3 упаковок таблеток, названия *ДАННЫЕ ПОВРЕЖДЕНЫ*. При этом, одна из них оказывается пустой.')
                                            type_print('Забрать эту упаковку? (y/n)')
                                            choose_gamer = input()
                                            if choose_gamer == 'y' and 'упаковка от таблеток' not in inventary_for_1lvl:
                                                inventary_for_1lvl.append(take_thing('упаковка от таблеток'))
                                                clue += 1
                                                
                                            elif 'упаковка от таблеток' in inventary_for_1lvl:
                                                type_print('Данный предмет уже у вас в инвентаре.')
                                                
                                            else:
                                                break
                                        case '2':
                                            type_print('Подойдя к столу, вы начали прибираться в надежде найти что-то важное. И вы оказались правы! На самом дне этого беспорядка вы находите счёт из хим.чистки.')
                                            type_print('Забрать счет? (y/n) ')
                                            choose_gamer = input()
                                            if choose_gamer == 'y' and 'счёт' not in inventary_for_1lvl:
                                                inventary_for_1lvl.append(take_thing('счёт'))
                                                clue += 1
                                            
                                            elif 'счёт' in inventary_for_1lvl:
                                                type_print('Данный предмет уже у вас в инвентаре.')
                            
                                            else:
                                                break
                                        case '3':
                                            type_print('Осмотрев весь гардероб, вы ничего не нашли.')
                                            
                                        case '4':
                                            if 'ключи' not in inventary_for_1lvl:
                                                type_print('Подойдя к сейфу, вы пробуете открыть его, но тот закрыт. Найдя ключ, вы сможете его открыть.')
                                                
                                                
                                            elif 'ключи' in inventary_for_1lvl:
                                                type_print('Вставив найденный ключ в замочную скважину и провернув его, сейф открылся.')
                                                type_print('После, вы подошли к мистеру Филлипсу и сообщили о том, что ключ нашелся. \nМистер Филлипс сказал, что он случайно их выбросил, выбрасывая пакет от рубашки.')
                                                time.sleep(4)
                                                type_print(f'Вы прошли уровень за {step} шагов')
                                                pass_next_lvl = 1
                                                update_lvl(pass_next_lvl, level)
                                                return # ОСТАНАВЛИВАЕТ ВНЕШНИЙ ЦИКЛ
                                        case 'back':
                                            break
                                            
                            if choose_gamer == 's':
                                break

                            if step == 40:
                                type_print('Игры окончена вы израсходовали все свои шаги')
                                pass_next_lvl = 0
                                update_lvl(pass_next_lvl, level)
                                return # ОСТАНАВЛИВАЕТ ВНЕШНИЙ ЦИКЛ
                    
                    elif choose_gamer == 's':
                        print('Зачем вам покидать дом, если вы не выполнили свою задачу?')

                    #КУХНЯ
                    elif choose_gamer == 'a':

                        type_print('Вы зашли на кухню')
                        while processing_lvl_1 == 0:
                            type_print('Войдя на кухню, вы впервую очередь замечаете чистый обеденный стол, холодильнк с какими-то буажками, раковину с горой посуды и под ней полное мусорное ведро. \n Доступные действия: \nd - выйти в коридор. \nsee - осмотреть кухню.')
                            choose_gamer = input()
                            step += 1
                            if choose_gamer == 'see':
                                see_lvl(kitchen_space)
                                step += 1
                                
                                while True:
                                    type_print('\nЧто именно вы собираетесь осмотреть?')
                                    choose_gamer = input()
                                    step += 1
                                    match choose_gamer:
                                        case '1':
                                            type_print('Этот стол оказался настолько чистым, что вы там ничего не смогли найти.')
                                        case '2':
                                            type_print('На холодильнике висело множество различных записок, среди которых вы замечаете лишшь две. На первой было сказано:')
                                            type_print('"Прежде чем закапать глаза, вытащи ключи из рубашки!"')
                                            type_print('Также вы осматриваете вторю записку, на которой было написано: \n')
                                            type_print(f'на которой было написано: \n *ДАННЫЕ ПОВРЕЖДЕНЫ*, не вздумай забыть свой пароль от компьютера: "{password}" и найден адрес просп. *ДАННЫЕ ЗАШИФРОВАНЫ*')
                                            type_print('Забрать записку? (y/n)')
                                            choose_gamer = input()
                                            if choose_gamer == 'y' and 'записка' not in inventary_for_1lvl:
                                                inventary_for_1lvl.append(take_thing('записка'))
                                                clue += 1
                                            elif 'записка' in inventary_for_1lvl:
                                                type_print('Данный предмет уже у вас в инвентаре.')
                                            else:
                                                pass
                                        case '3':
                                            type_print('Перебрав всю посуду, вы ничего не смогли найти.')
                                        case '4':
                                            if clue == 4:
                                                type_print('Надев перчатки, вы начали перебирать весь мусор из ведра и в итоге, на дне, вы находите ключи.')
                                                inventary_for_1lvl.append(take_thing('ключи'))
                                            elif clue == 4 and 'ключи' in inventary_for_1lvl:
                                                type_print('Ключи уже у вас в инвентаре.')
                                            else:
                                                type_print('Пока что вы не видите смысла лезть в мусорку.')
                                        case 'back':
                                            break
                            if choose_gamer == 'd':
                                break

                            if step == 40:
                                type_print('Игры окончена вы израсходовали все свои шаги')
                                pass_next_lvl = 0
                                update_lvl(pass_next_lvl, level)
                                return # ОСТАНАВЛИВАЕТ ВНЕШНИЙ ЦИКЛ
                    
                    #ВАННАЯ КОМНАТА
                    elif choose_gamer == 'd':        
                        type_print('Войдя в ванную, вы сразу приметили перед собой вымытую раковину, приоткрытый ящик с лекарствами, корзину с грязной одеждой, а рядом с нй запаренную душевую кабинку.')
                        type_print('Доступные действия: \na - выйти в коридор. \nsee - осмотреться в комнате.')
                        while processing_lvl_1 == 0:
                            type_print('Выберите команду: ')
                            choose_gamer = input()
                            step += 1
                            if choose_gamer == 'see':
                                see_lvl(bathroom_space)
                                
                                while True:
                                    type_print('\nЧто именно вы хотите осмотреть?')
                                    choose_gamer = input()
                                    step += 1
                                    
                                    match choose_gamer:
                                        case '1':
                                            type_print('В раковине вы ничего не нашли.')
                                        case '2':
                                            type_print('На удивление, но на полке вы не нашли ничего важного.')
                                        case '3':
                                            type_print('Среди грязных вещей вы нашли экземпляр счета из хим.чистки.')
                                            type_print('Забрать квитанцию? (y/n)')
                                            choose_gamer = input()
                                            if choose_gamer == 'y' and 'второй экземпляр квитанции из химчистки' not in inventary_for_1lvl:
                                                inventary_for_1lvl.append(take_thing('второй экземпляр квитанции из химчистки'))
                                                clue += 1
                                            elif 'записка' in inventary_for_1lvl:
                                                type_print('Данный предмет уже находится у вас в инвентаре.')
                                            else:
                                                pass
                                        case '4':
                                            type_print('Ничего интересного в кабинке вы не нашли.')
                                        case 'back':
                                            break

                            if choose_gamer == 'a':
                                break

                            if step == 40:
                                type_print('Игра окончена! Вы израсходовали все шаги.')
                                pass_next_lvl = 0
                                update_lvl(pass_next_lvl, level)
                                return # ОСТАНАВЛИВАЕТ ВНЕШНИЙ ЦИКЛ
                                

                    elif choose_gamer == 'open':
                        see_inventory(inventary_for_1lvl)
                    
                    if step == 40:
                        print('Игра окончена! Вы израсходовали все шаги.')
                        pass_next_lvl = 0
                        update_lvl(pass_next_lvl, level)
                        return # ОСТАНАВЛИВАЕТ ВНЕШНИЙ ЦИКЛ

    #ЗАПУСК УРОВНЯ 2
    if level == 2:
        type_print('Загрузка задания 2\n')
        time.sleep(3)
        type_print('После последнего дела о пропаже ключа от сейфа вы начали пересматривать свой журнал улик, где обнаружили одну занятную деталь...')
        type_print('Когда вы были на кухне вы обнаружили записку на обратной стороне которой был адрес и напоминание о пароле от какого-то компьютера')
        type_print('Всю неделю вас мучали мысли об этой записке и адресе. И вы решаетесь съездить на этот адрес\n')
        type_print('На месте вы обнаружили заброшенное здание старого завода')
        type_print('Вы решаете зайти в здание и осмотреть его')
         
        while run_level_2 == True:
            type_print('Подойдя к зданию, вы думаете, как поступить. Попробовать зайти с главного входа(1) или же сначала осмотреть здание(2)?')
            choose_gamer = input()
            if choose_gamer == '1':
                type_print('\nДернув за ручку вы понимаете, что главный вход заперт с внутренней стороны.')
            if choose_gamer == '2':
                type_print('Обойдя здание, вы нашли запасной вход. Онаружив, что он не заперт, вы решаете зайти внутрь. Но как только вы вошли вы увидели включенную сигнализацию\n')
                while True:
                    type_print('\n--ЗАДАНИЕ--\n')
                    type_print('Выключите систему безопасности')
                    type_print('Выберите куда вы пойдете:\n1. Главный цех\n2. Подвал')
                    choose_gamer = input()
                    if choose_gamer == '1':
                        type_print('Сработала система сигнализации. И был выпущен ядовитый газ из-за которого вы погибли\n')
                        type_print('|---------|')
                        type_print('|GAME OVER|')
                        type_print('|---------|')
                        pass_next_lvl = 0
                        update_lvl(pass_next_lvl, level)
                        return
                    
                    if choose_gamer == '2':
                        type_print('Спустившись в подвал вы обнаружили провода, ведущие в какую-то комнату. На другой же стене в заметили план этого поддвала.')
                        type_print('Вы понимаете, что необходимо найти щиток, чтобы отключить питание сигнализации.\n')
                        type_print('Сам план')
                        type_print('')
                        type_print('')
                        type_print('                  |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|')
                        type_print('                  |     ________________    |')
                        type_print('|¯¯¯¯¯¯¯¯¯¯¯¯¯¯|  |	|	|	  |')
                        type_print('|¯¯¯¯¯¯¯¯¯¯¯¯¯¯|  |	|	|	  |')
                        type_print('|              |  |	|	|	  |')
                        type_print('|              |  |	|	|______    |')
                        type_print('|              |  |	| ________    |     |')
                        type_print('|              |  |	| |      |    |     |')
                        type_print('|	      |  |	| |      |    |     |')
                        type_print('|____   _______|  |	| |      |__  |     |')
                        type_print('    |   |         |	| |___   __|  |     |')
                        type_print('    |   |_________|	|____|   |____|   __|')
                        type_print('    |______________     ____________________|')
                        type_print('		  |  *  |')
                        processing_lvl_2 = labirint_game(lifes)
                        if processing_lvl_2 == 0:
                            pass_lvl = 0
                            update_lvl(pass_lvl, level)
                            return
                        if processing_lvl_2 == 1:
                            type_print('Отключив подачу энергии вы засекли 30 минут, т.к. иначе начнутся подозрения.')
                            type_print('Перед входом на каждый этаж есть определенная эмблема, которая показывает для чего предназначен этаж')
                            type_print('Проанализировав все эмблемы на этажах угадайте какая из них ведет к начальству, т.к. именно на этом этаже находится компьютер, который вы ищете')
                            type_print('1 этаж - Шестеренки.')
                            type_print('2 этаж - Лупа.')
                            type_print('3 этаж - Стопка бумаг.')
                            
                            while True:   
                                type_print('Введите номер этажа.') 
                                choose_gamer = input()
                                if choose_gamer == '1':
                                    type_print('Поднявшись на 1 этаж вы замечаете море станков. Видимо, это этаж производства.')
                                if choose_gamer == '2':
                                    type_print('Поднявшись на этаж, вы оббнаружили нужный вам кабинет начальства.')
                                    time.sleep(2)
                                    type_print('Подойдя к двери, вы попытались открыть дверь и она открылась. Перед вашим взором был просторный кабинет. В другом конце коридора находился рабочий стол с нужным вам компьютером.')
                                    type_print('Включив компьютер, вы обнаружили, что Филлипсы смогли выкрасть документы из *ДАННЫЕ ЗАШИФРОВАНЫ*.')
                                    type_print('Обнаружив это, вы в срочном порядке выключили компьютер и побежали к главному выходу совершенно забыв о включении энергии.')
                                    type_print('Из-за этого при выходе включилась система безопасности и вы в спешке побежали обратно в подвал, чтобы отключить её как можно скорее.')
                                    
                                    
                                    while True:
                                        type_print('Текущая заддача: Как можно быстрее отключить систему безоопасности.')
                                        type_print('На экране будут появляться различные примеры. На ответ вам отводится 10 секунд.')
                                        for i in range(1, 4):
                                            a = randint(1, 100)
                                            b = randint(1, 100)
                                            type_print(f'Пример {i}: {a} + {b}')
                                        
                                            result = [None]
                                            
                                            start_time = time.time()
                                            type_print('Введите число: ')
                                            choose_gamer_int = int(input())

                                            thread = threading.Thread(target= check_answer, args=(a, b, choose_gamer_int, result))

                                            thread.start()

                                            thread.join(timeout = 10)

                                            full_time = time.time() - start_time

                                            if full_time > 10:
                                                type_print('Время вышло')
                                                lifes -= 1
                                        
                                            elif result[0] == True:
                                                type_print('Ответ засчитан')
                                            elif result[0] == False:
                                                type_print('Ответ не засчитан')
                                                lifes -= 1
                                            else:
                                                type_print('Ответ не засчитан')
                                                lifes -= 1
                                        
                                        if lifes >= 0:
                                            type_print('Вы сумели отключить систему безопасности до того момента, как она привлекла внимание.')
                                            type_print('Задание пройдено')
                                            pass_lvl = 1
                                            update_lvl(pass_lvl, level)
                                            return
                                    
                                        if choose_gamer == '3':
                                            print('Поднявшись на этаж, вы увидели табличку "Бухгалтерия". Это не тот этаж.')
                                if lifes == 0:
                                    type_print('|---------|')
                                    type_print('|GAME OVER|')
                                    type_print('|---------|')
                                    pass_lvl = 0
                                    update_lvl(pass_lvl, level)
                                    return
                                
    if level == 3:
        type_print('После успешного побега с заброшенного здания вы направились к дому Филлипсов, чтобы арестовть их.')
        type_print('Но подъезжая к дому вы увидели, как Филлипсы быстро собирают вещи. Заприметив вас, они быстро сели в машину и начали уезжать.т\n')
        type_print('--ЗАДАЧА--')
        type_print('Успешно догнать Филлипсов.')
        type_print('У вас будет 3 жизни и вам нужно будет объезжать препятствия на своем пути за определенное время (Управление осуществляется при помощи клавиш "1" "2" и "3".)')
        while True:
            lifes = 3
            max_let = randint(5,11)
            score = 0
            for _ in range(1, max_let):
                score += 1
                choise_level_1 = choice(choise_list)
                type_print(f'Раунд {score}\n')
                type_print(choise_level_1)

                result = [None]

                start_time = time.time()
                type_print('Выберите куда поедете("1", "2", "3"): ')
                choose_gamer_int = int(input())
                thread = threading.Thread(target = need_for_speed, args = (choise_level_1, choose_gamer_int, result))

                thread.start()

                thread.join(timeout = 5)

                full_time = time.time() - start_time

                if full_time > 5:
                    type_print('Время вышло')
                    lifes -= 1

                elif result[0] == True:
                    type_print('Вы объехали препятствие')
                
                elif result[0] == False:
                    type_print('Вы не прошли')
                    type_print('-1 жизнь')
                    lifes -= 1
                else:
                    type_print('Вы не прошли')
                    type_print('-1 жизнь')
                    lifes -= 1
                if lifes == 0:
                    pass_lvl = 0
                    update_lvl(pass_lvl, level)
                    return
                
                if lifes == 0:
                    type_print('|---------|')
                    type_print('|GAME OVER|')
                    type_print('|---------|')
                    pass_lvl = 0
                    update_lvl(pass_lvl, level)
                    return
            if lifes > 0:
                type_print('ПОЗДРАВЛЯЕМ ВЫ ПРОШЛИ ВСЕ ЗАДАНИЯ НАШЕЙ ИГРЫ')
                type_print('Теперь вам доступны все задания')
                return

type_print("""Добро пожаловать в игру "Город, который не спит" """)
type_print('Для начала выберите задание\n')

while True:
            type_print(f'Доступные задания:')
    
            check_levels()
            type_print('Для выбора задания напишите число: ')
            level_choose = int(input())
            levels_values_list  = list(levels.values())
            if level_choose <= count_for_levels: #ПРОВЕРКА ТОГО ЧТО ВВОД УРОВНЯ МЕНЬШЕ ИЛИ РАВНО ЗНАЧЕНИЯ МАКСИМАЛЬНОГО УРОВНЯ                 
                if levels_values_list[level_choose - 1] == 'Недоступно':
                    type_print('Данное задание временно недоступен. Пожалуйста, попробуйте позже.\n')
                elif levels_values_list[level_choose - 1] == 'Доступно':
                    if count_for_character == 1 and level_choose == 1 or level_choose == 2 or level_choose == 3: 
                        type_print("Хотите сменить персонажа?(Y/N) ")
                        character_change = input()
                    if count_for_character == 0 or character_change == 'y': #ПРОВЕРКА НА ТО ЧТО ПОЛЬЗОВАТЕЛЬ ВЫБИРАЕТ ПЕРСОНАЖА ВПЕРВЫЕ ИЛИ ОН ХОЧЕТ ЕГО ИЗМЕНИТЬ
                        type_print('Выберите персонажа: ')
                        score = 0
                        for key, value in characters.items():
                            score += 1
                            type_print(f"Персонаж №{str(score)}, {key}: {value}\n")
            
                        type_print('Для выбора персонажа введите номер персонажа:')
                        characters_choose = int(input())


                        if characters_choose == 1:
                            type_print(f"Персонаж №1, {characters_list[characters_choose-1]} выбран.")
                            dowland_level(level_choose, characters_choose)

                        if characters_choose == 2:
                            type_print(f"Персонаж №1,{characters_list[characters_choose-1]} выбран.")
                            dowland_level(level_choose, characters_choose)
                        count_for_character = 1
                    else:
                         dowland_level(level_choose, characters_choose)
            else: 
                type_print('Выберите задания из предложенных')    