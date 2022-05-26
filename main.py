import sqlalchemy
from pprint import pprint
import psycopg2


if __name__ == '__main__':
    db = 'postgresql://maks:ghbdtnbr@localhost:5432/test'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()

    # Запрос 1
    request_1 = '''
                SELECT name, COUNT(artist_id)
                FROM genre JOIN artistgenre ON genre.id=artistgenre.genre_id
                GROUP BY name;
        '''
    print('Количество исполнителей в каждом жанре:')
    sel = connection.execute(request_1)
    pprint(sel.fetchall())
    print()

    # Запрос 2
    request_2 = '''
                    SELECT COUNT(trek.id)
                    FROM album JOIN trek ON album.id=trek.album_id
                    WHERE album.release BETWEEN '01-01-2019' AND '01-01-2020'; 
            '''
    print('Количество треков, вошедших в альбомы 2019-2020 годов:')
    sel = connection.execute(request_2)
    pprint(sel.fetchall()[0][0])
    print()

    # Запрос 3
    request_3 = '''
                        SELECT album.name, round(AVG(trek.duration),1)
                        FROM album JOIN trek ON album.id=trek.album_id
                        GROUP BY album.name; 
                '''
    print('Средняя продолжительность треков по каждому альбому:')
    sel = connection.execute(request_3)
    pprint(sel.fetchall())
    print()

    # Запрос 4
    request_4 = '''
                SELECT name FROM artist
                WHERE id NOT IN(
                SELECT artistalbum.artist_id FROM artistalbum JOIN album ON artistalbum.album_id=album.id
                WHERE album.release='01-01-2020')                          
                ; 
                    '''
    print('Все исполнители, которые не выпустили альбомы в 2020 году:')
    sel = connection.execute(request_4)
    pprint(sel.fetchall())
    print()

    # Запрос 5
    request_5 = '''
                                SELECT collection.name
                                FROM collection JOIN collectiontrek ON collection.id=collectiontrek.collection_id
                                JOIN trek ON collectiontrek.trek_id=trek.id
                                JOIN album ON trek.album_id=album.id
                                JOIN artistalbum ON album.id=artistalbum.album_id
                                WHERE artistalbum.artist_id=2                          
                                ; 
                        '''
    print('Названия сборников, в которых присутствует конкретный исполнитель (id=2, группа "БИ-2"):')
    sel = connection.execute(request_5)
    pprint(sel.fetchall())
    print()

    # Запрос 6
    request_6 = '''
                                    SELECT album.name
                                    FROM album JOIN artistalbum ON album.id=artistalbum.album_id
                                    JOIN artist ON artistalbum.artist_id=artist.id
                                    JOIN artistgenre ON artist.id=artistgenre.artist_id
                                    GROUP BY album.name                          
                                    HAVING COUNT(artistgenre.genre_id)>1
                                    ; 
                            '''
    print('Название альбомов, в которых присутствуют исполнители более 1 жанра;:')
    sel = connection.execute(request_6)
    pprint(sel.fetchall())
    print()

    # Запрос 7
    request_7 = '''
                                        SELECT trek.name
                                        FROM trek LEFT JOIN collectiontrek ON trek.id=collectiontrek.trek_id
                                        WHERE collectiontrek.trek_id is NULL
                                        ; 
                                '''
    print('Наименование треков, которые не входят в сборники:')
    sel = connection.execute(request_7)
    pprint(sel.fetchall())
    print()

    # Запрос 8
    request_8 = '''
                                            SELECT artist.name
                                            FROM artist JOIN artistalbum ON artist.id=artistalbum.artist_id
                                            JOIN album ON artistalbum.album_id=album.id
                                            JOIN trek ON album.id=trek.album_id
                                            WHERE trek.duration=(SELECT MIN(duration) FROM trek) 
                                            ; 
                                    '''
    print('Исполнители, написавшие самый короткий по продолжительности трек:')
    sel = connection.execute(request_8)
    pprint(sel.fetchall())
    print()

    # Запрос 9
    request_9 = '''     SELECT album.name, COUNT(trek.id) trek_count
                        INTO albums
                        FROM album JOIN trek ON album.id=trek.album_id
                        GROUP BY album.name;
                        SELECT name, trek_count FROM albums
                        WHERE albums.trek_count=(SELECT MIN(albums.trek_count) FROM albums)
                        ; 
                '''
    print('Название альбомов, содержащих наименьшее количество треков.:')
    sel = connection.execute(request_9)
    pprint(sel.fetchall())
    print()