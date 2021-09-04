from __future__ import unicode_literals

from django.db import models
from config.settings_mongo import DBCONNECT
from bson import ObjectId
import re

# Create your models here.
class App():
    def __init__(self,dataTable,__dataBase):
        self.__dataBase = DBCONNECT if not __dataBase else __dataBase
        self.__dataTable = self.__dataBase.get_collection(dataTable)

    #  搜索
    def search_data(self,filter_json={},offset=0,limit=0,sort='id',order='desc'):
        mfilter = {}
        if filter_json:
            for fkey in filter_json:
                regex = '.*' + filter_json[fkey] + '.*'
                mfilter[fkey] = {'$regex':regex,'$ option':'i'}
        data_list = []
        ova = -1 if order == 'desc' else 1
        for res in self.__dataTable.find(mfilter).sort(sort,ova).skip(offset).limit(limit):
            res['id'] =str(res['id'])
            data_list.append(res)
        return data_list

    # 获取搜索结果个数
    def search_data_count(self,filter_json):
        mfilter = {}
        if filter_json:
            for fkey in filter_json:
                regex = '.*' + filter_json[fkey] + '.*'
                mfilter[fkey] = {'$regex':regex,'$ option':'i'}
        return self.__dataTable.find(mfilter).count()

    # 聚合搜索
    def aggregate_search(self,cmd=[]):
        return self.__dataTable.aggregate(cmd)

    # 判断数据是否存在
    def is_exsited(self,data):
        if len(self.search_data(filter_json={'id':data['id']},limit=1))>0:
            return True
        else:
            return False

    # 使用id检索数据
    def get_data_by_id(self,id):
        return self.search_data({'id':id})[0]

    # 添加数据
    def add_data(self):
        rep = {}
        if self.is_exsited(rep):
            return self.update_data(rep)
        else:
            rep['id'] = ObjectId()
            return self.__dataTable.insert_one(rep),rep
            
    # 删除数据   
    def remove_data(self,id):
        return self.__dataTable.remove({'id':id})

    # 更新数据
    def update_data(self,id,data):
        return self.__dataTable.update({'id':id},{'$set':data})

    # 关闭数据库连接
    def close(self):
        self.__dataTable.client.close