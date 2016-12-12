#-*- coding:utf-8 -*-
#!/usr/bin/python

import pandas as pd
from  DataReadWriter import DataReader, DataWriter
from PortfolioBuilder import PortfolioBuilder
import numpy as np
import time
import datetime
import sys
#Long타입은 아래처럼 datetime으로 변환 가능.
#print datetime.datetime.fromtimestamp(1447977600).strftime('%Y-%m-%d')

start_time = time.time()
try:

	dw = DataWriter()
	dr = DataReader()

	#해당날짜의 평균회귀 성향 확인
	current_date = '2016-01-04'
	next_date = '2016-01-05'
	end_date = '2016-12-07'
	target_column = 'price_close'
	limit = 0
	#get index from dataframe with column, value
	#print dr.loadDirectionsByDate(current_date)['price_date'][dr.loadDirectionsByDate(current_date)['price_date'] == '2015-11-20'].index.tolist()[0]

	portfolio = PortfolioBuilder()

	#show Hit Ratio and save Correct Ratio, count True,False,All
	codes = dr.loadCodes(1,limit)	
	seriesCode = pd.Series(name= 'code')
	seriesCompany = pd.Series(name='company')
	seriesTargetColumn = pd.Series(name= 'target_column')
	seriesCountTrue = pd.Series(name='count_true')
	seriesCountFalse = pd.Series(name='count_false')
	seriesCountAll = pd.Series(name='count_all')

	index = 0
	for a in range(len(codes)):
		#show Hit Ratio
		df_direction = dr.loadDirectionsByCode(codes.iloc[a]['code'] )
		if (df_direction.empty ==False) :
			c_code, c_company, c_target_column,c_count_true,c_count_false,c_count_all =portfolio.showHitRatio(df_direction,target_column)
			#맞는 날짜값이 없으면 c_code=0으로 돌려줌	
			#print "c_code = %s" %c_code
			if( len(c_code) >= 6):
				seriesCode = seriesCode.set_value(index,c_code)
				seriesCompany= seriesCompany.set_value(index,c_company)
				seriesTargetColumn = seriesTargetColumn.set_value(index,c_target_column)
				seriesCountTrue = seriesCountTrue.set_value(index,c_count_true)
				seriesCountFalse = seriesCountFalse.set_value(index,c_count_false)
				seriesCountAll = seriesCountAll.set_value(index,c_count_all)
				#print "len(c_code)>=6 activate c_code =%s"%c_code
				index+=1
	df_count = pd.concat([seriesCode, seriesCompany,seriesTargetColumn, seriesCountTrue, seriesCountFalse, seriesCountAll],axis=1)
	print df_count
	df_count.to_pickle("stockPredictionData/predictionData.data")
	dw.updatePredictionToDB(df_count)
	current_date = next_date

finally:
	end_time = time.time()- start_time
	print "---------------- 수행 시간(초)----------------"
	print end_time

	#print time.strftime("%s시간: %s분 :%s초 소요",round(end_time,0)/3600 , round(end_time,0)/60, round(end_time,0))
