from bs4 import BeautifulSoup
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Country():
    def __init__(self,id,name,en_name,short_name):
        self.id = id
        self.name = name
        self.en_name = en_name
        self.short_name = short_name
class Main():

    def __init__(self):
        self.country = 'tr'
    def get_country(self):
        list = []
        tags = self.soup.select('tbody tr')
        for tag in tags:

            id = tag.get('id')[8:len(tag.get('id'))]
            name = tag.find(attrs={'data-name':'country[name]'})
            en_name = tag.find(attrs={'data-name':'country[en_name]'})
            short_name = tag.find(attrs={'data-name':'country[short_name]'})
            if(name != None):
                name = name.get_text()
            if(en_name != None):
                en_name = en_name.get_text()
            if(short_name != None):
                short_name = short_name.get_text()
            q = Country(id,name,en_name,short_name)
            list.append(q)
           # print country
        return list
    def build_sql(self,country):
            sql =  'INSERT INTO poi_country (id, NAME, en_name, short_name)VALUES("%s", "%s", "%s", "%s")' \
                   % (country.id,country.name,country.en_name,country.short_name)
            return sql
    def read(self, file_name):
        try:
            fo = open(file_name, 'r')
            str = fo.read()
            fo.close()
            self.soup = BeautifulSoup(str)
            self.file_name = fo.name[fo.name.rfind('\\', 1, len(fo.name)) + 1:fo.name.rfind('.', 0, len(fo.name))]
            print 'read file success ' + fo.name
        except:
            self.soup = 0
            self.file_name = 0
            print 'file no exist [ ' + file_name + ' ]'
    def insert(self,sql):
        if (sql != None):
            try:
                # print sql
                self.cursor.execute(sql)
                self.db.commit()
                # self.result = self.cursor.fetchone()
                print '---------------insert success', self.file_name
            except BaseException, Exception:
                self.db.rollback()
                print 'insert fail', Exception
                # print self.result
                # self.db.close()
    def get_conn(self):
        self.db = MySQLdb.connect(host='101.200.214.9', port=3306, user='roadbooks', passwd='roadbooks', db='roadbooks',
                                  charset='utf8')
        self.cursor = self.db.cursor()
base_dir = 'D:\\Document\\16_PrivateWork\\06_Roadbooks3\\03_poi\\countries\\countries\\'
country = Main()
for i in range(1,4):
    country.read(base_dir+str(i)+'.html')
    list = country.get_country()
    country.get_conn()
    for c in list:
        sql = country.build_sql(c)
        country.insert(sql)