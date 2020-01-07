from function import Afisha
import datetime

class vkbot:
    def __init__(self, user_id):
        self.User_id = user_id
        self.Commands = ('начать', 'кино', 'концерты', "сегодня", "завтра", "на", "фильм", "театр", "выставки", "выставка", "рестораны", "ресторан", "город")
        self.Exception = ("I don't know what you need", "Некорректный ввод")

    def new_msg(self, message):
        func = Afisha(self.User_id)
        country, b = func.confirm(message.lower())
        if message.lower() == self.Commands[0]:
            a = func.start()
            return a
        elif message.lower()[:5] == self.Commands[12]:
            country, b = func.confirm(message.lower()[6:])
            return country
        elif self.Commands[1] in message.lower():
            array = message.lower().split(' ')               
            try: film, a = func.films(array[1])
            except: return self.Exception[1:]
            return film 
        elif self.Commands[6] in message.lower():
            try: film = func.films_info(message.lower()[6:])
            except: return self.Exception[1:]
            return film
        elif self.Commands[9] in message.lower():
            try: desc = func.exhibition_info(message.lower()[9:])
            except: return self.Exception[1:]
            return desc
        elif self.Commands[10] in message.lower():
            try: rest = func.restaurants(message[10:])
            except: return self.Exception[1:]
            return rest
        elif self.Commands[11] in message.lower():
            desc = func.restaurants_info(message[9:])
            #except: return self.Exception[1:]
            return desc

        elif (self.Commands[7] in message.lower()) or (self.Commands[2] in message.lower()) or (self.Commands[8] in message.lower()):
            array = message.lower().split(' ')
            if self.Commands[7] in message.lower(): temp = 'theatre'
            elif self.Commands[2] in message.lower(): temp = 'concerts'
            else: temp = 'exhibition'
            if array[-1] == self.Commands[3]:
                try: concert = eval('func.%s(0, "na-segodnya")' %temp)
                except: return self.Exception[1:]
                return concert
            elif array[-1] == self.Commands[4]:
                try: concert = eval('func.%s(0, "na-zavtra")' %temp)
                except: return self.Exception[1:]
                return concert
            elif len(array) > 2 and array[-3] == self.Commands[5]:
                date1 = datetime.datetime.now()
                try:
                    date2 = (date1 + datetime.timedelta(days = int(array[-2]))).strftime("%d-%m")
                    date = date1.strftime("%d-%m") + "_" + date2
                    concert = eval('func.%s(0, date)' %temp)
                except: return self.Exception[1:]
                return concert
            else:
                try: concert = eval('func.%s(1)' %temp)
                except: return self.Exception[1:]
                return concert
        else:
            array = message.lower().split(' ')    
            name = message.split(' ')
            #print(array)
            temp = name[0]                                   #СДЕЛАТЬ упрощение введения названий фильмов (проверка процентов ввода человеком с ключами словаря)
            if len(array) >= 3:
                if len(array) == 4:
                    array.pop(-2)
                try:
                    temp = int(temp)
                    a, b = func.films(array[1], temp, 1)
                    if a:
                        shedule = func.shedule_film(b, array[1], array[2])
                        return shedule
                    else: return b
                except:
                    for name_temp in name[1:len(name)-2]:
                        a, b = func.films(array[1], temp, 1)
                        if a: 
                            shedule = func.shedule_film(b, array[1], array[2])   #Обработка составных названий СДЕЛАТЬ ПОИСК ВСЕХ СЛОВ ДО ВХОЖДЕНИЯ ГОРОДА
                            return shedule
                        temp += ' ' + name_temp
                    return self.Exception[1:]
            else:
                try: 
                    temp = int(temp)
                    a, b = func.films(array[1], temp, 1)
                    if a:
                        shedule = func.shedule_film(b, array[1])
                        return shedule
                    else: return b
                except:
                    for name_temp in name[1:len(name)-1]:
                        try: a, b = func.films(array[1], temp, 1)
                        except: self.Exception[:1] 
                        if a:
                            shedule = func.shedule_film(b, array[1])   #Обработка составных названий СДЕЛАТЬ ПОИСК ВСЕХ СЛОВ ДО ВХОЖДЕНИЯ ГОРОДА
                            return shedule
                        temp += ' ' + name_temp
                    else: return self.Exception[1:]
                    #temp += ' ' + name_temp
                #try: concert, a = func.concerts(array[-1])
                #for name_temp in name[1:len(name)-1]:

            #else:
                #return self.Exception[:1]
