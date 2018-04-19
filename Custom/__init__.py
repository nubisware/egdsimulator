import csv

class Parser(object):

	def __init__(self, model):
		self.model = model
		pass

	def parse(self, csvdata, delimiter=",", skiplines = 1):
		self.delimiter = delimiter
		self.skiplines = skiplines
		
		if csvdata == None or csvdata == "":
			return
		
		self.reader = None
		if not (hasattr(csvdata, 'read') and hasattr(csvdata, 'write')):
			self.reader = csv.reader(csvdata.split("\n"), delimiter=delimiter)
		else:
			self.reader = csv.reader(csvdata, delimiter=delimiter)
		
		for i in range(self.skiplines):
			next(self.reader)

		for row in self.reader:
			if row != None and len(row) == 4:
				producerid = row[0]
				exchangenumber = row[1]
				address = row[2]
				tagtype = row[3]
				producer = self.model.getProducer(producerid)
				if producer == None:
					producer = self.model.addProducer(producerid, "")

				byteoffset, bitoffset = address.split(".")
				exchange = producer.getExchange(exchangenumber)
				if exchange == None:
					exchange = producer.addExchange(exchangenumber, 1000)
				
				exchange.addTagFromAddressParts(tagtype, byteoffset, bitoffset)

		self.model.buildCodecs()
