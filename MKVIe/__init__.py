import csv

class Parser(object):

	def __init__(self, model):
		self.model = model
		pass

	def parse(self, csvdata, delimiter=",", skiplines = 2):
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
			if row != None and len(row) > 11:
				producerid = row[8]
				address = row[3]
				tagtype = row[5]
				period = row[9]
				destination = row[12]

				producer = self.model.getProducer(producerid)
				if producer == None:
					producer = self.model.addProducer(producerid, destination)

				exchangenumber, byteoffset, bitoffset = address.split(".")
				exchange = producer.getExchange(exchangenumber)
				if exchange == None:
					exchange = producer.addExchange(exchangenumber, period)
				
				#print("Adding tag to exchange",exchange.exchangenumber,tagtype,byteoffset, bitoffset)
				t = exchange.addTagFromAddressParts(tagtype, byteoffset, bitoffset)
				#print(t.dump())
		self.model.buildCodecs()
