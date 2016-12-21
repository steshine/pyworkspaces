from bs4 import BeautifulSoup
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Book():
    def __init__(self,id,name,url):
        self.id = id
        self.name = name
        self.url = url
class Main():

    def __init__(self):
        self.country = 'tr'
    def get_country(self):
        list = []
        tags = self.soup.select('tbody tr td a')
        for tag in tags:
           # tag = tag.select('')
            id = tag.get_text()
            if(len(id) == 5):
                name = tag.get('data-title')
                url = tag.get('href')
                q = Book(id,name,url)
                list.append(q)
           # print country
        return list
    def build_sql(self,book):
            sql =  ' INSERT INTO roadbooks.poi_guide_book  ( title,  url ) VALUES ("%s", "%s")' \
                   % (book.name,book.url)
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
base_dir = 'D:\\Document\\16_PrivateWork\\06_Roadbooks3\\03_poi\\guidbook\\guidbook\\'
book = Main()
for i in range(1,47):
    book.read(base_dir+str(i)+'.html')
    list = book.get_country()
    book.get_conn()
    for c in list:
        print c.id,c.name,c.url
        sql = book.build_sql(c)
        book.insert(sql)