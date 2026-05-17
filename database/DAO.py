from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(n, idMapA):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID, t.IATA_CODE, count(*) as N 
                    from (select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*) 
                    from airports a, flights f
                    where a.ID = f.ORIGIN_AIRPORT_ID 
                    or a.ID = f.DESTINATION_AIRPORT_ID 
                    group by a.ID, a.IATA_CODE, f.AIRLINE_ID ) t 
                    group by t.ID, t.IATA_CODE
                    HAVING N >= %s
                    order by N asc"""

        cursor.execute(query, (n,))

        for row in cursor:
            result.append(idMapA[row["ID"]])
        # ho aggiunto al mio risultato una lista di aeroporti, che sono un sottoinsieme degli aeroporti che sono presenti nell'idMap,
        # sono quelli che hanno un n maggiore di quello specificato dall'utente
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMapA):    # prima versione facendo query più facile e complicando il python
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as peso
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID """

        cursor.execute(query)

        for row in cursor:
            # per evitare di fare questo commentato ho creato direttamente il file tratta.py
            # result.append((idMapA[row["ORIGIN_AIRPORT_ID"]],
            #                idMapA[row["DESTINATION_AIRPORT_ID"]],
            #                row["peso"]
            #                ))
            # e posso fare direttamente questo sotto così poi potrò usare la notazione con il punto
            result.append(Tratta(
                idMapA[row["ORIGIN_AIRPORT_ID"]],
                idMapA[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]
                ))

        cursor.close()
        conn.close()
        return result


    def getAllEdgesV2(idMapA):    # seconda versione facendo query più difficile e semplificando il python
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, coalesce(t1.n, 0) + coalesce(t2.n, 0) as peso
                    from (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) t1
                    left join (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f 
                    group by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID ) t2
                    on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID 
                    and t1.DESTINATION_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID
                    where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is null """

        cursor.execute(query)

        for row in cursor:
            result.append(Tratta(
                idMapA[row["ORIGIN_AIRPORT_ID"]],
                idMapA[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]
                ))

        cursor.close()
        conn.close()
        return result