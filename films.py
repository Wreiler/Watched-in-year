import re
import pandas as pd
from IPython.display import HTML, display
from datetime import datetime


def input_film():
    with open('films2021.txt', 'a+', encoding='utf-8') as f:
        p = input('Последний просмотренный фильм или сериал: ')
        if p == '':
            pass
        else:
            if re.search('сезон', p):
                num = re.search('сезон', p).start()
                f.write(p[:num].title() + p[num:])
            else:
                f.write(p.title())
        date = input('Дата просмотра последнего фильма или сериала (DD-MM): ')
        if date == '':
            pass
        else:
            date = date.split('-')
            s = f" [{date[0]}-{date[1]}-2021]"
            f.write(s + '\n')


def analys():
    global films, shows, filmlist, showlist, last_date
    films = 0
    shows = 0
    filmlist = []
    showlist = []
    last_date = ['', '']
    with open('films2021.txt', encoding='utf-8') as f:
        for i in f:
            if i != '':
                i = i.split()
                k = i[:-1]
                if re.search('сезон', ' '.join(k)):
                    shows += 1
                    showlist.append(k)
                    last_date[1] = i[-1]
                else:
                    films += 1
                    filmlist.append(k)
                    last_date[0] = i[-1]


def film_word(n):
    if len(str(n)) > 1:
        if str(n)[-1] in '234' and int(str(n)[-2]) != 1:
            return 'фильма'
        elif str(n)[-1] == '1' and int(str(n)[-2]) != 1:
            return 'фильм'
        return 'фильмов'
    if str(n)[-1] in '234':
        return 'фильма'
    elif str(n)[-1] == '1':
        return 'фильм'
    return 'фильмов'


def count_films():
    total = films
    print(f'Вы посмотрели {total} {film_word(total)} с начала 2021-го года')

    pom = 300 - total
    if pom > 0:
        print(f'\n\nДо цели осталось посмотреть {pom} {film_word(pom)} до конца этого года!'.upper())
    else:
        print(f'\n\nЦель посмотреть 300 {film_word(300)} до конца этого года выполнена!'.upper())


def count_ser():
    print(f'Вы посмотрели {shows} сериалов с начала 2021-го года')


lf = ''
ls = ''


def last_film():
    global lf, last_date
    lf = '"' + ' '.join(filmlist[-1]) + '"' if filmlist != [] else 'отсутствует'
    ldf = last_date[0] if filmlist != [] else '[xx-xx-xxxx]'
    print(f'Последний просмотренный фильм на сегодняшний день - ' + lf)
    print('Просмотрен: ' + ldf)


def last_show():
    global ls
    ls = '"' + ' '.join(showlist[-1]) + '"' if showlist != [] else 'отсутствует'
    lds = last_date[1] if showlist != [] else '[xx-xx-xxxx]'
    print(f'Последний просмотренный сериал (сезон сериала) на сегодняшний день - ' + ls)
    print('Закончен просмотр: ' + lds)


def all_films():
    res = [' '.join(x) for x in filmlist]
    res.sort()
    for i in res:
        print(i.upper().center(len(lf) + 8, '-') if i == lf else i.title())


def ser_res():
    res = [' '.join(x) for x in showlist]
    res.sort()
    for i in res:
        print(i)

    n = sum([1 if x[-1] == 'сезон)' else int(x[-2][1]) for x in [i.split() for i in res]])
    print(f'\nВсего сезонов: {n}')

    
def svod_table(n):
    global films, shows, filmlist, showlist, last_date
    dates = [[], []]
    with open('films2021.txt', encoding='utf-8') as f:
        for i in f:
            if i != '':
                i = i.split()
                k = i[:-1]
                if re.search('сезон', ' '.join(k)):
                    dates[1].append(datetime.strptime(i[-1][1:-1], '%d-%m-%Y'))
                else:
                    dates[0].append(datetime.strptime(i[-1][1:-1], '%d-%m-%Y'))
    films_for_use = [' '.join(i) for i in filmlist]
    shows_for_use = [' '.join(i) for i in showlist]
    films_set = {(films_for_use[x].upper(), dates[0][x]) if dates[0][x]==last_date[0][1:-1] 
                  else (films_for_use[x], dates[0][x]) for x in range(len(filmlist))}
    show_set = {(shows_for_use[x].upper(), dates[1][x]) if dates[1][x]==last_date[1][1:-1] 
                  else (shows_for_use[x], dates[1][x]) for x in range(len(showlist))}
    
    # Для фильмов
    if n == 1:
        films_dict = {x[0]: x[1] for x in sorted(films_set, key=lambda x: x[1])}
    elif n == 2: 
        films_dict = {x[0]: x[1] for x in sorted(films_set, key=lambda x: x[0])}
    films_dict = {x: datetime.strftime(films_dict[x], '%d-%m-%Y') for x in films_dict}
    lfilm = films_for_use[-1]
    tabf = pd.DataFrame.from_dict(films_dict, orient='index', columns=['Дата просмотра']).reset_index()
    tabf.rename(columns={'index': 'Фильм', 0: 'Дата просмотра'}, inplace=True)
    tabf.rename(index = lambda x: x+1, inplace=True)
    f = tabf.style.set_properties(**{'background-color': '#222430', 
                                     'color': '#95abab',
                                     'border-style': 'solid',
                                     'border-width': '1px',
                                     'border-color': '#733737',
                                     'max-width': '450px',
                                     'font-size': '10pt',
                                     'text-align': 'center'})
    def check_last(df, com, ind, last):
        """Передается датафрейм, комманда стиля, индекс в списке даты (фильм/сериал), 
        последний фильм/сериал"""
        df.apply(lambda x: [com if i==last_date[ind][1:-1] or i==last else '' for i in x])
        
    for k in ['font-weight: bold', 'font-style: italic', 'background-color: #6e2626']:
        check_last(f, k, 0, lfilm)
    f = f.render()
    display(HTML(f))
    
    # Для сериалов
    if show_set != set():
        if n == 1:
            show_dict = {x[0]: x[1] for x in sorted(show_set, key=lambda x: x[1])}
        elif n == 2:
            show_dict = {x[0]: x[1] for x in sorted(show_set, key=lambda x: x[0])}
        show_dict = {x: datetime.strftime(show_dict[x], '%d-%m-%Y') for x in show_dict}
        lshow = shows_for_use[-1]
        tabs = pd.DataFrame.from_dict(show_dict, orient='index', columns=['Дата просмотра']).reset_index()
        tabs.rename(columns={'index': 'Сериал', 0: 'Дата просмотра'}, inplace=True)
        tabs.rename(index = lambda x: x+1, inplace=True)
        s = tabs.style.set_properties(**{'background-color': '#222430', 
                                     'color': '#95abab',
                                     'border-style': 'solid',
                                     'border-width': '1px',
                                     'border-color': '#733737',
                                     'max-width': '450px',
                                     'font-size': '10pt',
                                     'text-align': 'center',
                                     'font': 'TimesNewRoman'})
        for j in ['font-weight: bold', 'font-style: italic', 'background-color: #6e2626']:
            check_last(s, j, 1, lshow)
        s = s.render()
        display(HTML(s))
