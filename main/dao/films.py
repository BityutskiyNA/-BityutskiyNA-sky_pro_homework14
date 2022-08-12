import sqlite3


class BD_films:

    def __init__(self, path):
        self.path = path

    def get_query_rez(self, sqlite_query):
        """
        Выполянет запрос по переданому тексту запроса и переберает результат что бы получился список словарей для json
        :param sqlite_query: текст запроса
        """
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute(sqlite_query)
            query_result = []
            for row in cursor.fetchall():
                query_result.append({cursor.description[row.index(line)][0]: line for line in row})
        return query_result


    def get_film_name(self, title):
        """
        Формируем запрос по полю title и отправляем его в общую функцию для получения результата запроса в формате
        списка словарей
        :param title: Название фильма
        """
        sqlite_query = f"""
                            SELECT 
                            netflix.title as 'title', 
                            country as 'country', 
                            release_year as 'release_year', 
                            listed_in as 'genre',
                            description as 'description' 
                            FROM netflix
                            WHERE  netflix.title='{title}'
                            ORDER BY release_year desc LIMIT 1
                        """
        result = self.get_query_rez(sqlite_query)
        return result


    def get_film_by_date(self, start_selection, end_selection):
        """
        Формируем запрос по полю release_year и отправляем его в общую функцию для получения результата
        запроса в формате списка словарей
        :param start_selection: Начальная дата выборки
        :param end_selection: Конечная дата выборки
        """
        sqlite_query = f"""
                            SELECT 
                            title as 'title', 
                            release_year as 'release_year'
                            FROM netflix
                            WHERE release_year BETWEEN {start_selection} AND {end_selection}
                                """
        result = self.get_query_rez(sqlite_query)
        return result


    def get_film_by_rating(self, ratings):
        """
        Формируем запрос по полю rating и отправляем его в общую функцию для получения результата запроса в формате
        списка словарей
        :param ratings: список рейтингов
        """
        sqlite_query = f"""
                            SELECT 
                            title as 'title', 
                            rating as 'rating',
                            description as 'description'
                            FROM netflix
                            WHERE rating IN {ratings}
                                """
        result = self.get_query_rez(sqlite_query)
        return result


    def get_film_by_listed(self, listed_in):
        """
        Формируем запрос по полю listed_in и отправляем его в общую функцию для получения результата запроса в формате
        списка словарей
        :param listed_in: Параметры listed_in жанр фильма
        """
        sqlite_query = f"""
                            SELECT 
                            title as 'title', 
                            rating as 'rating',
                            description as 'description'
                            FROM netflix
                            WHERE listed_in LIKE '%{listed_in}%'
                            ORDER BY release_year desc LIMIT 10
                                """
        result = self.get_query_rez(sqlite_query)
        return result

    def get_film_by_actor(self, first_actor, second_actor):
        """
        Формируем запрос по двум актерам и возвращаем только тех актеров которые играли с указанами актерами более
        двух раз
        :param first_actor: первый актер
        :param second_actor: второй актер
        """
        sqlite_query = f"""
                            SELECT
                            netflix.cast
                            FROM netflix
                            WHERE netflix.cast LIKE '%{first_actor}%' OR netflix.cast LIKE'%{second_actor}%'
                                """
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute(sqlite_query)
            query_result = []
            for row in cursor.fetchall():
                query_result.extend([z for z in row[0].split(', ') if z != first_actor and z != second_actor])

            result = list(set([x for x in query_result if query_result.count(x) > 1]))
            # for x in xc:
            #     if xc.count(x) > 1 and rez.count(x) == 0:
            #         rez.append(x)

        return result

    def get_film_by_type(self, type, release_year, listed_in):
        """
        Формируем запрос по полям type,release_year,listed_in и отправляем его в общую функцию
        для получения результата запроса в формате списка словарей
        :param type: Тип картины
        :param release_year: Год выпуска
        :param listed_in: Жанр фильма
        """
        sqlite_query = f"""
                            SELECT 
                            title as 'title', 
                            description as 'description'
                            FROM netflix
                            WHERE listed_in LIKE '%{listed_in}%' 
                            AND netflix.type='{type}' 
                            AND release_year = '{release_year}'
                                   """
        result = self.get_query_rez(sqlite_query)
        return result




# ajlaafjl = BD_films('../../netflix.db')
#
# rating = "('G')"
# test = ajlaafjl.get_film_by_rating(rating)
# print(test)




