# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
from sgmllib import SGMLParser  
import sys
import chardet
# create a subclass and override the handler methods
class ListName(SGMLParser):  
    def __init__(self):  
        SGMLParser.__init__(self)  
        self.is_h4 = ""  
        self.name = []  
    def start_h4(self, attrs):  
        self.is_h4 = 1  
    def end_h4(self):  
        self.is_h4 = ""  
    def handle_data(self, text):  
        if self.is_h4 == 1:  
            self.name.append(text)  


# instantiate the parser and fed it some HTML
fo = open("1.html",'r')
str = fo.read()
fo.close()
sys_codec = sys.getdefaultencoding()
file_codec = chardet.detect(str)
codec_str = str.decode('utf-8')
listname = ListName() 
listname.feed(codec_str)
for item in listname.name:  
    print item.decode('utf8')
'''

	
print '***Tag==============='

	print tag.get_text().strip()
print '***base_info==============='
for keyword in base_keywords:
	key = soup.select('tr[id="'+keyword+'"] td')[0].get_text().strip()
	value = soup.select('tr[id="'+keyword+'"] td')[1].get_text().strip()
	print key+'->'+value
print '***book_info========'	
for book in booking_info:
	key = soup.select('tr[id="'+book+'"] td')[0].get_text().strip()
	value = soup.select('tr[id="'+book+'"] td')[1].get_text().strip()
	print key+'->'+value
print '***place_field========'
for place in place_field:
	key = soup.select('tr[id="'+place+'"] td')[0].get_text().strip()
	value = soup.select('tr[id="'+place+'"] td')[1].get_text().strip()
	print key+'->'+value
print '*** schema====='
schemas = soup.select('.control-item img')
for schema in schemas:
	print schema.get('src')
print '*** upload_img ========'
imgs = soup.select('.upload_place_image_list img')
for img in imgs:
	print img.get('src')
'''
