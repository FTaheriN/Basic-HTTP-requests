#!/usr/bin/python
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi

import threading

PORT_NUMBER = 8080

#This class will handle any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/html1.html"
        # direct user to the page containing form for trying the post method
		elif self.path=="/formpage":
    			self.path="/html2.html"

		try:
			#Check the file extension required and
			#set the right mime type
			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()

				serverName = self.server.server_name
				portNumber = str(self.server.server_port)
				path = self.path
				URLaddress = ''.join([serverName, ':', portNumber, '/', path])

                # creating a new file to keep log info
				textfile = open("logfile.txt" , "a")
                # append the user id and log time in the file
				textfile.write("%s - - [%s] - - [%s] \n" %(self.client_address[0],self.log_date_time_string(),URLaddress)) 
				textfile.close()

				message =  threading.currentThread().getName()
				self.wfile.write(f.read().encode())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

		
    #Handler for the POST requests
	def do_POST(self):
		if self.path=="/send":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			serverName = self.server.server_name
			portNumber = str(self.server.server_port)
			path = self.path
			URLaddress = ''.join([serverName, ':', portNumber, '/', path])

			# creating a new file to keep log info
			textfile = open("logfile.txt" , "a")
            # append the user id and log time in the file
			textfile.write("%s - - [%s] - - [%s] \n" %(self.client_address[0],self.log_date_time_string(), URLaddress)) 
			textfile.close()
			print ("Your name is: %s" % form["fname"].value)
			self.send_response(200)
			self.end_headers()
			self.wfile.write(("Thanks %s !" % form["fname"].value).encode('utf-8'))
			return	

# class defined to be able to handle multiple requests at a time
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


try:
    # using threads to respond to webpage requests
    server = ThreadedHTTPServer(('localhost', 8080), myHandler)
    print ('Starting server on port {}, use <Ctrl-C> to stop' .format(PORT_NUMBER))
    server.serve_forever()


except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()			
