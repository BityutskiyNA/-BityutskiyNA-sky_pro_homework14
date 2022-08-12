from flask import Blueprint, jsonify
from main.dao.films import BD_films


bp_main = Blueprint('bp_main',__name__)
film_DAO = BD_films('netflix.db')

@bp_main.route('/')
def bp_main_1():
    txt = """
          Страница с запросами к базе данных netflix.db. Реализовано несколько запросов 
          1. /movie/<title>/ запрос по имени фильма Возвращает данные  в формате json  
          Пример запроса:  http://127.0.0.1:5000/movie/13TH/
          2. /movie/year/to/year/<date1>,<date2>/ запрос по датам выпуска фильмов.
          Получает выборку между датой 1 и датой2. Возвращает данные  в формате json  
          Пример запроса: http://127.0.0.1:5000/movie/year/to/year/2019,2020/
          3. /rating/<rating>/ запрос по группе рейтинга фильма. Группы есть children,family,adult. 
          Если указана не известная группа то вернет строчку 'нет такой группы' Возвращает данные  в формате json
          Пример запроса по группе children: http://127.0.0.1:5000//rating/children/
          Пример запроса по группе family: http://127.0.0.1:5000//rating/family/
          Пример запроса по группе adult: http://127.0.0.1:5000//rating/adult/
          4. /genre/<genre> запрос по жанру фильма Возвращает данные  в формате json  
          Пример запроса:  http://127.0.0.1:5000/genre/Documentaries/
    """
    return txt

@bp_main.route('/movie/<title>/')
def bp_film_by_name(title:str):
    films = film_DAO.get_film_name(title)
    return jsonify([film for film in films])

@bp_main.route('/movie/year/to/year/<date1>,<date2>/')
def bp_film_by_date(date1,date2):
    films = film_DAO.get_film_by_date(date1,date2)
    return jsonify([film for film in films])

@bp_main.route('/rating/<rating>/')
def bp_film_by_rating(rating:str):
    if rating == 'children':
        ratings = "('G')"
    elif rating == 'family':
        ratings = ('G', 'PG', 'PG-13')
    elif rating == 'adult':
        ratings = ('R', 'NC-17')
    else:
        return "нет такой группы"
    films = film_DAO.get_film_by_rating(ratings)
    return jsonify([film for film in films])

@bp_main.route('/genre/<genre>')
def bp_film_by_genre(genre:str):
    films = film_DAO.get_film_by_listed(genre)
    return jsonify([film for film in films])
