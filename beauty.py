from bs4 import BeautifulSoup
import MySQLdb
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')


class Schema():
    def __init__(self, url, name, img_name):
        self.url = url
        self.name = name
        self.img_name = img_name


class Parse():
    def __init__(self):
        self.base_keywords = ['country_name', 'place_display_name', 'google_place_id', 'level_one_activity',
                              'company_name', 'local_name'
            , 'cn_name', 'display_name', 'search_keyword', 'search_places_info', 'coordinate', 'is_noteworthy'
            , 'introduce_desc', 'remark', 'is_noteworthy']
        poi_tag = 'poi-tags-content'
        self.booking_info = ['is_need_booking', 'website', 'booking_desc', 'rebate_desc', 'expedia_search_url',
                             'booking_search_url', 'rating'
            , 'expedia_api_url', 'haoqiao_api_url']
        place_field = ['gather_place', 'telephone', 'way_to_poi']
        upload_img = 'upload_place_image_list'
        self.poi_type = ''
        self.activity = ['level_one_activity', 'company_name', 'gather_place', 'telephone', 'way_to_poi']
        self.car_rental = ['rental_address', 'telephone', 'way_to_poi', 'pick_up_desc', 'self_pick_up_desc',
                           'rental_reminder_desc']
        self.car_back = ['return_address', 'telephone', 'return_desc', 'self_return_desc', 'return_reminder_desc',
                         'gas_station_address', 'gas_station_coordinate']
        self.meal = ['address', 'telephone', 'way_to_poi', 'availability_desc', 'price_desc', 'recommend_dish',
                     'reminder_desc']
        self.sem = ['price_number', 'package_name', 'is_prepaid', 'is_booked']
        self.attraction = ['address', 'telephone', 'way_to_poi', 'opening_time', 'price_desc', 'guide_desc',
                           'reminder_desc']
        self.tip = ['tipable_type','tipable_id','tip_desc','reminder_desc','tip_type']
        self.roadtrip = ['departure_place','terminal_place','distance','suggested_times','use_tips']
        self.flight = ['flight_number','departure_airport','arrival_airport','airline','cross_day_num','availability_desc','departure_terminal','arrival_terminal'
                       ,'take_off_time','landing_time','flight_duration','luggage_quota','dining_desc','reminder_desc']
        self.line = ['transport_method','departure_station_name','terminal_station_name','transport_company','vehicle_type','availability_desc','price_desc','duration','ride_desc','reminder_desc']
        self.hubs = ['hub_type','address','way_to_poi','reminder_desc']
        self.hotel = ['address','telephone','way_to_poi','check_in_time_desc','parking_desc','network_desc','reminder_desc','check_out_time_desc','check_out_reminder_desc']
        self.airport = ['website','icao_code','way_to_poi','way_to_city']
        self.images = []
        self.schemas = []

        for base in self.base_keywords:
            setattr(self, base, '')

    def get_conn(self):
        # self.db = MySQLdb.connect(host='127.0.0.1', port=3306, user='roadbooks', passwd='roadbooks', db='roadbooks',charset='utf8')
        self.db = MySQLdb.connect(host='101.200.214.9', port=3306, user='roadbooks', passwd='roadbooks', db='roadbooks',
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

    def get_book(self):
        self.get_tr_text(self.booking_info)

    def insertSingle(self, sql):
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
                sys.exit(0)
                # print self.result
                # self.db.close()

    def insert(self, sql, value):
        self.cursor.executemany(sql, value)
        self.db.commit()
        print 'insert images success'

    # ------------------------getxxx-------------------------------
    def get_tr_text(self, keys):
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
        self.get_tr_text(self.car_rental)

    def get_car_back(self):
        self.get_tr_text(self.car_back)

    def get_airport(self):
        self.get_tr_text(self.airport)

    def get_hotel(self):
        self.get_tr_text(self.hotel)

    def get_sem(self):
        self.get_tr_text(self.sem)

    def get_meal(self):
        self.get_tr_text(self.meal)

    def get_attraction(self):
        self.get_tr_text(self.attraction)
    def get_tip(self):
        self.get_tr_text(self.tip)
    def get_roadtrip(self):
        self.get_tr_text(self.roadtrip)
    def get_flight(self):
        self.get_tr_text(self.flight)
    def get_line(self):
        self.get_tr_text(self.line)
    def get_hubs(self):
        self.get_tr_text(self.hubs)
    def get_type(self):
        self.type = self.soup.select('h1 span ')[0].get('id')
        htmltype = self.type[self.type.index('_', 8) + 1:self.type.rindex('_')]
        print 'source ' + htmltype
        if (htmltype == 'activity'):
            self.type = 'Activity'
        if (htmltype == 'hotel'):
            self.type = 'HotelMessage'
        if (htmltype == 'meal'):
            self.type = 'MealType'
        if (htmltype == 'attraction'):
            self.type = 'TouristAttractions'
        if (htmltype == 'tip'):
            self.type = 'DisposablePrompt'
        if (htmltype == 'roadtrip'):
            self.type = 'RoadTrips'
        if (htmltype == 'airport'):
            self.type = 'AirportType'
        if (htmltype == 'flight'):
            self.type = 'Aircraft'
        if (htmltype == 'line'):
            self.type = 'CityTraffic'
        if (htmltype == 'car_rental'):
            self.type = 'CarStore'
        if (htmltype == 'airbnb'):
            self.type = 'Airbnb'
        if (htmltype == 'hub'):
            self.type = 'TransportationHub'
        if (htmltype.find('_') > -1):
            print 'target ' + self.type

    def get_images(self):
        imageList = self.soup.select('.upload_place_image_list img')
        for img in imageList:
            self.images.append(img.get('src'))

    def get_schemas(self):
        scmList = self.soup.select('.control-item img')
        for img in scmList:
            url = img.get('src').strip()
            name = img.next_sibling.next_sibling.get_text().strip()
            img_name = url[url.rindex('/') + 1:len(url)]
            self.schemas.append(Schema(url, name, img_name))

    # ----------------------buildxxxsql----------------
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
                            % (self.file_name, "0", self.country_name, self.place_display_name, self.google_place_id,
                               self.coordinate,
                               self.cn_name, self.display_name, self.local_name, self.search_places_info,
                               self.search_keyword, self.type, '0'
                               , self.introduce_desc, self.remark, '0', '0', dt, dt, 'crash')
        else:
            self.base_sql = 0
        print self.base_sql

    def build_activity_sql(self):
        self.activity_sql = 'INSERT INTO roadbooks.poi_activity (first_type, company_name, scene_address, scene_phone, scene_arrive_way, scene_gather_place, base_id)' \
                            'VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
                            % (self.level_one_activity, self.company_name, self.gather_place, self.telephone,
                               self.way_to_poi, self.gather_place, self.file_name)
        print self.activity_sql

    def build_book_sql(self):
        self.book_sql = 'INSERT INTO roadbooks.poi_book_info ( website, book_way, rebate_desc, base_id, can_book,' \
                        ' expedia_search_url, booking_search_url, expedia_api_url, haoqiao_api_url)VALUES' \
                        '( "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
                        % (self.website, self.booking_desc, self.rebate_desc, self.file_name, self.is_need_booking,
                           self.expedia_search_url
                           , self.booking_search_url, self.expedia_api_url, self.haoqiao_api_url)
        print self.book_sql

    def build_images_sql(self):
        self.images_sql = 'INSERT INTO roadbooks.poi_images (base_id, img_url,img_name, poisition, has_copyright)VALUES(%s, %s, %s, %s, %s)'
        res = []
        for img in self.images:
            tmp = (int(self.file_name), str(img), img[img.rindex('/') + 1:len(img)], 0, 0)
            res.append(tmp)
        self.images_sql_value = res;

    def build_schema_sql(self):
        self.schema_sql = 'INSERT INTO roadbooks.poi_schematics (img_url, img_name, sub_type, describ , base_id)VALUES( %s, %s, %s, %s, %s)'
        res = []
        for sem in self.schemas:
            tmp = (sem.url, sem.img_name, '0', sem.name, int(self.file_name))
            res.append(tmp)
        self.sem_sql_value = res

    def build_car_rental_sql(self):
        self.car_rental_sql = 'INSERT INTO roadbooks.car_rental (rental_address, phone, arrive_type, store_instruction, auto_instruction, item, base_id)VALUES("%s","%s", "%s", "%s", "%s","%s","%s")' \
                              % (self.rental_address, self.telephone, self.way_to_poi, self.pick_up_desc,
                                 self.self_pick_up_desc, self.rental_reminder_desc, self.file_name)

    def build_car_back_sql(self):
        self.car_back_sql = 'INSERT INTO roadbooks.car_back ( return_address, store_instruction, auto_instruction, item, station_address, station_coord, base_id)VALUES( "%s", "%s", "%s", "%s","%s","%s","%s")' \
                            % (self.return_address, self.return_desc, self.self_return_desc, self.return_reminder_desc,
                               self.gas_station_address, self.gas_station_coordinate, self.file_name)

    def build_airport_sql(self):
        self.airport_sql = 'INSERT INTO roadbooks.poi_airport_type   ( icao_code,   offical_website,   way_to_poi,   way_to_city,   base_id  )  VALUES  ( "%s", "%s", "%s", "%s","%s" )' \
                           % (self.icao_code, self.website, self.way_to_poi, self.way_to_city, self.file_name)

    def build_sem_sql(self):
        self.sem_sql = 'INSERT INTO roadbooks.poi_sem (price_number, package_name, is_prepaid, is_booked, base_id)VALUES("%s", "%s", "%s", "%s", "%s")' \
                       % (self.price_number, self.package_name, self.is_prepaid, self.is_booked, self.file_name)

    def build_hotel_sql(self):
        self.hotel_sql = 'INSERT INTO roadbooks.poi_hotel ( address, phone, arrive_type, check_in_time, parking_situation, network_situation, check_in_item, check_out_time, check_out_item, base_id)VALUES' \
                         '( "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' \
                         % (self.address, self.telephone, self.way_to_poi, self.check_in_time_desc, self.parking_desc,
                            self.network_desc, self.reminder_desc, self.check_out_time_desc,
                            self.check_out_reminder_desc, self.file_name)

    def build_tag_sql(self):
        self.tag_sql = ''

    def build_meal_sql(self):
        self.meal_sql = 'INSERT INTO roadbooks.poi_meal_type (sence_address, sence_phone, sence_arrive_way, sence_bussiness_time, sence_per_consume, sence_recom_food, sence_attention, base_id)VALUES("%s","%s","%s","%s","%s","%s","%s","%s")' \
                        % (self.address, self.telephone, self.way_to_poi, self.availability_desc, self.price_desc,
                           self.recommend_dish, self.reminder_desc, self.file_name)

    def build_attraction(self):
        self.attraction_sql = 'INSERT INTO roadbooks.poi_tourist_attractions  ( sence_address,  sence_phone,  sence_arrive_way,  sence_open_time,  sence_price,  sence_activity,  sence_attention,  base_id ) VALUES (  "%s",  "%s",  "%s",  "%s",  "%s",  "%s", "%s","%s" )' \
                              % (self.address, self.telephone, self.way_to_poi, self.opening_time, self.price_desc,
                                 self.guide_desc, self.reminder_desc.replace('"',' '), self.file_name)
        print self.attraction_sql
    def build_tip_sql(self):
        self.tip_sql = 'INSERT INTO roadbooks.poi_disposable_prompt (app_scope, app_region, prompt_type, prompt_desc,reminder_desc,base_id)VALUES("%s","%s","%s","%s","%s","%s")' \
            % (self.tipable_type,self.tipable_id,self.tip_type,self.tip_desc,self.reminder_desc.replace('"',' '),self.file_name)
    def build_roadtrips(self):
            self.roadtrip_sql = 'INSERT INTO roadbooks.poi_road_trips ( start_city, end_city, sence_full_distance, sence_proposal_time, sence_tips, base_id)VALUES( "%s","%s","%s","%s","%s","%s")' \
            % (self.departure_place,self.terminal_place,self.distance,self.suggested_times,self.use_tips,self.file_name)
    def build_flight_sql(self):
        self.flight_sql = 'INSERT INTO roadbooks.poi_aircraft (flight_number, start_airport, end_airport, airline, cross_day, operate_time, sence_start_terminal, sence_arrive_terminal, sence_take_off_time, sence_land_time, sence_flight_time, sence_pack_limit, sence_food_situation, sence_attention, base_id)VALUES("%s" ,"%s" ,"%s" ,"%s" ,"%s" ,"%s" ,"%s" ,"%s" ,"%s" ,"%s" ,"%s" ,"%s" ,"%s" ,"%s" ,"%s")' \
            % (self.flight_number,self.departure_airport,self.arrival_airport,self.airline,self.cross_day_num,self.availability_desc,self.departure_terminal,self.arrival_terminal,self.take_off_time,self.landing_time,self.flight_duration,self.luggage_quota,self.dining_desc,self.reminder_desc,self.file_name)
    def build_line_sql(self):
        self.line_sql = 'INSERT INTO roadbooks.poi_city_traffic (transportation, start_station, end_station, carrier_company, car_type, operate_time, price, sence_long, sence_take_illustration, reminder_desc,base_id)VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' \
            % (self.transport_method,self.departure_station_name,self.terminal_station_name,self.transport_company,self.vehicle_type,self.availability_desc,self.price_desc,self.duration,self.ride_desc,self.reminder_desc,self.file_name)
    def build_hubs_sql(self):
        self.hubs_sql = 'INSERT INTO roadbooks.poi_transportation_hub (hub_type, base_id, address, arrive_way, attention)VALUES("%s","%s","%s","%s","%s")'\
            % (self.hub_type,self.file_name,self.address,self.way_to_poi,self.reminder_desc)
        print self.hubs_sql
list = ['1', '56', '61']
base_dir = 'D:\\Document\\16_PrivateWork\\06_Roadbooks3\\03_poi\\poi\\poi\\'
for i in range(28, 5000):
    parse = Parse()
    parse.read(base_dir + str(i) + '.html')
    if (parse.file_name != 0):

        parse.get_conn()
        parse.get_type()

        parse.get_schemas()
        parse.get_images()
        parse.get_base_info()

        parse.build_images_sql()
        parse.build_base_sql()
        parse.build_schema_sql()

        parse.insert(parse.schema_sql, parse.sem_sql_value)
        parse.insert(parse.images_sql, parse.images_sql_value)
        parse.insertSingle(parse.base_sql)
        if (parse.type == 'Activity'):
            parse.get_activity()
            parse.build_activity_sql();
            parse.get_book();
            parse.build_book_sql()
            parse.insertSingle(parse.activity_sql)
            parse.insertSingle(parse.book_sql)
        if (parse.type == 'AirportType'):
            parse.get_airport()
            parse.build_airport_sql()
            parse.insertSingle(parse.airport_sql)
            parse.get_schemas()
            parse.build_schema_sql()
            parse.insert(parse.schema_sql, parse.sem_sql_value)
        if (parse.type == 'CarStore'):
            parse.get_car_rental()
            parse.get_car_back()
            parse.get_book()
            parse.build_car_rental_sql()
            parse.build_car_back_sql()
            parse.insertSingle(parse.car_rental_sql)
            parse.insertSingle(parse.car_back_sql)
        if (parse.type == 'HotelMessage'):
            parse.get_book()
            parse.get_hotel()
            parse.get_sem()
            parse.build_book_sql()
            parse.build_hotel_sql()
            parse.build_sem_sql()
            parse.insertSingle(parse.sem_sql)
            parse.insertSingle(parse.book_sql)
            parse.insertSingle(parse.hotel_sql)
        if (parse.type == 'MealType'):
            parse.get_book()
            parse.get_meal()
            parse.get_sem()
            parse.build_book_sql()
            parse.build_meal_sql()
            parse.build_sem_sql()

            parse.insertSingle(parse.book_sql)
            parse.insertSingle(parse.meal_sql)
            parse.insertSingle(parse.sem_sql)
        if (parse.type == 'TouristAttractions'):
            parse.get_book()
            parse.get_attraction()
            parse.get_sem()

            parse.build_book_sql()
            parse.build_sem_sql()
            parse.build_attraction()

            parse.insertSingle(parse.book_sql)
            parse.insertSingle(parse.sem_sql)
            parse.insertSingle(parse.attraction_sql)
        if(parse.type == 'DisposablePrompt'):
            parse.get_book()
            parse.get_sem()
            parse.get_tip()

            parse.build_book_sql()
            parse.build_sem_sql()
            parse.build_tip_sql()

            parse.insertSingle(parse.book_sql)
            parse.insertSingle(parse.sem_sql)
            parse.insertSingle(parse.tip_sql)
        if(parse.type == 'RoadTrips'):
            parse.get_roadtrip()
            parse.build_roadtrips()
            parse.insertSingle(parse.roadtrip_sql)
        if(parse.type == 'Aircraft'):
            parse.get_flight()
            parse.build_flight_sql()
            parse.insertSingle(parse.flight_sql)
        if(parse.type == 'CityTraffic'):
            parse.get_line()
            parse.get_book()
            parse.get_sem()
            parse.build_line_sql()
            parse.build_book_sql()
            parse.build_sem_sql()

            parse.insertSingle(parse.book_sql)
            parse.insertSingle(parse.sem_sql)
            parse.insertSingle(parse.line_sql)

        if(parse.type == 'TransportationHub'):
            parse.get_hubs()
            parse.build_hubs_sql()
            parse.insertSingle(parse.hubs_sql)


