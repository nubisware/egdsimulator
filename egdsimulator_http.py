import cgi, sys, getopt
try:
	from BaseHTTPServer import BaseHTTPRequestHandler
	import SocketServer
except:
	from http.server import BaseHTTPRequestHandler
	import socketserver as SocketServer

import egdmodel
import MKVIe, Custom
import egdsimulator

class MyHandler(BaseHTTPRequestHandler):

	def buildTag(self, tag):
		return"""<tr class="tag"><td>{}</td><td>{}</td><td>{}</td></tr>""".format(
				tag.offsetbyte+"."+tag.offsetbit, 
				tag.type, 
				tag.lastvalue if tag.lastvalue != None else "")

	def buildExchange(self, exchange):
		print(exchange.dump())
		return"""
			<tr class="exchange">
				<td>Exchange {}</td>
				<td>Period {} (ms)</td>
				<td>Msg {}</td>
				<td>{} tags</td>
				<td class="toggle"><label></label></td>
			</tr>
			{}
		""".format(
					exchange.exchangenumber, exchange.period, 
					exchange.lasttimestamp if exchange.lasttimestamp != None else "", 
					len(exchange.tags),
					"".join(list(map(lambda t: self.buildTag(t), exchange.sortedTags()))))

	def buildProducer(self, producer):
		return"""
			<tr class="producer"><td>Producer {}</td></tr>
			{}
		""".format(
					producer.producerid, 
					"".join(map(lambda e: self.buildExchange(producer.exchanges[e]), producer.exchanges.keys())))

	def buildTable(self, configuration):
		return"""
			<table><tbody>{}</tbody></table>
		""".format(
					"".join(list(
							map(lambda p: self.buildProducer(configuration.producers[p]), configuration.producers.keys()))
						)
			)

	def buildPage(self, simulator, state):
		page = (open("resources/index.html")).read()
		patches = { 
			"error" : state["error"],
			"errorvisible" : "" if state["error"] != None else "invisible",
  		"delimiter" : state["delimiter"],
  		"skiplines" : state["skiplines"],
  		"address" : simulator.address,
  		"fixed" : "checked" if simulator.fixed else "",
			"displaystart" : "inactive" if simulator.isRunning() else "active",
			"displaystop" : "active" if simulator.isRunning() else "inactive",
			"egd" : self.buildTable(simulator.egd) if simulator.egd != None else ""
		}
		page = page.format(**patches)
		state["error"] = None
		return page
	
	def buildDocumentationPage(self):
		page = (open("resources/documentation.html")).read()
		patches = { 
			"license" : open("LICENSE").read().replace("\n", "<br/>"),
			"authors" : open("AUTHORS").read().replace("\n", "<br/>"),
			"manual" : open("README.md").read().replace("\n", "<br/>")
		}
		page = page.format(**patches)
		return page
	
	def returnPage(self, page):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		if sys.version_info < (3,):
			self.wfile.write(page)
		else:
			self.wfile.write(bytes(page, "UTF-8"))

	def returnResource(self, resource, mediatype):
		self.send_response(200)
		self.send_header('Content-type', (mediatype if mediatype != None else ""))
		self.end_headers()
		self.wfile.write(open(resource, "rb").read())

	def redirect(self, location):
		self.send_response(301)
		self.send_header('Location',location)
		self.end_headers()

	def do_GET(self):

		global simulator
		global state

		if self.path == "/":
			self.returnPage(self.buildPage(simulator, state))
			return
		if self.path == "/logo":
			self.returnResource("resources/logonubisware.png", "image/png")
			return
		if self.path == "/favicon.ico":
			self.returnResource("resources/favicon.ico", "image/ico")
			return
		if self.path == "/documentation":
			self.returnPage(self.buildDocumentationPage())
			return
		else:
			self.redirect("/")
			return

	def parseMultipartPy2(self):
		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		if not ctype == "multipart/form-data":
			self.redirect("/")
			return

		query = cgi.parse_multipart(self.rfile, pdict)

		mkvie = query.get("mkvie")[0] if query.get("mkvie")[0].decode("utf-8-sig") != "" else None
		custom = query.get("custom")[0] if query.get("custom")[0].decode("utf-8-sig") != "" else None

		state["delimiter"] = query.get("delimiter")[0]
		state["skiplines"] = int(query.get("skiplines")[0])
		
		return (mkvie, custom)
			
	def parseMultipartPy3(self):
		global state
		ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
						
		if not ctype == "multipart/form-data":
			self.redirect("/")
			return

		pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
			
		query = cgi.parse_multipart(self.rfile, pdict)
		
		mkvie = query.get("mkvie")[0] if query.get("mkvie")[0].decode("utf-8-sig") != "" else None
		custom = query.get("custom")[0] if query.get("custom")[0].decode("utf-8-sig") != "" else None

		state["delimiter"] = (query.get("delimiter")[0]).decode("utf-8")
		state["skiplines"] = int(query.get("skiplines")[0])
		
		return (mkvie, custom)

	def do_POST(self):

		global simulator
		global state

		if self.path == "/start":
			ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
			
			try:
				pdict["boundary"] = bytes(pdict["boundary"], "utf-8") #fix 2 to 3 bug
			except:
				pdict["boundary"] = bytes(pdict["boundary"])
				
			if not ctype == "multipart/form-data":
				self.returnPage(self.buildPage())
				return
			query = cgi.parse_multipart(self.rfile, pdict)

			simulator.fixed = query.get("fixed") != None and query.get("fixed")[0] != ""

			if query.get("address")[0] != None and query.get("address")[0] != "":
				simulator.address = (query.get("address")[0]).decode("utf-8")

			if not simulator.isRunning():
				simulator.start()
			self.redirect("/")

		if self.path == "/stop":
			if simulator.isRunning():
				simulator.stop()
			self.redirect("/")

		if self.path == "/configure":

			mkvie = None
			custom = None
			if sys.version_info < (3,):
				mkvie, custom = self.parseMultipartPy2()
			else:
				mkvie, custom = self.parseMultipartPy3()
			
			wasrunning = simulator.isRunning()
			if wasrunning: simulator.stop()

			if mkvie != None and mkvie != "" and mkvie != b"":
				print("Parsing MKVIE")
				newegd = egdmodel.EGDConfiguration()
				try:
					MKVIe.Parser(newegd).parse(mkvie, state["delimiter"], state["skiplines"])
				except Exception as e:
					state["error"] = "Unable to parse MKVIe CSV: " + str(e) + str(sys.exc_info()[2].tb_lineno)
					self.redirect("/")

				simulator.egd = newegd
				print(simulator.egd.dump())

			elif custom != None and custom != "" and custom != b"":
				print("Parsing Custom")
				newegd = egdmodel.EGDConfiguration()
				try:
					Custom.Parser(newegd).parse(custom, state["delimiter"], state["skiplines"])
				except Exception as e:
					state["error"] = "Unable to parse Custom CSV: " + str(e) + str(sys.exc_info()[2].tb_lineno)
					self.redirect("/")

				simulator.egd = newegd
				print(simulator.egd.dump())

			if wasrunning: 
				simulator.start()

			self.redirect("/")

			return

		else:
			self.redirect("/")
			return

simulator = None
state = {
	"skiplines" : 2,
	"delimiter" : ",",
	"error" : None
}

def dumpUsage():
	print("python " + sys.argv[0] + ' [-p <port>] [-a <initial send address>]')

def boot(argv):
	global simulator
	global state
	HTTP_PORT = 8000
	INIT_ADDRESS = "127.0.0.255"
	#INIT_CSV = None
	try:
		opts, args = getopt.getopt(argv[1:],"hp:a:")
		for opt, arg in opts:
			if opt == "-h":
				dumpUsage()
				sys.exit(0)
			elif opt == "-p":
				HTTP_PORT = int(arg)
			elif opt == "-a":
				INIT_ADDRESS = int(arg)

	except getopt.GetoptError:
		dumpUsage()
		sys.exit(2)

	#Initialize with empty configuration and default values for fixed and address
	simulator = egdsimulator.EGDSimulator(egdmodel.EGDConfiguration(), INIT_ADDRESS, False)

	httpd = SocketServer.TCPServer(("", HTTP_PORT), MyHandler, bind_and_activate=False)

	httpd.allow_reuse_address = True
	httpd.daemon_threads = True
	try:
		httpd.server_bind()
		httpd.server_activate()
		print("\n " + sys.argv[0] + " HTTP server is listening on port " + str(HTTP_PORT) + "...")
		httpd.serve_forever()
	except:
		pass

	simulator.stop()
	httpd.shutdown()
	httpd.server_close()

if __name__ == "__main__":
	boot(sys.argv)
