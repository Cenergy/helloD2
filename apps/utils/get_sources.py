# -*-coding:utf-8 -*-
__author__ = 'Cenergy'
__date__ = '14/9/18 下午5:58'

from django.db import connection
import pandas as pd
def get_source(sourcename):
    query_sql="select * from sources_sourcescore where sourcename like '%{abc}%'".format(abc=sourcename)
    all_data=pd.read_sql(query_sql,connection)
    data_count = all_data.iloc[:, 0].size
    data_dict = all_data.to_dict(orient='index')
    return data_count, data_dict
def get_source_by_id(source_id):
    query_sql = "select * from sources_sourcescore where id={}".format(source_id)
    all_data = pd.read_sql(query_sql, connection)
    data_dict = all_data.to_dict(orient='index')
    return data_dict

