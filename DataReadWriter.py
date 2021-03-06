#-*- coding: utf-8 -*-
#!/usr/bin/python
import MySQLdb
import sys
#import StockPrice
#import StockCode
from StockData import StockData
import datetime
import pandas as pd
import logging

class DataReader:
	db = 0
	cursor = 0

	#Naming Mangling 으로 외부에서 파악 불가능하게 함.
	__insCount = 0

	def __init__(self):
		DataReader.__insCount +=1
		# 디비 연결
		self.db = MySQLdb.connect("localhost","dev","aA99426383","StockRecommendationML" )
		self.db.set_character_set('utf8')
		# prepare a cursor object 
		self.cursor = self.db.cursor()
		self.cursor.execute('SET NAMES utf8;')
		self.cursor.execute('SET CHARACTER SET utf8;')
		self.cursor.execute('SET character_set_connection=utf8;')
		
	def __del__(self):
		self.db.close()

	def instanceCount(cls):
		print ("DataReader Instance Count : %s" % cls.__insCount)
		return cls.__insCount

	
	#return dataFrame_codes from db
	def loadCodes(self,market_type, limit =0):
		sqlGetCode = "select * from codes"	
		sqlGetCode += " where market_type = %s"%market_type
		if( limit !=0) :
			sqlGetCode += " limit %s;"%limit
		else :
			sqlGetCode += ";"
		self.cursor.execute(sqlGetCode)
		rows = self.cursor.fetchall()
        #self.db.commit()
		seriesCode = pd.Series(name='code')
		seriesCompany = pd.Series(name= 'company')
		
		for a_index in range(0,len(rows)):
			seriesCode = seriesCode.set_value(a_index,rows[a_index][1])
			seriesCompany = seriesCompany.set_value(a_index,rows[a_index][4])
		
		
		#self.db.close()	
		

		return pd.concat([seriesCode,seriesCompany], axis=1)
		
	#return dataFrame_prices from db
	def loadPrices(self, code, limit=0):
		sqlGetCode = "select * from prices"	
		sqlGetCode += " where code = \"%s\""%code
		if( limit !=0) :
			sqlGetCode += " limit %s;"%limit
		else :
			sqlGetCode += ";"	
		self.cursor.execute(sqlGetCode)
		rows = self.cursor.fetchall()
        #self.db.commit()
		
		seriesDate = pd.Series(name='date')
		seriesCode = pd.Series(name= 'code')
		seriesOpen = pd.Series(name='price_open')
		seriesClose = pd.Series(name= 'price_close')
		seriesHigh = pd.Series(name='price_high')
		seriesLow = pd.Series(name= 'price_low')
		seriesAdjClose = pd.Series(name='price_adj_close')
		seriesVolume = pd.Series(name= 'volume')

	
		for a_index in range(0,len(rows)):
			seriesDate = seriesDate.set_value(a_index,rows[a_index][1])
			seriesCode = seriesCode.set_value(a_index,rows[a_index][2])
			seriesOpen = seriesOpen.set_value(a_index,rows[a_index][3])
			seriesClose = seriesClose.set_value(a_index,rows[a_index][4])
			seriesLow = seriesLow.set_value(a_index,rows[a_index][5])
			seriesHigh = seriesHigh.set_value(a_index,rows[a_index][6])
			seriesAdjClose = seriesAdjClose.set_value(a_index,rows[a_index][7])
			seriesVolume = seriesVolume.set_value(a_index,rows[a_index][8])
		
		#print seriesCode.to_frame().iloc[0]['code']
		#self.db.close()
	
		return pd.concat([seriesDate, seriesCode, seriesOpen, seriesClose, seriesLow, seriesHigh, seriesAdjClose, seriesVolume], axis=1)
		
	#return dataFrame_directions from db
	def loadDirectionsByCode(self, code, date= '2016-12-07', limit=0):
		sqlGetCode = "select * from directions"	
		sqlGetCode += " where code = \"%s\" and price_date<='%s 00:00:00' order by price_date desc"%(code,date)
		if( limit !=0) :
			sqlGetCode += " limit %s;"%limit
		else :
			sqlGetCode += ";"
		self.cursor.execute(sqlGetCode)
		rows = self.cursor.fetchall()
        #self.db.commit()
		
		seriesDate = pd.Series(name='price_date')
		seriesCode = pd.Series(name= 'code')
		seriesCompany = pd.Series(name='company')
		seriesTargetColumn = pd.Series(name= 'target_column')
		seriesDirection = pd.Series(name='direction')
		seriesRankScore = pd.Series(name='rank_score')	
		for a_index in range(0,len(rows)):
			seriesDate = seriesDate.set_value(a_index,rows[a_index][1])
			seriesCode = seriesCode.set_value(a_index,rows[a_index][2])
			seriesCompany= seriesCompany.set_value(a_index,rows[a_index][3])
			seriesTargetColumn = seriesTargetColumn.set_value(a_index,rows[a_index][4])
			seriesDirection = seriesDirection.set_value(a_index,rows[a_index][5])
			seriesRankScore = seriesRankScore.set_value(a_index, rows[a_index][6])

		df_result = pd.concat([seriesDate, seriesCode, seriesCompany, seriesTargetColumn, seriesDirection, seriesRankScore],axis=1)			
		#df_result = df_result.sort_values(by= 'rank_score', ascending =False)
		#df_result = df_result.reset_index(drop ='True')
		return df_result
	
	#return dataFrame_directions from db
	def loadDirectionsByDate(self, date, limit=0):
		sqlGetCode = "select * from directions"	
		sqlGetCode += " where price_date = \"%s\""%(date+" 00:00:00")
		if( limit !=0) :
			sqlGetCode += " limit %s;"%limit
		else :
			sqlGetCode += ";"
		self.cursor.execute(sqlGetCode)
		rows = self.cursor.fetchall()
        #self.db.commit()
		
		seriesDate = pd.Series(name='price_date')
		seriesCode = pd.Series(name= 'code')
		seriesCompany = pd.Series(name='company')
		seriesTargetColumn = pd.Series(name= 'target_column')
		seriesDirection = pd.Series(name='direction')
		seriesRankScore = pd.Series(name='rank_score')
		for a_index in range(0,len(rows)):
			seriesDate = seriesDate.set_value(a_index,rows[a_index][1])
			seriesCode = seriesCode.set_value(a_index,rows[a_index][2])
			seriesCompany= seriesCompany.set_value(a_index,rows[a_index][3])
			seriesTargetColumn = seriesTargetColumn.set_value(a_index,rows[a_index][4])
			seriesDirection = seriesDirection.set_value(a_index,rows[a_index][5])
			seriesRankScore = seriesRankScore.set_value(a_index,rows[a_index][6])

		df_result = pd.concat([seriesDate, seriesCode, seriesCompany, seriesTargetColumn, seriesDirection, seriesRankScore],axis=1)			
		#df_result = df_result.sort_values(by= 'rank_score', ascending =False)
		#df_result = df_result.reset_index(drop ='True')
		return df_result
	
	def loadTopCountPrediction(self, limit=0):
		sqlGetCount = "select * from countPrediction"
		sqlGetCount += " order by count_all DESC"
		if( limit != 0):
			sqlGetCount += " limit %s;"%limit
		else :
			sqlGetCount += ";"
		self.cursor.execute(sqlGetCount)
		rows = self.cursor.fetchall()
        #self.db.commit()
		
		
		seriesCode = pd.Series(name= 'code')
		seriesCompany = pd.Series(name='company')
		seriesTargetColumn = pd.Series(name= 'target_column')
		seriesCountTrue = pd.Series(name='count_true')
		seriesCountFalse = pd.Series(name='count_false')
		seriesCountAll = pd.Series(name='count_all')
		seriesMoneyDiff = pd.Series(name='money_diff')
		for a_index in range(0,len(rows)):
			seriesCode = seriesCode.set_value(a_index,rows[a_index][1])
			seriesCompany= seriesCompany.set_value(a_index,rows[a_index][2])
			seriesTargetColumn = seriesTargetColumn.set_value(a_index,rows[a_index][3])
			seriesCountTrue = seriesCountTrue.set_value(a_index,rows[a_index][4])
			seriesCountFalse = seriesCountFalse.set_value(a_index,rows[a_index][5])
			seriesCountAll = seriesCountAll.set_value(a_index,rows[a_index][6])
			seriesMoneyDiff = seriesMoneyDiff.set_value(a_index, rows[a_index][7])	
		
		
		df_result =pd.concat([ seriesCode, seriesCompany, seriesTargetColumn, seriesCountTrue, seriesCountFalse, seriesCountAll, seriesMoneyDiff],axis=1)
		df_result = df_result.sort_values(by='count_all', ascending=0)
		df_result = df_result.reset_index(drop='True')
		return df_result
	
		
class DataWriter:
	db = 0
	cursor = 0

	#Naming Mangling 으로 외부에서 파악 불가능하게 함.
	__insCount = 0
		
	def __init__(self):
		DataWriter.__insCount +=1
		# 디비 연결
		self.db = MySQLdb.connect("localhost","dev","aA99426383","StockRecommendationML" )
		self.db.set_character_set('utf8')
		# prepare a cursor object 
		self.cursor = self.db.cursor()
		self.cursor.execute('SET NAMES utf8;')
		self.cursor.execute('SET CHARACTER SET utf8;')
		self.cursor.execute('SET character_set_connection=utf8;')
		
	def __del__(self):
		self.db.close()

	def instanceCount(cls):
		print ("DataReader Instance Count : %s" % cls.__insCount)
		return cls.__insCount
	
	#if this func didn't work, use module DataWriter
	def updateCodesToDB(self):
		try:
			# INSERT
			# download Stock's Code from Koscom
			print "Starting Downloading Stock Codes from Koscom."
			codes =StockData()
			codes.parseCodeHTML(codes.downloadCode(1),1)
			codes.parseCodeHTML(codes.downloadCode(2),2)

			sqlAddCode = """insert into codes (last_update, code, full_code, market_type, company) values (now(),%s,%s,%s,%s) ON DUPLICATE KEY UPDATE last_update = now(), full_code =%s, market_type =%s , company =%s"""
			for key, value in codes.iterItems():
				if( len(key) == 0 ):
					continue
				dataCode = (key, value.full_code,value.market_type, value.company , value.full_code, value.market_type, value.company)
				self.cursor.execute(sqlAddCode, dataCode)	
			self.db.commit()
			
		finally:
			print "Finish Update Codes To DB"

	#if this func didn't work, use module DataWriter			
	def updatePricesToDB(self,market_type, dateTime1, dateTime2):
		
		# debug
		#logging.basicConfig(level=logging.DEBUG)
		
		# INSERT
		# downlodat Stock's data from Yahoo
		print "Starting Downloading Stock Data from Yahoo. market_type: %s , %s ~ %s" % (market_type, dateTime1.strftime("%Y%m%d") , dateTime2.strftime("%Y%m%d") )
		sqlGetCode = "select * from codes"
		sqlGetCode += " where market_type =%s" % (market_type)
		
		self.cursor.execute(sqlGetCode)
		rows =self.cursor.fetchall()
		#cursor.beginTrans()
		prices = StockData()
		index = 1
		print rows

		for a_row in rows:	
			try:
				code = a_row[1]
				company = a_row[4]
				#data_count = db.getDataCount(code)
				#if data_count == 0:
				print "... %s of %s : Downloading [(%s)%s]'s data to stockData/ " % (index, len(rows),code, company)
					
				file_name = 'stockData/[%s](%s)' %(index, code)
				file_name += a_row[4]
				file_name += ".data"
				#print 'filename : %s , company : %s , code : %s' %(file_name, company, code)
				df_data = prices.downloadPrice(file_name, code, dateTime1, dateTime2)
				if df_data is not None:
					#DB로 전송
					for i in range(0,len(df_data.index)):
						if(df_data.Volume[i] != 0): #주식 거래량이 0이 아닌 것만  DB갱신
							sqlAddPrice = """insert into prices (last_update, price_date, code, price_open, price_close, price_low, price_high, price_adj_close, volume) values (now(), %s, %s, %s, %s, %s, %s, %s , %s) ON DUPLICATE KEY UPDATE last_update = now(), price_open =%s , price_close=%s, price_low = %s, price_high =%s, price_adj_close =%s, volume = %s"""
							dataPrice = (df_data.index[i].strftime('%Y-%m-%d %H:%M:%S'), a_row[1], df_data.Open[i], df_data.Close[i], df_data.Low[i], df_data.High[i], df_data.iloc[i]['Adj Close'], df_data.Volume[i] , df_data.Open[i], df_data.Close[i], df_data.Low[i], df_data.High[i], df_data.iloc[i]['Adj Close'], df_data.Volume[i] )
							self.cursor.execute(sqlAddPrice, dataPrice)
				# end if df_data is not None
				self.db.commit()
				print "... %s of %s : %s 's data Committed to DB" % (index, len(rows), company)

			except:
				print "Fail Update Prices to DB"
			finally:
				index+=1
		print "Finish Update Prices to DB"
		

	def updateDirectionsToDB(self,df_directions):
		try:
			# INSERT
			#DB로 전송
			for i in range(0,df_directions.shape[0]):
				sqlAddDirection = """insert into directions (last_update, price_date, code, company, target_column, direction, rank_score) values (now(), %s, %s, %s, %s , %s,%s) ON DUPLICATE KEY UPDATE last_update = now(), target_column= %s, direction = %s , rank_score=%s"""
				dataDirection = ( (df_directions.iloc[i]['price_date']+' 00:00:00'), df_directions.iloc[i]['code'], df_directions.iloc[i]['company'],df_directions.iloc[i]['target_column'], df_directions.iloc[i]['direction'] ,df_directions['rank_score'][i], df_directions.iloc[i]['target_column'], df_directions.iloc[i]['direction'] ,df_directions['rank_score'][i] )
				print dataDirection
				#if( (df_directions.iloc[i]['direction'] == 'SHORT') or (df_directions.iloc[i]['direction'] =='LONG')):
				self.cursor.execute(sqlAddDirection, dataDirection)
				self.db.commit()

				print "... %s of %s : %s 's direction data Committed to DB" % (i+1, df_directions.shape[0], df_directions.iloc[i]['company'])
		
			self.db.commit()
		finally:
			print "Finish Update Directions To DB"
		


	def updatePredictionToDB(self,df_prediction):
		try:
			# INSERT
			#DB로 전송
			for i in range(0,df_prediction.shape[0]):
				sqlAddPrediction = """insert into countPrediction (last_update,  code, company, target_column, count_true, count_false, count_all, money_diff) values (now(), %s, %s, %s , %s,%s,%s,%s) ON DUPLICATE KEY UPDATE last_update = now(), target_column= %s, count_true = %s, count_false = %s , count_all = %s , money_diff =%s"""
				dataPrediction = ( df_prediction.iloc[i]['code'], df_prediction.iloc[i]['company'],df_prediction.iloc[i]['target_column'], df_prediction.iloc[i]['count_true'] ,df_prediction.iloc[i]['count_false'], df_prediction.iloc[i]['count_all'] ,df_prediction.iloc[i]['money_diff'],df_prediction.iloc[i]['target_column'], df_prediction.iloc[i]['count_true'] ,df_prediction.iloc[i]['count_false'], df_prediction.iloc[i]['count_all'] , df_prediction.iloc[i]['money_diff'] )
			
				print dataPrediction
				self.cursor.execute(sqlAddPrediction, dataPrediction)
				self.db.commit()
				print "... %s of %s : %s 's count Prediction data Committed to DB" % (i+1, df_prediction.shape[0], df_prediction.iloc[i]['company'])
		
			self.db.commit()
		finally:
			print "Finish Update Prediction To DB"
		


