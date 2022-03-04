#!/bin/python

import threading
import time
import datetime
import socket
import random
import struct
import egdmodel

class EGDSimulator():

		def __init__(self, egd, address="127.0.0.255", fixed = False):
			self.egd = egd
			self.sock = None
			self.socklock = threading.Lock()
			self.count = 0
			self.address = address
			self.fixed = fixed

		def computeValue(self, tag):
			if tag.type in ["REAL","LREAL"]:
				tag.lastvalue = tag.lastvalue if tag.lastvalue != None else (-1000.0 + random.random() * 2000.0)
				tag.lastvalue += 0 if self.fixed else -10 + random.random() * 20
			elif tag.type == "DINT":
				tag.lastvalue = tag.lastvalue if tag.lastvalue != None else random.randrange(-1000,1000)
				tag.lastvalue += 0 if self.fixed else random.randrange(-10,11) 
			elif tag.type == "INT":
				tag.lastvalue = tag.lastvalue if tag.lastvalue != None else random.randrange(-100,100)
				tag.lastvalue += 0 if self.fixed else random.randrange(-1,2)
			elif tag.type == "UDINT":
				tag.lastvalue = tag.lastvalue if tag.lastvalue != None else random.randrange(0,2000)
				tag.lastvalue += 0 if self.fixed else random.randrange(0,21)
			elif tag.type == "UINT":
				tag.lastvalue = tag.lastvalue if tag.lastvalue != None else random.randrange(0,200)
				tag.lastvalue += 0 if self.fixed else random.randrange(0,3)
			elif tag.type == "BOOL":
				tag.lastvalue = tag.lastvalue if tag.lastvalue != None else random.randrange(0,2)
				tag.lastvalue = tag.lastvalue if (self.fixed or random.randrange(0,10000) < 9998) else not tag.lastvalue
			
			return tag.lastvalue

		def computeValues(self, exchange):
			values = []
			lasttag = None
			for tag in exchange.tags:
				v = self.computeValue(tag)
				v = v if tag.type != "BOOL" else v << int(tag.offsetbit)
				if lasttag != None and lasttag.offsetbyte == tag.offsetbyte:
					values[len(values)-1] = values[len(values)-1] | v
				else:
					values.append(v)
					lasttag = tag
					
			return values

		def produce(self, producer, exchange):
			if self.isRunning():
				self.count += 1
				#record last time stamp for dumping purposes by using lasttimestamp field of egd exchange
				tm = time.localtime()
				exchange.lasttimestamp = "" + str(self.count) + " at " + str(tm.tm_hour).zfill(2) + ":" + str(tm.tm_min).zfill(2) + ":" + str(tm.tm_sec).zfill(2)
				hdr = egdmodel.EGDHeader.newHeaderFor(producer.producerid, exchange.exchangenumber, self.count).header
				payload = struct.pack(exchange.codec, *self.computeValues(exchange))
				self.sock.sendto(hdr+payload, (self.address, egdmodel.UDP_DATA_PORT))
				threading.Timer(float(exchange.period) / 1000.0, self.produce, [producer, exchange]).start()

		def isRunning(self):
			with self.socklock:
				return self.sock != None

		def stop(self):
			with self.socklock:
				if self.sock != None: 
					self.sock.close()
					self.sock = None

		def start(self, producerid = None):
			with self.socklock:
				self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				if self.address.endswith(".255"):
					self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

			for producerid in self.egd.producers:
				producer = self.egd.producers[producerid]
				for exchangenumber in producer.exchanges:
					exchange = producer.exchanges[exchangenumber]
					if self.fixed: self.computeValues(exchange)
					threading.Timer(float(exchange.period) / 1000.0, self.produce, [producer, exchange]).start()

