from database.DB_connect import DBConnect # 1
from model.states import State
from model.connessione import Connessione


class DAO:
    @staticmethod
    def getAllShapes(anno):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct s.shape as forma
                from sighting s 
                where year(s.`datetime`) = %s
                """
        cursor.execute(query, (anno,))
        for row in cursor:
            result.append(row["forma"])
        cursor.close()
        conn.close()
        return result

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
                select distinct n.state1  as stato1, n.state2  as stato2 
                from neighbor n
                where n.state1 < n.state2
                """
        cursor.execute(query)
        for row in cursor:
            result.append(Connessione(idMap[row['stato1']], idMap[row['stato2']]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPesi(stato1, stato2, shape, year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT COUNT(*) AS peso
                FROM sighting s
                WHERE (s.state = %s OR s.state = %s) 
                AND s.shape = %s 
                AND YEAR(s.datetime) = %s
                """
        cursor.execute(query, (stato1, stato2, shape, year))
        for row in cursor:
            result.append(row['peso'])
        cursor.close()
        conn.close()
        return result
