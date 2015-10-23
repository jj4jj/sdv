#encoding=utf-8

#mysql/redis ?
#mysql
import time,MySQLdb
import config
#timestamp, key, ivalue, svalue

def current_ms():
    return long(time.time()*1000);


class DBChartAgent:
    def __init__(self, host, port, user, passwd, dbname):
        self.conn=MySQLdb.connect(host=host, user=user, port=port, passwd=passwd,db=dbname, charset="utf8")
        self.cursor = self.conn.cursor()
        pass

    def createKey(self, key):
        sql = """CREATE TABLE IF NOT EXISTS `%s` (
                    `time`  bigint(20) NOT NULL ,
                    `sid`  varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL ,
                    `ivalue`  bigint(20) NOT NULL ,
                    `svalue`  varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL ,
                    PRIMARY KEY (`time`, `sid`)
                    )
                    ENGINE=InnoDB
                    DEFAULT CHARACTER SET=utf8 COLLATE=utf8_bin
                    ROW_FORMAT=COMPACT;"""
        #print(sql)
        return self.cursor.execute(sql % key)
        pass

    def getLatestISK(self, key, sid, limit):
        sql = """
        SELECT `time`,`ivalue`, `svalue` FROM `%s`WHERE `sid`="%s"
            ORDER BY `time` DESC LIMIT %d;
        """
        sql = sql % (key, sid, limit)
        #print(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def setKey(self, key, sid, svalue, ivalue=0):
        sql = """
        INSERT INTO `%s`(`time`,`sid`,`svalue`,`ivalue`)
          VALUES(%d, "%s", "%s", %d)
        """
        sql = sql % (key, current_ms(), sid, svalue, ivalue)
        #print(sql)
        n = self.cursor.execute(sql)
        #print(n)
        self._commit()
        return n

    def incKey(self, key, sid, inc = 1, param = ""):
        sql = """
        INSERT INTO `%s`(`time`,`sid`,`ivalue`,`svalue`)
            SELECT  %u,`sid`,
               `ivalue`+ %d, "%s"
            FROM
               `%s`
            WHERE
               `sid` = "%s"
            ORDER BY
               `time` DESC
            LIMIT 1
        """
        sql = sql % (key, current_ms(), inc, param, key, sid)
        #print(sql)
        n = self.cursor.execute(sql)
        #print(n)
        if n==0:
            n=self.setKey(key, sid, param, inc)
        self._commit()
        return n


    def decKey(self, key, sid, dec=1, param = ""):
        sql = """
        INSERT INTO `%s`(`time`,`sid`,`ivalue`,`svalue`)
            SELECT  %d,`sid`,
               `ivalue`- %d, "%s"
            FROM
               `%s`
            WHERE
               `sid` = "%s"
            ORDER BY
               `time` DESC
            LIMIT 1
        """
        sql = sql % (key, current_ms(), dec, param, key, sid)
        n = self.cursor.execute(sql)
        #print(n)
        if n==0:
            n=self.setKey(key, sid, param, -dec)
        self._commit()
        return n

    def _commit(self):
        self.conn.commit()



if __name__ == "__main__":
    dca = DBChartAgent(config.DB_HOST,config.DB_PORT, config.DB_USER,config.DB_PASSWD, config.DB_NAME)
    dca.createKey("online")
    dca.createKey("register")
    dca.setKey("register","2003","hello,world")
    dca.incKey("online","2002", 30)
    dca.incKey("online","2003")
    dca.incKey("online","2004")
    dca.decKey("online","2002")
    all=dca.getLatestISK("online","2002",5)
    print(all)