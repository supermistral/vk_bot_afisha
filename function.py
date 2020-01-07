import requests, bs4, datetime
import sqlite3 as sql

class Afisha:
    def __init__(self, user_id):
        #self.City = {'мск': 'msk', 'москва': 'msk', 'сочи': 'sochi', 'спб': 'spb', 'санкт-петербург': 'spb'}
        self.Date = datetime.datetime.now().strftime("%d-%m-%Y")
        self.User_id = user_id
        self.Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}

    def open_close_2(subfunction):
        def wrapper(self, *args):
            self.conn = sql.connect("base_db.sqlite")
            self.cur = self.conn.cursor()
            a, b = subfunction(self, *args)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            return a, b
        return wrapper

    def open_close_1(subfunction):
        def wrapper(self, *args):
            self.conn = sql.connect("base_db.sqlite")
            self.cur = self.conn.cursor()
            a = subfunction(self, *args)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            return a
        return wrapper

    def output_result(self, arg, x):                                                    #ПЕРЕСМОТРЕТЬ ВЫСТАВКИ (СДЕЛАТЬ СЛОВАРЬ С КЛЮЧАМИ ПО ЧИСЛАМ)
        stroka = ''
        stroka_list = []
        #k = 0
        if x == 1: sample = "str({0}) + ' - ' + arg[{0}][0] + ' - ' + arg[{0}][5] + ' | ' + arg[film][1][:len(arg[{0}][1])-2] + ' | режиссер: ' + arg[{0}][2][:len(arg[{0}][2])-2] + '\n\n'"
        elif x == 2: sample = "{0} + ': ' + arg[{0}][0][:len(arg[{0}][0])-2] + ' - ' + arg[{0}][2] + ' | ' + arg[{0}][3] + '\n\n'"
        elif x == 3: sample = "{0} + ' | ' + arg[{0}][1] + ' | жанр: ' + arg[{0}][2][:len(argt[{0}][2])-2] + ' | где: ' + arg[{0}][0][:len(arg[{0}][0])-2] + '\n\n'"
        elif x == 4: sample = "{0} + ' | ' + arg[{0}][1] + ' | жанр: ' + arg[{0}][2][:len(arg[{0}][2])-2] + ' | режиссер: ' + arg[{0}][3][:len(arg[{0}][3])-2] + ' | где: ' + arg[{0}][0][:len(arg[{0}][0])-2] + '\n\n'"
        elif x == 5: sample = "{0} + ' - ' + arg[{0}][0] + ' - ' + arg[{0}][4] + ' | ' + arg[{0}][2] + ' | жанр: ' + arg[{0}][3][:len(arg[{0}][3])-2] + ' | где: ' + arg[{0}][1][:len(arg[{0}][1])-2] + '\n\n'"
        elif x == 6: sample = "str({0}) + ' - ' + arg[{0}][0] + ' | ' + arg[{0}][1] + '\n' + arg[{0}][2] + ' | ' + arg[{0}][3] + '\n\n'"
        for film in arg.keys():
            temp = eval(sample.format(film))
            if len(stroka + temp) > 4096:                                                          #ОБХОД ОГРАНИЧЕНИЯ ЧЕРЕЗ СПИСОК
                stroka_list.append(stroka)
                stroka = ''
            stroka += temp
        stroka_list.append(stroka)
        return stroka_list

    @open_close_1
    def start(self):
        self.cur.execute("SELECT user_id FROM users WHERE user_id = %d" %self.User_id)
        #print(self.cur.fetchone())
        if self.cur.fetchone() == None:
            self.cur.execute("INSERT INTO users (user_id) VALUES (%d)" %self.User_id)
        else:
            return ['Вы уже начали работу с ботом']
        return ['Вас приветствует Болодя Варанюк\n\nВведите город, в котором будет производиться поиск информации, с помощью команды:\n"город ВАШ ГОРОД"']
    
    @open_close_1
    def confirm(self, user_city):
        cities = {
            'мск': 'msk', 'москва': 'msk', 'спб': 'spb', 'санкт-петербург': 'spb', 'абакан': 'abakan', 'азов': 'azov', 'альметьевск': 'almetyevsk', 'анапа': 'anapa', 
            'ангарск': 'angarsk', 'арзамас': 'arzamas', 'армавир': 'armavir', 'артем': 'artem', 'архангельск': 'arkhangelsk', 'астрахань': 'astrakhan', 'ачинск': 'achinsk', 'балаково': 'balakovo', 
            'балашиха': 'balashiha', 'балашов': 'balashov', 'барнаул': 'barnaul', 'батайск': 'bataisk', 'белгород': 'belgorod', 'белорецк': 'beloretsk', 'белореченск': 'belorechensk', 
            'бердск': 'berdsk', 'березники': 'berezniki', 'бийск': 'bijsk', 'благовещенск': 'blagoveshensk', 'братск': 'bratsk', 'брянск': 'bryansk', 'бугульма': 'bugulma', 'бугуруслан': 'buguruslan', 
            'бузулук': 'buzuluk', 'великий новгород': 'veliky_novgorod', 'верхняя пышма': 'verchnaya_pishma', 'видное': 'vidnoe', 'владивосток': 'vladivostok', 'владикавказ': 'vladikavkaz', 
            'владимир': 'vladimir', 'волгоград': 'volgograd', 'волгодонск': 'volgodonsk', 'волжский': 'volzhskij', 'вологда': 'vologda', 'вольск': 'volsk', 'воронеж': 'voronezh', 
            'воскресенск': 'voskresensk', 'всеволожск': 'vsevolozhsk', 'выборг': 'viborg', 'гатчина': 'gatchina', 'геленджик': 'gelendzhik', 'горно-алтайск': 'gorno-altajsk', 'грозный': 'groznij', 
            'губкин': 'gubkin', 'гудермес': 'gudermes', 'дербент': 'derbent', 'дзержинск': 'dzerginsk', 'димитровград': 'dimitrovgrad', 'дмитров': 'dmitrov', 'долгопрудный': 'dolgoprudnyj', 
            'домодедово': 'domodedovo', 'дубна': 'dubna', 'евпатория': 'evpatoriya', 'екатеринбург': 'ekaterinburg', 'елец': 'elets', 'ессентуки': 'essentuki', 'железногорск': 'zheleznogorsk', 
            'жуковский': 'zhukovskij', 'зарайск': 'zarajsk', 'заречный': 'zarechnij', 'звенигород': 'zvenigorod', 'зеленогорск': 'zelenogorsk_spb', 'зеленоград': 'zelenograd', 'златоуст': 'zlatoust', 
            'иваново': 'ivanovo', 'ивантеевка': 'ivanteevka', 'ижевск': 'izhevsk', 'иркутск': 'irkutsk', 'искитим': 'iskitim', 'истра': 'istra', 'йошкар-ола': 'yoshkar_ola', 'казань': 'kazan', 
            'калининград': 'kaliningrad', 'калуга': 'kaluga', 'каменск-уральский': 'kamensk_uralskij', 'камышин': 'kamyshin', 'каспийск': 'kaspijsk', 'кемерово': 'kemerovo', 'кингисепп': 'kingisepp', 
            'кириши': 'kirishi', 'киров': 'kirov', 'кисловодск': 'kislovodsk', 'клин': 'klin', 'клинцы': 'klinci', 'ковров': 'kovrov', 'коломна': 'kolomna', 'колпино': 'kolpino', 
            'комсомольск-на-амуре': 'komsomolsk-na-amure', 'копейск': 'kopeisk', 'королев': 'korolev', 'коряжма': 'koryazhma', 'кострома': 'kostroma', 'красногорск': 'krasnogorsk', 
            'краснодар': 'krasnodar', 'краснознаменск': 'krasnoznamensk', 'красноярск': 'krasnoyarsk', 'кронштадт': 'kronshtadt', 'кстово': 'kstovo', 'кубинка': 'kubinka', 'кузнецк': 'kuznetsk', 
            'курган': 'kurgan', 'курск': 'kursk', 'лесной': 'lesnoj', 'лесной городок': 'lesnoy_gorodok', 'липецк': 'lipetsk', 'лобня': 'lobnja', 'лодейное поле': 'lodeynoe_pole', 
            'ломоносов': 'lomonosov1', 'луховицы': 'luhovici', 'лысьва': 'lysva', 'лыткарино': 'lytkarino', 'люберцы': 'luberci', 'магадан': 'magadan', 'магнитогорск': 'magnitogorsk', 
            'майкоп': 'majkop', 'махачкала': 'mahachkala', 'миасс': 'miass', 'можайск': 'mozhaysk', 'московский': 'moskovsky', 'мурманск': 'murmansk', 'муром': 'murom', 'мытищи': 'mitischi', 
            'набережные челны': 'naberezhnie_chelni', 'назрань': 'nazran', 'нальчик': 'nalchik', 'наро-фоминск': 'naro_fominsk', 'находка': 'nahodka', 'невинномысск': 'nevinnomissk', 
            'нефтекамск': 'neftekamsk', 'нефтеюганск': 'neftejugansk', 'нижневартовск': 'nizhnevartovsk', 'нижнекамск': 'nizhnekamsk', 'нижний новгород': 'nnovgorod', 'нижний тагил': 'nizhny_tagil', 
            'новоалтайск': 'novoaltajsk', 'новокузнецк': 'novokuznetsk', 'новокуйбышевск': 'novokuybyshevsk', 'новомосковск': 'novomoskovsk', 'новороссийск': 'novorossijsk', 'новосибирск': 'novosibirsk', 
            'новоуральск': 'novouralsk', 'новочебоксарск': 'novocheboksarsk', 'новошахтинск': 'novoshakhtinsk', 'новый уренгой': 'new_urengoy', 'ногинск': 'noginsk', 'норильск': 'norilsk', 
            'ноябрьск': 'noyabrsk', 'нягань': 'nyagan', 'обнинск': 'obninsk', 'одинцово': 'odintsovo', 'озерск': 'ozersk', 'озеры': 'ozeri', 'октябрьский': 'oktyabrskij', 'омск': 'omsk', 'орел': 'orel', 
            'оренбург': 'orenburg', 'орехово-зуево': 'orehovo_zuevo', 'орск': 'orsk', 'павлово': 'pavlovo', 'павловский посад': 'pavlovskiy_posad', 'пенза': 'penza', 'первоуральск': 'pervouralsk', 
            'пермь': 'prm', 'петергоф': 'petergof_spb1', 'петрозаводск': 'petrozavodsk', 'петропавловск-камчатский': 'petropavlovsk-kamchatskij', 'подольск': 'podolsk', 'прокопьевск': 'prokopyevsk', 
            'псков': 'pskov', 'пушкин': 'pushkin', 'пушкино': 'pushkino', 'пятигорск': 'pyatigorsk', 'раменское': 'ramenskoe', 'ревда': 'revda', 'реутов': 'reutov', 'ростов-на-дону': 'rostov-na-donu', 
            'рубцовск': 'rubtsovsk', 'руза': 'ruza', 'рыбинск': 'rybinsk', 'рязань': 'ryazan', 'салават': 'salavat', 'салехард': 'salehard', 'самара': 'samara', 'саранск': 'saransk', 'саратов': 'saratov', 
            'саров': 'sarov', 'севастополь': 'sevastopol', 'северодвинск': 'severodvinsk', 'североморск': 'severomorsk', 'северск': 'seversk', 'сергиев посад': 'sergiev_posad', 'серпухов': 'serpuhov', 
            'сестрорецк': 'sestroreck_spb', 'симферополь': 'simferopol', 'смоленск': 'smolensk', 'сокол': 'sokol_vologda', 'солнечногорск': 'solnechnogorsk', 'сосновый бор': 'sosnovij_bor', 'сочи': 'sochi', 
            'спасск-дальний': 'spassk_dalnij', 'ставрополь': 'stavropol', 'старый оскол': 'old_oskol', 'стерлитамак': 'sterlitamak', 'ступино': 'stupino', 'сургут': 'surgut', 'сызрань': 'syzran', 
            'сыктывкар': 'syktyvkar', 'таганрог': 'taganrog', 'тамбов': 'tambov', 'тверь': 'tver', 'тихвин': 'tihvin', 'тольятти': 'tolyatti', 'томск': 'tomsk', 'туапсе': 'tuapse', 'тула': 'tula', 
            'тюмень': 'tumen', 'улан-удэ': 'ulan_ude', 'ульяновск': 'ulyanovsk', 'уссурийск': 'ussurijsk', 'усть-илимск': 'ust_ilimsk', 'уфа': 'ufa', 'феодосия': 'feodosiya', 'фрязино': 'fryazino', 
            'хабаровск': 'habarovsk', 'ханты-мансийск': 'hanti_mansijsk', 'химки': 'chimki', 'чебоксары': 'cheboksary', 'челябинск': 'chelyabinsk', 'череповец': 'cherepovec', 'черкесск': 'cherkessk', 
            'чехов': 'chehov', 'чита': 'chita', 'шахты': 'shahti', 'щелково': 'shchelkovo', 'электросталь': 'electrostal', 'элиста': 'elista', 'энгельс': 'engels', 'южно-сахалинск': 'yuzhno-sakhalinsk', 
            'якутск': 'yakutsk', 'ялта': 'yalta', 'ярославль': 'yaroslavl'
        }
        try:
            ci = cities[user_city]
        except: 
            return ['Этот город не поддерживается'], 0
        self.cur.execute("UPDATE users SET city = '%s' WHERE user_id = %d" %(ci, self.User_id))
        return ['''Бот-афиша на связи

"кино ДАТА" - список фильмов в прокате с указанием даты в формате ДД-ММ-ГГГГ (например, 01-09-2019)

"ФИЛЬМ ДАТА МЕСТО" - расписание по данному фильму с указанием даты в формате ДД-ММ-ГГГГ. ФИЛЬМ - число, сгенерированное напротив каждого фильма в списке, МЕСТО (необязательный параметр) - ключевое слово, указывающее на расположение кинотеатра (например, метро)

"фильм ФИЛЬМ" - информация по выбранному фильму, где ФИЛЬМ - число напротив приведенных в списке.

"концерты сегодня/завтра/на ЧИСЛО дней" - список концертов с необязательным указанием дневного диапазона. Если дневной параметр не указан, выводит список наиболее ожидаемых грядущих мероприятий (на неделю)

"театр сегодня/завтра/на ЧИСЛО дней" - список спектаклей, аналогичен описанию выше

"выставки сегодня/завтра/на ЧИСЛО дней" - список выставок, аналогичен описанию выше

"выставка ВЫСТАВКА" - информация по выбранному мероприятию, где ВЫСТАВКА - число напротив приведенных записей в списке выставок

"рестораны МЕСТО" - список ресторанов с указанием ключевой точки месторасположения заведений

"ресторан РЕСТОРАН" - информация о выбранном ресторане, где РЕСТОРАН - число напротив записей в списке ресторанов

Значения командных слов, выделенных заглавными буквами, зависят непосредственно от пользователя'''], 1

    @open_close_2
    def films(self, user_time = datetime.datetime.now().strftime("%d-%m-%Y"), user_film = None, x = 0):    #ВЫДЕЛИТЬ ЯЧЕЙКУ ПОД ХРАНЕНИЕ АНГЛОЯЗЫЧНОГО НАЗВАНИЯ
        self.cur.execute("SELECT city FROM users WHERE user_id = %d" %self.User_id)
        city = self.cur.fetchone()[0]                                                                                                                 #Сделать числовые идентификаторы, дабы не набирать название фильма
        if user_time == self.Date:
            url = 'https://www.afisha.ru/%s/schedule_cinema/?view=list' %city
        else:
            url = 'https://www.afisha.ru/%s/schedule_cinema/%s/?view=list' %(city, user_time)
        param = {}
        page_k = 1
        film_name = 0
        while 1:
            s = requests.get(url, headers = self.Headers)
            b = bs4.BeautifulSoup(s.text, 'html.parser')
            if b.find('article', attrs = {'class': 'page__content object'}) == None:
                break
            #iterator = b.find('article', attrs = {'class': 'page__content object'})
            name = b.find_all('div', attrs = {'class': 'new-list__item-info'})
            content = b.find_all('div', attrs = {'class': 'new-list__item-content'})
            k = 0
            k2 = 1
            for i in name:
                film_name += 1
                text_nostr = i.find('a', attrs = {'class': 'new-list__item-link'})
                text = text_nostr.getText()
                param[film_name] = ['', '', '', '']                          #на 0 - название, 1 - жанр, 2 - режиссер, 3 - актеры, 5 - год/страна, 4 - ссылка в цифрах на фильм
                param[film_name][0] += text
                param[film_name].append(text_nostr.get('href')[6:])
                for value in content[k].find_all('div', attrs = {'class': 'new-list__item-record-value'}):
                    for j in value.find_all('a', attrs = {'class': 'link-list__item-link'}):
                        param[film_name][k2] += j.get_text() + ', '
                    k2 += 1
                year = i.find('div', attrs = {'class': 'new-list__item-status'})
                param[film_name].append(year.getText())
                k += 1
                k2 = 1
            page_k += 1
            page_temp = 'page%d' %page_k
            print(url)
            if user_time == self.Date: url = 'https://www.afisha.ru/%s/schedule_cinema/%s/?view=list' %(city, page_temp)
            else: url = 'https://www.afisha.ru/%s/schedule_cinema/%s/%s/?view=list' %(city, user_time, page_temp)
        with open('id%s.txt' %self.User_id, 'w') as book:
            for i in param.keys():
                book.write(str(i) + ' ' + param[i][4] + '\n')

        if x:
            try:
                user_film = int(user_film)
                #print(user_film)
                with open('id%s.txt' %self.User_id) as book:
                    shedule = book.readlines()
                #print(shedule)
                link_list = []
                for i in range(len(shedule)):
                    link = shedule[i].rstrip('\n').split(' ')
                    link_list.append(link[1])
                #print(link_list)
                try: 
                    res = link_list[user_film - 1]
                    return 1, res
                except:
                    return 0, ['Указан неверный номер']
            except:
                for i in param.keys():
                    if user_film.lower() == param[i][0].lower():
                        res = param[i][4]
                        return 1, res
                else:
                    return 0, 0
        return self.output_result(param, 1), param

    @open_close_1
    def shedule_film(self, res, user_time, user_place = ' '):
        self.cur.execute("SELECT city FROM users WHERE user_id = %d" %self.User_id)
        city = self.cur.fetchone()[0]
        if user_time == self.Date: url = 'https://www.afisha.ru/%s/schedule_cinema_product%s' %(city, res)
        else: url = 'https://www.afisha.ru/%s/schedule_cinema_product%s%s' %(city, res, user_time)
        print(url)
        cinema_dict = {}
        page_k = 1
        while 1:
            s = requests.get(url, headers = self.Headers)
            b = bs4.BeautifulSoup(s.text, 'html.parser')
            if b.find('div', attrs = {'class': 'content content_view_list'}) == None: break 
            iterator = b.find('div', attrs = {'class': 'content content_view_list'}).find_all('li', attrs = {'class': 'unit__schedule-row'})
            k = k2 = 0
            for i in iterator:
                cinema = i.find('a', attrs = {'class': 'unit__movie-name__link'}).getText()
                cinema_dict[cinema] = ['']                                            #на 0 месте - время сеансов, 1 - ссылка на кинотетатр, 2 - адрес, 3 - ссылка
                link_cinema = i.find('a', attrs = {'class': 'unit__movie-name__link'})
                cinema_dict[cinema].append(link_cinema.get('href'))
                address_cinema = i.find('div', attrs = {'class': 'unit__movie-location'})
                cinema_dict[cinema].append(address_cinema.getText())
                link_url = 'https://www.afisha.ru%s' %cinema_dict[cinema][1]
                s2 = requests.get(link_url, headers = self.Headers)
                b2 = bs4.BeautifulSoup(s2.text, 'html.parser')
                link = b2.find('section', attrs = {'class': 'object__content'}).find('div', attrs = {'class': 'object__block-meta'}).find('link', attrs = {'itemprop': 'sameAs'})
                if link.get('href') == None: cinema_dict[cinema].append('сайта нет')
                else: cinema_dict[cinema].append('https://www.afisha.ru' + link.get('href'))
                if iterator[k].find('li', attrs = {'class': 'tooltip timetable__item'}) == None:
                    for value in iterator[k].find('li', attrs = {'class': 'tooltip timetable__item timetable__item_disabled'}).find_all('time', attrs = {'class': 'timetable__item-time'}):
                        try: cinema_dict[cinema][0] += value.get_text() + ' (в кассах), '
                        except: pass
                for value in iterator[k].find_all('li', attrs = {'class': 'tooltip timetable__item'}):
                    cinema_dict[cinema][0] += value.find('time', attrs = {'class': 'timetable__item-time'}).getText() + ', '
                    if value.find('small', attrs = {'class': 'tooltip__body'}) and '3D' in value.find('small', attrs = {'class': 'tooltip__body'}).getText():
                        cinema_dict[cinema][0] += cinema_dict[cinema][0] + ' - 3D, '
                    elif value.find('small', attrs = {'class': 'tooltip__body'}) and '4DX' in value.find('small', attrs = {'class': 'tooltip__body'}).getText():
                        cinema_dict[cinema][0] += cinema_dict[cinema][0] + ' - 4DX, '
                    k2 += 1
                k2 = 0
                k += 1
            page_k += 1
            page_temp = 'page%d' %page_k
            if user_time == self.Date: url = 'https://www.afisha.ru/%s/schedule_cinema_product%s%s' %(city, res, page_temp)
            else: url = 'https://www.afisha.ru/%s/schedule_cinema_product%s%s/%s' %(city, res, user_time, page_temp)
        return self.output_result(cinema_dict, 2)

    def films_info(self, user_film):
        url = 'https://www.afisha.ru/movie/?sort=name&view=list'
        link_list = []
        try: 
            user_film = int(user_film)
            with open('id%s.txt' %self.User_id) as book:
                film = book.readlines()
            for i in range(len(film)):
                link = film[i].rstrip('\n').split(' ')
                link_list.append(link[1])
            try: 
                res = link_list[user_film - 1]
            except:
                return ['Указан неверный номер'], 0
        except:
            user_film = user_film.split(' ')
            user_film = '_'.join(user_film)
            return ['https://ru.wikipedia.org/wiki/%s' %user_film]
        url = 'https://afisha.ru/movie%s' %res
        #print(url)
        s = requests.get(url, headers = self.Headers)
        b = bs4.BeautifulSoup(s.text, 'html.parser')
        iterator = b.find('div', attrs = {'class': 'info-widget object__block row'})
        k = 0
        cinema_desc = ['', '', '']          #0 - жанр, 1 - актеры, 2 - режиссеры, 3 - кр.описание, 4 - полное, 5 - возраст, 6 - длительность, 7 - дата выхода
        #print(iterator.find_all('li', attrs = {'class': 'info-widget__meta-item'})[0].getText())
        if b.find('div', attrs = {'class': 'director director_single object__block object__block_grey'}):
            for i in b.find('div', attrs = {'class': 'director director_single object__block object__block_grey'}).find_all('span', attrs = {'itemprop': 'name'}):
                cinema_desc[2] += i.getText() + ', '
        elif 'Режиссер:' in iterator.find_all('li', attrs = {'class': 'info-widget__meta-item'})[0].getText():
            cinema_desc[2] += iterator.find_all('li', attrs = {'class': 'info-widget__meta-item'})[0].find('a').getText() + ', '
            k += 1
        else:
            cinema_desc[2] += 'отсутствует, '         
        if iterator.find('h2', attrs = {'class': 'info-widget__header'}):
            cinema_desc.append(iterator.find('h2', attrs = {'class': 'info-widget__header'}).getText())
        else: 
            cinema_desc.append(b.find('article', attrs = {'class': 'page__content object'}).find('span', attrs = {'class': 'name___15--1'}).getText())
        cinema_desc.append(iterator.find('p', attrs = {'class': 'info-widget__description'}).getText())
        #cinema_desc.append(iterator.find('li', attrs = {'class': 'info-widget__meta-item info-widget__meta-item_genres'}).find('span', attrs = {'itemprop': 'genre'}).getText())
        a = iterator.find('span', attrs = {'class': 'info-widget__meta-item_part'}).getText()
        cinema_desc.append(a)
        #print(iterator.find_all('li', attrs = {'class': 'info-widget__meta-item'})[1])
        cinema_desc.append(iterator.find_all('li', attrs = {'class': 'info-widget__meta-item'})[1].find_all('span')[1].getText())
        #print(cinema_desc)
        cinema_desc.append(iterator.find('time').getText())
        #print(cinema_desc)
        for i in iterator.find('li', attrs = {'class': 'info-widget__meta-item info-widget__meta-item_genres'}).find_all('span', attrs = {'itemprop': 'genre'}):
            cinema_desc[0] += i.getText() + ', '
        if b.find_all('div', attrs = {'class': 'main-actors__actor'}):
            for i in b.find_all('div', attrs = {'class': 'main-actors__actor'}):
                cinema_desc[1] += i.find('span', attrs = {'itemprop': 'name'}).getText() + ', '
        else: 
            pass
        #print(cinema_desc)
        if b.find('div', attrs = {'class': 'other-actors'}):
            for i in b.find('div', attrs = {'class': 'other-actors'}).find_all('span', attrs = {'itemprop': 'name'}):
                cinema_desc[1] += i.getText() + ', '
        else: 
            cinema_desc[1] += 'отсутствуют, '
        #print(cinema_desc[1])
        #print(b.find('div', attrs = {'class': 'director director_single object__block object__block_grey'}))
        #print(cinema_desc)
        description = [
            cinema_desc[3] + '\n\n' + cinema_desc[0][:len(cinema_desc[0])-2] + ' | ' + cinema_desc[5] + ' | ' + cinema_desc[6] + ' | дата выхода: ' + cinema_desc[7] + '\n\n' + cinema_desc[4]
            + '\n\nРежиссер: ' + cinema_desc[2][:len(cinema_desc[2])-2] + '\nАктеры: ' + cinema_desc[1][:len(cinema_desc[1])-2]
        ]
        return description

    @open_close_1
    def concerts(self, x, on_days = None):                                             #Сделать выдачу расписания на задаваемое количество дней вперед (на 2 дня и прочее)
        self.cur.execute("SELECT city FROM users WHERE user_id = %d" %self.User_id)
        city = self.cur.fetchone()[0]                                       
        if x: url = 'https://www.afisha.ru/%s/schedule_concert/vybor-afishi/?view=list' %city
        else: url = 'https://www.afisha.ru/%s/schedule_concert/%s/?view=list' %(city, on_days)
        concert_dict = {}                                          #0 - адрес, 1 - время, 2 - жанр, 3 - участники
        k = 0
        page_k = 1
        while 1:
            s = requests.get(url, headers = self.Headers)
            b = bs4.BeautifulSoup(s.text, 'html.parser')
            if b.find('section', attrs = {'class': 'object__content'}) == None:           #Ограничитель по страницам
                break
            iterator = b.find('section', attrs = {'class': 'object__content'}).find_all('div', attrs = {'class': 'new-list__item concert-item'})
            for i in iterator:
                #if not i.find('div', attrs = {'class': 'afisha-choice'}) or i.find('div', attrs = {'class': 'afisha-choice'}).get('title') != 'Выбор «Афиши»':
                    #boolean = 0
                    #break
                concert = i.find('a', attrs = {'class': 'new-list__item-link'}).getText()
                concert_dict[concert] = ['', '', '', '']
                for value in i.find_all('div', attrs = {'class': 'new-list__item-record'}):        #ЧЕРЕЗ record-value
                    if k != 1: #value.find_all('a', attrs = {'class': 'link-list__item-link'}):
                        for value_item in value.find_all('a', attrs = {'class': 'link-list__item-link'}):
                            concert_dict[concert][k] += value_item.get_text() + ', '
                    else: concert_dict[concert][k] += value.find('div', attrs = {'class': 'new-list__item-record-value-chank'}).getText()
                    k += 1
                k = 0
            page_k += 1
            page_temp = 'page%d' %page_k
            if x: url = 'https://www.afisha.ru/%s/schedule_concert/vybor-afishi/%s/?view=list' %(city, page_temp)
            else: url = 'https://www.afisha.ru/%s/schedule_concert/%s/%s/?view=list' %(city, on_days, page_temp)
        return self.output_result(concert_dict, 3)                                

    @open_close_1
    def theatre(self, x, on_days = None):
        self.cur.execute("SELECT city FROM users WHERE user_id = %d" %self.User_id)
        city = self.cur.fetchone()[0]                                           
        if x: url = 'https://www.afisha.ru/%s/schedule_theatre/vybor-afishi/?view=list' %city
        else: url = 'https://www.afisha.ru/%s/schedule_theatre/%s/?view=list' %(city, on_days)
        theatre_dict = {}                                          #0 - адрес, 1 - время, 2 - жанр, 3 - режиссер, 4 - актеры
        k = 0
        page_k = 1
        print(url)
        while 1:
            s = requests.get(url, headers = self.Headers)
            b = bs4.BeautifulSoup(s.text, 'html.parser')
            #print(b.find('section', attrs = {'class': 'object__content'}).find_all('div', attrs = {'class': 'new-list__item exhibition-item'}))
            if b.find('section', attrs = {'class': 'object__content'}) == None:           #Ограничитель по страницам
                break
            iterator = b.find('section', attrs = {'class': 'object__content'}).find_all('div', attrs = {'class': 'new-list__item exhibition-item'})
            for i in iterator:
                #print(i)
                theatre = i.find('a', attrs = {'class': 'new-list__item-link'}).getText()
                theatre_dict[theatre] = ['', '', '', '', '']
                #print(theatre_dict)
                for value in i.find_all('div', attrs = {'class': 'new-list__item-record'}):        #ЧЕРЕЗ record-value
                    if k != 1:
                        for value_item in value.find_all('a', attrs = {'class': 'link-list__item-link'}):
                            theatre_dict[theatre][k] += value_item.get_text() + ', '
                    else: theatre_dict[theatre][k] += value.find('div', attrs = {'class': 'new-list__item-record-value-chank'}).getText()
                    k += 1
                k = 0
                for i in range(5):
                    if theatre_dict[theatre][i] == '': theatre_dict[theatre][i] += 'отсутствует, '
            page_k += 1
            page_temp = 'page%d' %page_k
            if x: url = 'https://www.afisha.ru/%s/schedule_theatre/vybor-afishi/%s/?view=list' %(city, page_temp)
            else: url = 'https://www.afisha.ru/%s/schedule_theatre/%s/%s/?view=list' %(city, on_days, page_temp)
        return self.output_result(theatre_dict, 4)

    @open_close_1
    def exhibition(self, x, on_days = None):
        self.cur.execute("SELECT city FROM users WHERE user_id = %d" %self.User_id)
        city = self.cur.fetchone()[0]                                            
        if x: url = 'https://www.afisha.ru/%s/schedule_exhibition/vybor-afishi/?view=list' %city
        else: url = 'https://www.afisha.ru/%s/schedule_exhibition/%s/?view=list' %(city, on_days)
        exhib_dict = {}                                          #0 - название, 1 - адрес, 4 - кр.описание, 2 - время, 3 - жанр, 5 - ссылка
        k = 1
        page_k = 1
        print(url)
        while 1:
            s = requests.get(url, headers = self.Headers)
            b = bs4.BeautifulSoup(s.text, 'html.parser')
            #print(b.find('section', attrs = {'class': 'object__content'}).find_all('div', attrs = {'class': 'new-list__item exhibition-item'}))
            if b.find('section', attrs = {'class': 'object__content'}) == None:           #Ограничитель по страницам
                break
            iterator = b.find('section', attrs = {'class': 'object__content'}).find_all('div', attrs = {'class': 'new-list__item exhibition-item'})
            name = 0
            for i in iterator:
                #print(i)
                name += 1
                exhib = i.find('a', attrs = {'class': 'new-list__item-link'}).getText()
                exhib_dict[name] = ['', '', '', '']
                exhib_dict[name][0] = exhib
                exhib_dict[name].append(i.find('div', attrs = {'class': 'new-list__item-verdict'}).getText())
                exhib_dict[name].append(i.find('a', attrs = {'class': 'new-list__item-link'}).get('href')[11:])
                #print(theatre_dict)
                for value in i.find_all('div', attrs = {'class': 'new-list__item-record'}):        #ЧЕРЕЗ record-value
                    if k != 2:
                        for value_item in value.find_all('a', attrs = {'class': 'link-list__item-link'}):
                            exhib_dict[name][k] += value_item.get_text() + ', '
                    else: exhib_dict[name][k] += value.find('div', attrs = {'class': 'new-list__item-record-value-chank'}).getText()
                    k += 1
                k = 1
                for i in range(1, 5):
                    if exhib_dict[name][i] == '': exhib_dict[name][i] += 'отсутствует, '
            page_k += 1
            page_temp = 'page%d' %page_k
            if x: url = 'https://www.afisha.ru/%s/schedule_exhibition/vybor-afishi/%s/?view=list' %(city, page_temp)
            else: url = 'https://www.afisha.ru/%s/schedule_exhibition/%s/%s/?view=list' %(city, on_days, page_temp)

        with open('id%s.txt' %self.User_id, 'w') as book:
            for i in exhib_dict.keys():
                book.write(str(i) + ' ' + exhib_dict[i][5] + '\n')

        return self.output_result(exhib_dict, 5)
    
    def exhibition_info(self, user_exhib):
        user_exhib = int(user_exhib)
        exhib_list = ['', '', '', '', '', '', '', '']                                                     #0 - жанр, 1 - описание, 2 - сайт, 3 - телефон, 4 - адрес, 5 - стоимость, 6 - режим работы
        link_list = []                                                                                    #ЗАПОЛНИТЬ СРАЗУ ТИРЕ
        with open('id%s.txt' %self.User_id) as book:                        #СТОИМОСТЬ                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            film = book.readlines()                                                                     #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for i in range(len(film)):
            link = film[i].rstrip('\n').split(' ')
            link_list.append(link[1])
        try: 
            res = link_list[user_exhib - 1]
        except:
            return ['Указан неверный номер']
        url = 'https://www.afisha.ru/exhibition%s' %res
        print(url)
        s = requests.get(url, headers = self.Headers)
        b = bs4.BeautifulSoup(s.text, 'html.parser')
        iterator = b.find('section', attrs = {'class': 'object__content'})
        #print(iterator.find('div', attrs = {'class': 'object__block-content'}).find('p', attrs = {'itemprop': 'description'}))
        #print(b.find('section', attrs = {'class': 'object__content'}).find_all('div', attrs = {'class': 'object__block-content'})[1].find('p', attrs = {'itemprop': 'description'}))
        if iterator.find('div', attrs = {'class': 'object__block-content'}).find('p', attrs = {'itemprop': 'description'}):
            exhib_list[0] = iterator.find('div', attrs = {'class': 'object__block-content'}).find('p', attrs = {'itemprop': 'description'}).getText()
        elif iterator.find_all('div', attrs = {'class': 'object__block-content'})[1].find('p', attrs = {'itemprop': 'description'}):
            exhib_list[0] = iterator.find_all('div', attrs = {'class': 'object__block-content'})[1].find('p', attrs = {'itemprop': 'description'}).getText()
        else:
            exhib_list[0] = iterator.find('h2', attrs = {'itemprop': 'description'}).getText()
        for i in iterator.find('li', attrs = {'class': 'info-widget__meta-item info-widget__meta-item_genres'}).find_all('a'):
            exhib_list[1] += i.getText() + ', '
        iterator = iterator.find('div', attrs = {'itemprop': 'location'})
        if iterator.find('link', attrs = {'itemprop': 'sameAs'}).get('href'):
            exhib_list[2] = 'https://www.afisha.ru' + iterator.find('link', attrs = {'itemprop': 'sameAs'}).get('href')
        else: exhib_list[2] = 'сайт не указан'
        #print(exhib_list)
        exhib_list[3] = iterator.find('meta', attrs = {'itemprop': 'telephone'}).get('content')
        #print(exhib_list)
        exhib_list[4] = iterator.find('label', attrs = {'itemprop': 'streetAddress'}).getText()
        #print(exhib_list)
        k = 0
        for i in iterator.find_all('div', attrs = {'class': 'unit__row'})[1].find_all('span', attrs = {'class': 'unit__col-label'}):
            #print(i)
            if i.getText() == 'цена': exhib_list[5] = iterator.find_all('div', attrs = {'class': 'unit__row'})[1].find_all('span', attrs = {'class': 'unit__col-value'})[k].getText()
            elif i.getText() == 'режим работы': exhib_list[6] = iterator.find_all('div', attrs = {'class': 'unit__row'})[1].find_all('span', attrs = {'class': 'unit__col-value'})[k].getText()
            k += 1
        for i in range(7):
            if not exhib_list[i]: exhib_list[i] = ' - '

        description = [
            exhib_list[0] + '\n\n' + 'Жанр: ' + exhib_list[1][:len(exhib_list[1])-2] + '\n\n' + exhib_list[4] + '\n' + exhib_list[3] + '\n\nЦена: ' + exhib_list[5] + 
            '\nРежим работы: ' + exhib_list[6] + '\n\n' + exhib_list[2]
        ]
        return description
        
    @open_close_1
    def restaurants(self, user_rest):
        self.cur.execute("SELECT city FROM users WHERE user_id = %d" %self.User_id)
        city = self.cur.fetchone()[0]
        user_rest = user_rest.split(' ')
        user_r = user_rest[0]
        for i in user_rest[1:]:
            user_r += '+' + i
        url = 'https://www.afisha.ru/%s/restaurants/restaurant_list/?q=%s' %(city, user_r)
        s = requests.get(url, headers = self.Headers)
        b = bs4.BeautifulSoup(s.text, 'html.parser')
        if not b.find('div', attrs = {'class': 'results'}):
            return ['По вашему запросу ничего не найдено']
        rest_dict = {}
        k = 0
        page_k = 1
        while 1:
            s = requests.get(url, headers = self.Headers)
            b = bs4.BeautifulSoup(s.text, 'html.parser')
            if not b.find('div', attrs = {'class': 'results'}):
                break
            iterator = b.find('section', attrs = {'class': 'search_results'}).find_all('span', attrs = {'class': 'places_cards'})
            for i in iterator:
                k += 1
                rest_dict[k] = []                                                                           #0 - имя, 1 - тег, 2 - адрес. 3 - цена в чеке, 4 - ссылка
                rest_dict[k].append(i.get('data-restaurant-name'))
                rest_dict[k].append(i.find('ul', attrs = {'class': 'places-tag_items'}).getText().strip('\n'))
                rest_dict[k].append(i.find('span', attrs = {'class': 'places_metro'}).getText().replace('\n', '').strip(' ') + ', ' + i.find('span', attrs = {'class': 'places_address'}).getText().replace('\n', '').strip(' '))
                if i.find('span', attrs = {'class': 'range s-tooltip'}):
                    rest_dict[k].append(i.find('span', attrs = {'class': 'range s-tooltip'}).get('data-title'))
                else: rest_dict[k].append('средняя цена не указана')
                rest_dict[k].append(i.get('data-restaurant-id'))
            page_k += 1
            page = 'page%d' %page_k
            url = 'https://www.afisha.ru/%s/restaurants/restaurant_list/%s/?q=%s' %(city, page, user_r)
        with open('id%s.txt' %self.User_id, 'w') as book:
            for i in rest_dict.keys():
                book.write(str(i) + ' ' + rest_dict[i][4] + '\n')
        return self.output_result(rest_dict, 6)

    @open_close_1
    def restaurants_info(self, user_rest):
        link_list = []
        try: 
            user_rest = int(user_rest)
            with open('id%s.txt' %self.User_id) as book:
                film = book.readlines()
            for i in range(len(film)):
                link = film[i].rstrip('\n').split(' ')
                link_list.append(link[1])
            try: 
                res = link_list[user_rest - 1]
            except:
                return ['Указан неверный номер'], 0
        except:
            ['По вашему запросу ничего не найдено']
        self.cur.execute("SELECT city FROM users WHERE user_id = %d" %self.User_id)
        city = self.cur.fetchone()[0]
        url = 'https://www.afisha.ru/%s/restaurant/%s/' %(city, res)
        print(url)
        s = requests.get(url, headers = self.Headers)
        b = bs4.BeautifulSoup(s.text, 'html.parser')
        iterator = b.find('section', attrs = {'class': 'detail'})
        #print(iterator)
        info_dict = {}
        description = ['', '']
        for i in iterator.find_all('li', attrs = {'class': 'detail_column'}):
            if i.find('span'):
                info_dict[i.find('a').getText()] = i.find('span').getText() + '\n'
        #print('Скидка на меню - ' + info_dict['Скидка на меню'] + 'Завтраки - ' + info_dict['Завтраки'] + 'Вайфай - ' + info_dict['Вайфай'] + 'Доставка - ' + info_dict['Доставка'])
        description[0] = 'Скидка на меню - ' + info_dict['Скидка на меню'] + 'Завтраки - ' + info_dict['Завтраки'] + 'Вайфай - ' + info_dict['Вайфай'] + 'Доставка - ' + info_dict['Доставка']
        #print(description[0])
        iterator = b.find('section', attrs = {'class': 'rest-tags'})
        for i in iterator.find_all('li', attrs = {'class': 'rest-tags_item'}):
            description[1] += i.find('a').getText().strip(' ').replace('\n', '') + ', '
            print(description[1])
        description[1] = description[1][:len(description[1])-2]
        iterator = b.find('section', attrs = {'class': 'contact'})
        for i in iterator.find_all('li', attrs = {'class': 'contact_item'}):
            if len(i.find_all('span', attrs = {'class': 'contact_sense'})) > 1:
                description.append(i.find_all('span', attrs = {'class': 'contact_sense'})[1].getText())
            else:
                description.append(i.find('span', attrs = {'class': 'contact_sense'}).getText().strip(' ').replace('\n', ''))
        stroka = ''
        for j in description:
            stroka += j + '\n'
        return [stroka]
