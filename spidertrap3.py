#!/usr/bin/env python3

# Spider Trap

### Configuration Section ###
# the lower and upper limits of how many links to put on each page
LINKS_PER_PAGE = (5, 10)
# the lower and upper limits of how long each link can be
LENGTH_OF_LINKS = (3, 20)
# the port to bind the webserver on 
PORT = 8000
# the delay between the receiving a request and serving up a webpage (in milliseconds)
DELAY = 350
# characters to compose random links from
CHAR_SPACE = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-/'
### End Configuration Section ###

import sys
import random
#import BaseHTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class Handler(BaseHTTPRequestHandler):
  webpages = None
  
  def generate_page(self, seed):
    """Generate a webpage containing only random links"""
    
    html = '<html>\n<body>\n'
    
    random.seed(seed)
    # number of links to put on a page
    num_pages = random.randint(*LINKS_PER_PAGE)
    
    # check if a file was provided
    if self.webpages is None:
      # generate some random links
      for i in range(num_pages):
        address = ''.join([random.choice(CHAR_SPACE) for i in range(random.randint(*LENGTH_OF_LINKS))])
        html += '<a href="' + address + '">' + address + '</a><br>\n'
    else:
      # get links from the file contents
      for i in range(num_pages):
        address = random.choice(self.webpages)
        html += '<a href="' + address + '">' + address + '</a><br>\n'
      
    html += '</body>\n</html>'
    
    return html
    
  def do_HEAD(self):
    """Sends header information"""
    
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()

  def do_GET(self):
    """Responds to any webpage request with a page generated by the generate_page function"""
    
    # sleep() takes number of seconds, but accepts floating values
    # DELAY should be in milliseconds
    time.sleep(DELAY/1000.0)
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    # seed the rand function with the current URL path
    self.wfile.write(self.generate_page(self.path).encode())
  

def print_usage():
  print('Usage: ' + sys.argv[0] + ' [FILE]\n')
  print('FILE is file containing a list of webpage names to serve, one per line.  If no file is provided, random links will be generated.')

    
def main():
  if '-h' in sys.argv or '--help' in sys.argv:
    print_usage()
    exit()
    
  # Use a file, if provided on command line
  if len(sys.argv) == 2:
    try:
      # read in the file
      f = open(sys.argv[1])
      Handler.webpages = f.readlines()
      f.close()
      
      # check for empty file
      if Handler.webpages == []:
        print('The file provided was empty.  Using randomly generated links.')
        Handler.webpages = None
    except IOError:
      print('Can\'t read input file.  Using randomly generated links.')
    
  try:
    print('Starting server on port %d...' % PORT)
    server = HTTPServer(('', PORT), Handler)
    print('Server started.  Use <Ctrl-C> to stop.')
    server.serve_forever()
  except KeyboardInterrupt:
    print('Stopping server...')
    server.socket.close()
    print('Server stopped')
  except:
    print('Error starting http server on port %d.' % PORT)
    print('Make sure you are root, if needed, and that port %d is open.' % PORT)
  
  
if __name__ == '__main__':
  main()
