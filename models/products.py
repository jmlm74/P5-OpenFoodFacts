# Created by jmlm at 30/03/2020-20:03 - testP5
from tools.databaseSQL import databaseConnect
from tools import jmlmtools
from setup import *
import json
import requests
import unicodedata
""""
Products table --> 
"""

class productsTable:

    def __init__(self) -> object:
        """
        init --> just init the variables !
        """
        self.tableName = TABLES["T_PRODUCTS"]
        self.temptableName = TABLES["T_TEMPPRODUCTS"]
        # self.url = 'https://fr.openfoodfacts.org/brands.json'
        self.url1 = URL_PRODUCTS1
        self.url2 = URL_PRODUCTS2


    def create_table_products(self):
        """
        Drop the table if exists and create it
        :return:
        """
        with databaseConnect() as cursor:
            sql = "drop table if exists %s " % self.tableName
            cursor.execute(sql)
            sql = "CREATE TABLE %s (idProduct INT UNSIGNED NOT NULL AUTO_INCREMENT, " \
                  "productName VARCHAR(80) NOT NULL," \
                  "url TEXT NULL, " \
                  "nutriscore_score SMALLINT DEFAULT 100," \
                  "nutriscore_grade CHAR(1) DEFAULT 'z', " \
                  "idCategory INT UNSIGNED," \
                  "dateCreation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP," \
                  "CONSTRAINT FK_Category FOREIGN KEY (idCategory) REFERENCES T_Categories(idCategory) ," \
                  "PRIMARY KEY (idProduct)) ENGINE=InnoDB CHARSET latin1" % self.tableName
            cursor.execute(sql)


    def create_temptable_products(self):
        """
        Drop the table if exists and create it
        :return:
        """
        with databaseConnect() as cursor:
            sql = "drop table if exists %s " % self.temptableName
            cursor.execute(sql)
            sql = "CREATE TABLE %s (idProduct INT UNSIGNED NOT NULL AUTO_INCREMENT, " \
                  "productName VARCHAR(80) NOT NULL," \
                  "url TEXT NULL, " \
                  "nutriscore_score SMALLINT DEFAULT 100," \
                  "nutriscore_grade CHAR(1) DEFAULT 'z', " \
                  "brands VARCHAR(100), "\
                  "idCategory INT UNSIGNED," \
                  "CONSTRAINT fk_tempcategory FOREIGN KEY (idCategory) REFERENCES T_Categories(idCategory) ," \
                  "PRIMARY KEY (idProduct)) ENGINE=InnoDB CHARACTER SET latin1" % self.temptableName
            cursor.execute(sql)


    def fill_temptable_products(self):
        dbconn = databaseConnect()
        with dbconn as cursor:
            sql = "select idCategory,categoryName from T_Categories"
            cursor.execute(sql)
            categories = cursor.fetchall()
            for category in categories:
                print("Récupere données : {} - {}".format(category[0],category[1]))
                sql1 = "insert into %s (productName,url,nutriscore_score,nutriscore_grade,brands,idCategory)" \
                       " values" % self.temptableName
                for i in range(2,7,2):
                    url=self.url1 + category[1] + self.url2 + str(i)
                    response = requests.get(url)
                    if (response.status_code) == 200:
                        # text = json.loads(response.content.decode('latin1'))
                        text = response.json()
                        for t in text['products']:
                            if 'product_name' in t and len(t['product_name']) > 0:
                                t['product_name'] = t['product_name'][:79]
                                t['product_name'] = t['product_name'].replace("'"," ")
                                if 'url' not in t:
                                    t['url'] = ''
                                if 'nutriscore_score' not in t:
                                    t['nutriscore_score'] = "100"
                                if 'nutriscore_grade' not in t:
                                    t['nutriscore_grade'] = "Z"
                                if 'brands' not in t:
                                    t['brands'] = "Inconnu"
                                t['brands'] = t['brands'][:49]
                                if len(t['brands']) == 0:
                                    t['brands'] = "Inconnu"
                                t['brands'] = t['brands'].replace("'", " ")
                                sql2 = "('%s','%s',%s,'%s','%s',%s)"% (  t['product_name'],
                                                                    t['url'],
                                                                    t['nutriscore_score'],
                                                                    t['nutriscore_grade'],
                                                                    t['brands'],
                                                                    category[0])
                                sql= sql1 + sql2
                                cursor.execute((sql))
                dbconn.commit()

    def fill_table_products(self):
        """
        insert from T_temp_products (distinct products)
        :param self:
        :return:
        """
        sql = "insert into T_Products (productName,url,nutriscore_score,nutriscore_grade,idCategory) select " \
              "productName,url, nutriscore_score,nutriscore_grade,idCategory from T_TempProducts group by productName;"
        dbconn = databaseConnect()
        with dbconn as cursor:
            cursor.execute(sql)
            dbconn.commit()


    def drop_temptable_products(self):
        with databaseConnect() as cursor:
            sql = "drop table if exists %s " % self.temptableName
            cursor.execute(sql)


    def drop_table_products(self):
        with databaseConnect() as cursor:
            sql = "drop table if exists %s " % self.tableName
            cursor.execute(sql)



