#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Dowloads the majestic top one million database and extracts and opens a random URL for a set time interval.  
'''


from __future__ import ( division, absolute_import, print_function, unicode_literals )

import sys, os, tempfile, logging, argparse, random, time, csv, string

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse

def download_file(url, dest=None):
   
    #Download and save a file specified by url to destination directory.
    
    u = urllib2.urlopen(url)

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    filename = os.path.basename(path)
    if not filename:
        filename = 'downloaded.file'
    if dest:
        filename = os.path.join(dest, filename)

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()

    return filename

def random_traffic():
     #list to hold URLs
     url_list = []

     #time to run random browser, 0 for infinite
     time_span = 0

     #seed random num gen based on system time
     random.seed()

     start_time = time.time()

     elapsed = 0

     while (time_span == 0 or elapsed < time_span):
         try:
             with open('majestic_million.csv') as f:
                 rows = csv.reader(f)
                 for row in rows:
                     url_list.append('http://' + row[2])  # Only put the URL column in the list
       
             r_url = random.choice(list(enumerate(url_list))) #Pick a random URL from the list
             random_url = ''.join(map(str, r_url[1])) # Get just the URL
             print ('Let us go somwhere random on the Internet: ' + random_url)
             urllib2.urlopen(random_url).read()
         except:
             pass
         elapsed = time.time() - start_time
         wait = random.randint(0,21)
         print ('We will wait for ' + str(wait) + ' seconds.')
         time.sleep(wait)


download_file('http://downloads.majesticseo.com/majestic_million.csv')
random_traffic()