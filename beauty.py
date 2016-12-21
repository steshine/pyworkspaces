from bs4 import BeautifulSoup
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Parse():
    def __init__(self):
        self.base_keywords = ['country_name', 'place_display_name', 'google_place_id', 'level_one_activity',
                              'company_name'
            , 'cn_name', 'display_name', 'search_keyword', 'search_places_info', 'coordinate', 'is_noteworthy'
            , 'introduce_desc', 'remark']
        poi_tag = 'poi-tags-content'
        booking_info = ['is_need_booking', 'website', 'booking_desc', 'rebate_desc']
        place_field = ['gather_place', 'telephone', 'way_to_poi']
        upload_img = 'upload_place_image_list'
        for base in self.base_keywords:
            setattr(self, base, '')

    def get_conn(self):
        self.db = MySQLdb.connect(host='127.0.0.1', port=3306, user='roadbooks', passwd='roadbooks', db='roadbooks',
                                  charset='utf8')
        self.cursor = self.db.cursor()

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

    def get_tag(self):
        list = []
        tags = self.soup.select('.poi-tags-content li')
        for tag in tags:
            list.append(tag.get_text().strip())
        return list

    def insert(self):
        if (self.sql != 0):
            try:
                # print self.sql
                self.cursor.execute(self.sql)
                self.db.commit()
                # self.result = self.cursor.fetchone()
                print '---------------insert success', self.file_name
            except BaseException, Exception:
                self.db.rollback()
                print 'insert fail', Exception
                # print self.result
                # self.db.close()

    def get_base_info(self):
        if (self.soup != 0):
            for base in self.base_keywords:
                keys = self.soup.select('tr[id="' + base + '"] td')
                values = self.soup.select('tr[id="' + base + '"] td')
                if (keys != '' and values != '' and len(keys) > 1 and len(values) > 1):
                    key = keys[0].get_text().strip()
                    value = values[1].get_text().strip()
                    # print key +'->' +value;
                    if (key != ''):
                        setattr(self, base, value.encode('utf-8'))

    def build_base_sql(self):
        if (self.soup != 0 and self.file_name != 0):

            self.sql = ' INSERT INTO roadbooks.poi_base_crash (id, country_name, place_display_name, \
			google_place_id, level_one_activity, company_name, cn_name, display_name, search_keyword, \
			search_places_info, coordinate, is_noteworthy, introduce_desc, remark ) VALUES \
			("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s" )' \
                       % (self.file_name, self.country_name, self.place_display_name, self.google_place_id,
                          self.level_one_activity, self.company_name, self.cn_name, self.display_name,
                          self.search_keyword, self.search_places_info, self.coordinate, self.is_noteworthy,
                          self.introduce_desc, self.remark)
        else:
            self.sql = 0
            # print self.sql

    def build_tag_sql(self):
        self.sql = ''


list = ['1', '56', '61']
base_dir = 'D:\\Document\\16_PrivateWork\\06_Roadbooks3\\03_poi\\poi\\poi\\'
for i in range(1, 50):
    parse = Parse()
    parse.read(base_dir + str(i) + '.html')
    parse.get_conn()
    parse.build_base_sql()
    parse.build_sql()
    parse.insert()


