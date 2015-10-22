#encoding=utf-8

#mysql/redis ?
#mysql
import time,MySQLdb

#timestamp, key, ivalue, svalue


class DBChartAgent:
    def __init__(self, host, user, passwd, dbname):
        self.conn=MySQLdb.connect(host=host, user=user, passwd=passwd,db=dbname, charset="utf8")
        self.cursor = self.conn.cursor()
        pass

    def createKey(self, key):
        sql = """CREATE TABLE `<TableNameToDO>` (
                    `time`  int(10) NOT NULL ,
                    `sid`  varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL ,
                    `ivalue`  bigint(20) NOT NULL ,
                    `svalue`  varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL ,
                    PRIMARY KEY (`time`, `sid`)
                    )
                    ENGINE=InnoDB
                    DEFAULT CHARACTER SET=utf8 COLLATE=utf8_bin
                    ROW_FORMAT=COMPACT;"""
        sql = sql.replace("<TableNameToDO>", key);
        self.cursor.excute(sql)
        pass

    def getLatestISK(self, key, sid, limit):
        sql = """
        SELECT `time`,`ivalue`, `svalue` FROM `<TableNameToDo>`WHERE `sid`=<sid>
            ORDER BY `time` DESC LIMIT <limit>;
        """
        sql = sql.replace("<TableNameToDo>", key)
        sql = sql.replace("<sid>", sid)
        sql = sql.replace("<limit>", limit)
        self.cursor.excute(sql)
        return self.cursor.fetchall()

    def writeKey(self, key, sid, svalue):
        sql = """
        INSERT INTO <TableNameToDo>(`time`,`sid`,`svalue`)
          VALUES(<time>, "<sid>", "<svalue>")
        """
        sql = sql.replace("<TableNameToDo>", key)
        sql = sql.replace("<time>", time.time())
        sql = sql.replace("<key>", key)
        sql = sql.replace("<sid>", sid)
        sql = sql.replace("<svalue>", svalue)
        self.cursor.excute(sql)

    def incKey(self, key, sid, inc, param):
        sql = """
        INSERT INTO <TableNameToDo>(`time`,`key`,`sid`,`ivalue`,`svalue`)
            SELECT  <time>,`key`,`sid`,
               `ivalue`+ <inc>, "<param>"
            FROM
               `<TableNameToDo>`
            WHERE
               `sid` = "<sid>"
            ORDER BY
               `time` DESC
            LIMIT 1
        """
        sql = sql.replace("<TableNameToDo>", key)
        sql = sql.replace("<time>", time.time())
        sql = sql.replace("<inc>", inc)
        sql = sql.replace("<sid>", sid)
        sql = sql.replace("<param>", param)
        self.cursor.excute(sql)
        pass

    def decKey(self, key, sid, dec, param):
        sql = """
        INSERT INTO <TableNameToDo>(`time`,`key`,`sid`,`ivalue` ,`svalue`)
            SELECT  <time>,`key`,`sid`,
               `ivalue`- <dec> , "<param>"
            FROM
               `<TableNameToDo>`
            WHERE
               `sid` = "<sid>"
            ORDER BY
               `time` DESC
            LIMIT 1
        """
        sql = sql.replace("<TableNameToDo>", key)
        sql = sql.replace("<time>", time.time())
        sql = sql.replace("<dec>", dec)
        sql = sql.replace("<sid>", sid)
        sql = sql.replace("<param>", param)
        self.cursor.excute(sql)


