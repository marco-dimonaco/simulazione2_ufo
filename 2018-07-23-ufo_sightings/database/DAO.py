from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.states import State


class DAO:
    @staticmethod
    def getAllStates():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct s.*
                from state s    
                """
        cursor.execute(query)
        for row in cursor:
            result.append(State(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnections(idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct n.state1 as s1, n.state2 as s2
                from neighbor n
                where n.state1 < n.state2   
                """
        cursor.execute(query)
        for row in cursor:
            result.append(Connessione(idMap[row['s1']], idMap[row['s2']]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPesi(stato1, stato2, anno, giorni):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select count(t.id1) as peso
                from(
                select s1.id as id1, s2.id as id2
                from sighting s1, sighting s2
                where s1.state = %s and s2.state = %s
                and year(s1.`datetime`) = %s
                and year(s1.`datetime`) = year(s2.`datetime`)
                and datediff(s1.`datetime`, s2.`datetime`) <= %s
                and datediff(s1.`datetime`, s2.`datetime`) > 0
                and s2.state != s1.state) as t
                """
        cursor.execute(query, (stato1, stato2, anno, giorni))
        for row in cursor:
            result.append(row['peso'])
        cursor.close()
        conn.close()
        return result

    """
    select ((count(distinct s1.id)) + count(distinct s2.id)) as peso
from neighbor n, sighting s1, sighting s2
where n.state1 = s1.state
and n.state2 = s2.state 
and year(s1.`datetime`) = 2014
and year(s2.`datetime`) = 2014
and abs(datediff(s1.`datetime`, s2.`datetime`)) <= 4
and s1.state in ('AL', 'FL')
and s2.state in ('FL', 'AL')
and s1.state < s2.state
    """
