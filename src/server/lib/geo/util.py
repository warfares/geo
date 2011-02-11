#!/usr/bin/env python
# encoding: utf-8
"""
util.py

Created by Rodolfo  Barriga.
"""
from psycopg2 import connect
import psycopg2.extras

CONN_STR = 'user=postgres password=postgres dbname=pelambre'

class DataHelper:
	def __init__(self):
		self.conn = connect(CONN_STR)
		self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	def fetchall(self,sql):
		self.cursor.execute(sql)
		rows = self.cursor.fetchall()
		return rows
	
	def fetchone(self,sql):
		self.cursor.execute(sql)
		row = self.cursor.fetchone()
		return row

	def close(self):
		self.cursor.close()
		self.conn.close()
		pass
