# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from kafka import KafkaProducer
from json import dumps
import time
# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

class Module03Pipeline(object):
    def __init__(self):
        self.producer = KafkaProducer(acks=0, 
                        compression_type='gzip',
                        bootstrap_servers=['127.0.0.1:9092'],
                        value_serializer=lambda x :dumps(x).encode('utf-8')
                        # dumps 파이썬의 dict를 json형태로 바꿔줌
                        # bite를 원래형태로 할때는 역직렬화
                        # 직렬화는 json타입으로 전달해줘야한다.
        )
    def process_item(self, item, spider):
        
        item = dict(item)
        

        # data = {"schema":{"type":"struct","fields":[{"type":"int32","optional":False,"field":"id"},{"type":"string","optional":False,"field":"title"},{"type":"string","optional":False,"field":"weekend"},{"type":"string","optional":False,"field":"gross"},{"type":"string","optional":False,"field":"weeks"},{"type":"int64","optional":True,"name":"org.apache.kafka.connect.data.Timestamp","version":1,"field":"created_at"}],"optional":False,"name":"users"},"payload":{"id":8,"title":"aaaf","weekend":"111","gross":"111","weeks":"9089","created_at":1615796717000}}

        data = {"schema":{"type":"struct","fields":[{"type":"string","field":"title"},{"type":"string","field":"weekend"},{"type":"string","field":"gross"},{"type":"string","field":"weeks"},{"type":"string","field":"genre"},{"type":"string","field":"rating"},{"type":"string","field":"movie_release"},{"type":"string","field":"people"},{"type":"int64","name":"org.apache.kafka.connect.data.Timestamp","version":1,"field":"created_at"}],"name":"users"},"payload":{"title":item['title'],"weekend":item['weekend'],"gross":item['gross'],"weeks":item['weeks'],"genre":item['genre'],"rating":item['rating'],"movie_release":item['movie_release'],"people":item['people'],"created_at":int(time.time()*1000)}}

        self.producer.send('my_topic_users', value = data)
        time.sleep(10)
        self.producer.flush()
        print('Done:')
 
        print('*********************',item,'*********************')



#{"schema":{"type":"struct","fields":[{"type":"int32","field":"id"},{"type":"string","field":"title"},{"type":"string","field":"weekend"},{"type":"string","field":"gross"},{"type":"string","field":"weeks"},{"type":"int64","name":"org.apache.kafka.connect.data.Timestamp","version":1,"field":"created_at"},{"type":"string","field":"genre"},{"type":"string","field":"rating"},{"type":"string","field":"movie_release"},{"type":"string","field":"people"}],"name":"users"},"payload":{"id":4,"title":"aaa","weekend":"aaa","gross":"aaa","weeks":"aaa","created_at":1615860192000,"genre":"abb13543aa","rating":"aaaaaaaaaa","movie_release":"aaa","people":"aabbba"}}
