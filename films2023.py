import re
import pandas as pd
from IPython.display import HTML, display
from datetime import datetime


def input_film():
    with open('films2023.txt', 'a+', encoding='utf-8') as f:
        req = 'n'
        while req == 'n':
            p = input('Last watched movie or TV series: ')
            if p == '':
                pass
            else:
                if re.search('season', p):
                    num = re.search('season', p).start()
                    m = p[:num] + p[num:]
                else:
                    m = p
            date = input('Date of last watched movie or TV series (DD.MM): ')
            if date == '':
                pass
            else:
                d = f" [{date}.2023]"
            flag = input('First time watched (F - default) or rewatched (R) (*for movies*): ').upper()
            if flag == '':
                s = " [F]"
            else:
                s = f" [{flag}]"
            req = input('Save or reinter (y/n): ').lower()
            if req == '': req = 'y'
        f.write(m)
        f.write(d)
        f.write(s + '\n')


def analys():
    global films, shows, filmlist, showlist, last_date
    films = 0
    shows = 0
    filmlist = []
    showlist = []
    last_date = ['', '']
    with open('films2023.txt', encoding='utf-8') as f:
        for i in f:
            if i != '':
                i = i.split()
                k = i[:-1]
                if re.search('season', ' '.join(k)):
                    shows += 1
                    showlist.append(k)
                    last_date[1] = i[-1]
                else:
                    k = i[:-2]
                    films += 1
                    filmlist.append(k)
                    last_date[0] = i[-2]


def film_word(n):
    if n == 1:
        return 'movie'
    return 'movies'


def count_films():
    total = films
    print(f'We watched already {total} {film_word(total)} in 2023')
    
    goal = 200
    pom = goal - total
    if pom > 0:
        print(f'\n\nTo prevail our goal we need to watch {pom} {film_word(pom)} before the end of this year!'.upper())
    else:
        print(f'\n\nThe goal to watch {goal} {film_word(goal)} in this year is accomplished!'.upper())


def show_word(n):
    if n == 1:
        return 'TV show'
    return 'TV shows'        
        
    
def count_ser():
    print(f'We watched already {shows} {show_word(shows)} in 2023')


lf = ''
ls = ''


def last_film():
    global lf, last_date
    lf = '"' + ' '.join(filmlist[-1]) + '"' if filmlist != [] else 'None'
    ldf = last_date[0] if filmlist != [] else '[xx.xx.xxxx]'
    print(f'Last watched movie - ' + lf)
    print('Watched on: ' + ldf)


def last_show():
    global ls
    ls = '"' + ' '.join(showlist[-1]) + '"' if showlist != [] else 'None'
    lds = last_date[1] if showlist != [] else '[xx.xx.xxxx]'
    print(f'Last watched TV series (or season) - ' + ls)
    print('Ended to watch on: ' + lds)


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

    n = sum([1 if x[-1] == 'season)' else int(x[-2][1]) for x in [i.split() for i in res]])
    print(f'\nTotal count of seasons: {n}')

    
def svod_table(n, v=0):
    global films, shows, filmlist, showlist, last_date
    dates = [[], []]
    flags = []
    with open('films2023.txt', encoding='utf-8') as f:
        for i in f:
            if i != '':
                i = i.split()
                k = i[:-1]
                if re.search('season', ' '.join(k)):
                    dates[1].append(datetime.strptime(i[-1][1:-1], '%d.%m.%Y'))
                else:
                    dates[0].append(datetime.strptime(i[-2][1:-1], '%d.%m.%Y'))
                    flags.append(i[-1])
                    
    films_for_use = [' '.join(i) for i in filmlist]
    shows_for_use = [' '.join(i) for i in showlist]
    films_set = {(films_for_use[x].upper(), dates[0][x], flags[x][1]) if dates[0][x]==last_date[0][1:-1] 
                  else (films_for_use[x], dates[0][x], flags[x][1]) for x in range(len(filmlist))}
    show_set = {(shows_for_use[x].upper(), dates[1][x]) if dates[1][x]==last_date[1][1:-1] 
                  else (shows_for_use[x], dates[1][x]) for x in range(len(showlist))}
    
    # Для фильмов
    if n == 1:
        films_dict = {x[0]: (x[1], x[2]) for x in sorted(films_set, key=lambda x: x[1])}
    elif n == 2: 
        films_dict = {x[0]: (x[1], x[2]) for x in sorted(films_set, key=lambda x: x[0])}
    films_dict = {x: (datetime.strftime(films_dict[x][0], '%d.%m.%Y'), films_dict[x][1]) for x in films_dict}
    lfilm = films_for_use[-1]
    tabf = pd.DataFrame.from_dict(films_dict, orient='index', columns=['Watch date', 'R/F*']).reset_index()
    tabf.rename(columns={'index': 'Movie', 0: 'Watch date', 1: 'R/F*'}, inplace=True)
    tabf.rename(index = lambda x: x+1, inplace=True)
    tabf = tabf if v == 0 else tabf.tail(v)
    f = tabf.style.set_properties(**{'background-color': '#222430', 
                                     'color': '#95abab',
                                     'border-style': 'solid',
                                     'border-width': '1px',
                                     'border-color': '#733737',
                                     'max-width': '450px',
                                     'font-size': '10pt',
                                     'text-align': 'center'})
    def check_last(df, com, ind, last, columns):
        """Передается датафрейм, комманда стиля, индекс в списке даты (фильм/сериал), 
        последний фильм/сериал"""
        def highlight(st, column, style):
            is_hl = pd.Series(data=False, index=st.index)
            is_hl[column] = st.loc[column].values == [last, last_date[ind][1:-1]]
            return [style if is_hl.any() else '' for v in is_hl]
        
        df.apply(highlight, column=columns, style=com, axis=1)
        
    for k in ['font-weight: bold', 'font-style: italic', 'background-color: #6e2626']:
        check_last(f, k, 0, lfilm, columns=['Movie', 'Watch date'])
    f = f.to_html()
    display(HTML(f))
    
    # Для сериалов
    if show_set != set():
        if n == 1:
            show_dict = {x[0]: x[1] for x in sorted(show_set, key=lambda x: x[1])}
        elif n == 2:
            show_dict = {x[0]: x[1] for x in sorted(show_set, key=lambda x: x[0])}
        show_dict = {x: datetime.strftime(show_dict[x], '%d.%m.%Y') for x in show_dict}
        lshow = shows_for_use[-1]
        tabs = pd.DataFrame.from_dict(show_dict, orient='index', columns=['Watch date']).reset_index()
        tabs.rename(columns={'index': 'TV series', 0: 'Watch date'}, inplace=True)
        tabs.rename(index = lambda x: x+1, inplace=True)
        tabs = tabs if v == 0 else tabs.tail(v)
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
            check_last(s, j, 1, lshow, columns=['TV series', 'Watch date'])
        s = s.to_html()
        display(HTML(s))
