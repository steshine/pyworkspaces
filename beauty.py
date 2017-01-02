from bs4 import BeautifulSoup
import MySQLdb
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')


class Parse():
    def __init__(self):
        self.base_keywords = ['country_name', 'place_display_name', 'google_place_id', 'level_one_activity',
                              'company_name','local_name'
            , 'cn_name', 'display_name', 'search_keyword', 'search_places_info', 'coordinate', 'is_noteworthy'
            , 'introduce_desc', 'remark','is_noteworthy']
        poi_tag = 'poi-tags-content'
        self.booking_info = ['is_need_booking', 'website', 'booking_desc', 'rebate_desc','expedia_search_url','booking_search_url','rating'
                        ,'expedia_api_url','haoqiao_api_url']
        place_field = ['gather_place', 'telephone', 'way_to_poi']
        upload_img = 'upload_place_image_list'
        self.poi_type = ''
        self.activity = ['level_one_activity','company_name','gather_place','telephone','way_to_poi']
        self.car_rental = ['rental_address','telephone','way_to_poi','pick_up_desc','self_pick_up_desc','rental_reminder_desc']
        self.car_back = ['return_address','telephone','return_desc','self_return_desc','return_reminder_desc','gas_station_address','gas_station_coordinate']
        self.images = []



        for base in self.base_keywords:
            setattr(self, base, '')

    def get_conn(self):
        #self.db = MySQLdb.connect(host='127.0.0.1', port=3306, user='roadbooks', passwd='roadbooks', db='roadbooks',charset='utf8')
        self.db = MySQLdb.connect(host='101.200.214.9', port=3306, user='roadbooks', passwd='roadbooks', db='roadbooks',charset='utf8')
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
    def get_book(self):
        self.get_tr_text(self.booking_info)
    def insert(self,sql):
        if (sql != 0):
            try:
                # print self.sql
                self.cursor.execute(sql)
                self.db.commit()
                # self.result = self.cursor.fetchone()
                print '---------------insert success', self.file_name
            except BaseException, Exception:
                self.db.rollback()
                print 'insert fail', Exception
                # print self.result
                # self.db.close()
    def insert(self,sql,value):
        self.cursor.executemany(sql,value)
        self.db.commit()
        print 'insert images success'
    def get_tr_text(self,keys):
        if (self.soup != 0):
            for base in keys:
                keys = self.soup.select('tr[id="' + base + '"] td')
                values = self.soup.select('tr[id="' + base + '"] td')
                if (keys != '' and values != '' and len(keys) > 1 and len(values) > 1):
                    key = keys[0].get_text().strip()
                    value = values[1].get_text().strip()
                    # print key +'->' +value;
                    if (key != ''):
                        setattr(self, base, value.encode('utf-8'))
                else:
                    setattr(self, base, ''.encode('utf-8'))
    def get_base_info(self):
        self.get_tr_text(self.base_keywords)
    def get_activity(self):
        self.get_tr_text(self.activity)
    def get_car_rental(self):
        self.get_tr_text()
    def get_type(self):
        self.type = self.soup.select('h1 span ')[0].get('id')
        htmltype =  self.type[self.type.index('_',8)+1:self.type.rindex('_')]
        print 'source '+htmltype
        if(htmltype == 'activity'):
            self.type = 'Activity'
        if (htmltype == 'hotel'):
            self.type = 'HotelMessage'
        if(htmltype == 'meal'):
            self.type = 'MealType'
        if(htmltype == 'attraction'):
            self.type = 'TouristAttractions'
        if(htmltype == 'tip'):
            self.type = 'DisposablePrompt'
        if(htmltype == 'roadtrip'):
            self.type = 'RoadTrips'
        if(htmltype == 'airport'):
            self.type = 'AirportType'
        if(htmltype == 'flight'):
            self.type = 'Aircraft'
        if(htmltype == 'line'):
            self.type = 'CityTraffic'
        if(htmltype == 'car_rental'):
            self.type = 'CarStore'
        if(htmltype == 'airbnbs'):
            self.type = 'Airbnb'
        if(htmltype == 'hubs'):
            self.type = 'TransportationHub'
        if(htmltype.find('_') > -1):
            print 'target ' + self.type
    def get_images(self):
        imageList = self.soup.select('.upload_place_image_list img')
        for img in imageList:
            self.images.append(img.get('src'))
    def build_base_sql(self):
        if (self.soup != 0 and self.file_name != 0):
            '''
            self.sql = ' INSERT INTO roadbooks.poi_base_crash (id, country_name, place_display_name, \
			google_place_id, level_one_activity, company_name, cn_name, display_name, search_keyword, \
			search_places_info, coordinate, is_noteworthy, introduce_desc, remark ) VALUES \
			("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s" )' \
                       % (self.file_name, self.country_name, self.place_display_name, self.google_place_id,
                          self.level_one_activity, self.company_name, self.cn_name, self.display_name,
                          self.search_keyword, self.search_places_info, self.coordinate, self.is_noteworthy,
                          self.introduce_desc, self.remark)
        '''
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.base_sql = 'INSERT INTO roadbooks.poi_base (id, nation, nation_name, place, google_place, \
                          coordinate, cn_name, display_name, local_name, search_palce, search_key, TYPE, is_dot, \
                          common_desc, remark, is_show, is_sfsc, ctime, utime, op_user) VALUES ' \
                           ' ("%s", "%s","%s", "%s", "%s","%s", "%s", "%s", "%s", "%s", "%s","%s", "%s", "%s", "%s", "%s","%s","%s","%s","%s")' \
                       %(self.file_name,"0",self.country_name,self.place_display_name,self.google_place_id,self.coordinate,
                         self.cn_name,self.display_name,self.local_name,self.search_places_info,self.search_keyword,self.type,'0'
                         ,self.introduce_desc,self.remark,'0','0',dt,dt,'crash')
        else:
            self.base_sql = 0
        print self.base_sql

    def build_activity_sql(self):
        self.activity_sql = 'INSERT INTO roadbooks.poi_activity (first_type, company_name, scene_address, scene_phone, scene_arrive_way, scene_gather_place, base_id)' \
                            'VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
                            %(self.level_one_activity,self.company_name,self.gather_place,self.telephone,self.way_to_poi,self.gather_place,self.file_name)
        print self.activity_sql
    def build_book_sql(self):
        self.book_sql = 'INSERT INTO roadbooks.poi_book_info ( website, book_way, rebate_desc, base_id, can_book,' \
                        ' expedia_search_url, booking_search_url, expedia_api_url, haoqiao_api_url)VALUES' \
                        '( "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
                        % (self.website,self.booking_desc,self.rebate_desc,self.file_name,self.is_need_booking,self.expedia_search_url
                          ,self.booking_search_url,self.expedia_api_url,self.haoqiao_api_url)
        print self.book_sql
    def build_images_sql(self):
        self.images_sql = 'INSERT INTO roadbooks.poi_images (base_id, img_url,img_name, poisition, has_copyright)VALUES(%s, %s, %s, %s, %s)'
        res = []
        for img in self.images:
            tmp = (int(self.file_name),str(img),img[img.rindex('/')+1:len(img)],0,0)
            res.append(tmp)
        self.images_sql_value = res;
    def build_car_rental_sql(self):
        self.car_rental_sql = 'INSERT INTO roadbooks.car_rental (rental_address, phone, arrive_type, store_instruction, auto_instruction, item, base_id)VALUES("%s","%s", "%s", "%s", "%s","%s","%s", "%s")'\
        % (self.rental_address,self.telephone,self.way_to_poi,self.pick_up_desc,self.self_pick_up_desc,self.rental_reminder_desc,self.file_name)
    def build_car_back_sql(self):
        self.car_back_sql = 'INSERT INTO roadbooks.car_back ( return_address, store_instruction, auto_instruction, item, station_address, station_coord, base_id)VALUES( "%s", "%s", "%s", "%s","%s","%s","%s")' \
                   % (self.return_address, self.return_desc, self.self_return_desc, self.return_reminder_desc,
                      self.gas_station_address, self.gas_station_coordinate,self.file_name)

    def build_tag_sql(self):
        self.tag_sql = ''


list = ['1', '56', '61']
base_dir = 'D:\\Document\\16_PrivateWork\\06_Roadbooks3\\03_poi\\poi\\poi\\'
for i in range(456, 2000):
    parse = Parse()
    parse.read(base_dir + str(i) + '.html')
    if(parse.file_name != 0):

        #parse.get_conn()
        parse.get_type()
        '''
        parse.get_images()
        parse.build_images_sql()
        parse.insert(parse.images_sql,parse.images_sql_value)
        parse.get_base_info()
        parse.build_base_sql()
        parse.get_book();
        parse.build_book_sql()
        parse.get_activity()
        parse.build_activity_sql();
        if(parse.type == 'Activity'):
            parse.insert(parse.base_sql)
            parse.insert(parse.activity_sql)
            parse.insert(parse.book_sql)
        '''



