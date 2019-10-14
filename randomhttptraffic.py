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
   
    # Download and save a file specified by url to destination directory.
    
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

    # List to hold URLs
    url_list = []

    # List of some arbitrarily chosen User-Agent strings
    agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246', 
            'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36', 
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9', 
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36', 
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1', 
            'Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:1.9b5) Gecko/2008032620 Firefox/3.0b5',
            'Mozilla/5.0 (Nintendo WiiU) AppleWebKit/536.30 (KHTML, like Gecko) NX/3.0.4.2.12 NintendoBrowser/4.3.1.11264.US', 
            'Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU', 
            'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.1058', 
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1', 
            'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36', 
            'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'
                ]

    # Time to run random browser, 0 for infinite
    time_span = 0

    # Seed random num gen based on system time
    random.seed()

    start_time = time.time()

    elapsed = 0

    while (time_span == 0 or elapsed < time_span):
        try:
            with open('majestic_million.csv') as f:
                rows = csv.reader(f)
                for row in rows:
                    url_list.append('http://' + row[2])      # Only put the URL column in the list
       
            r_url = random.choice(list(enumerate(url_list))) # Pick a random URL from the list
            random_url = ''.join(map(str, r_url[1]))         # Get just the URL
            print('Let us go somewhere random on the Internet:', random_url)
            user_agent = random.choice(agent_list)
            print('Random User-Agent string chosen:', user_agent)
            urllib2.urlopen(urllib2.Request(random_url, headers={'User-Agent': user_agent})).read()
        except:
            pass
        elapsed = time.time() - start_time
        wait = random.randint(0,21)
        print('We will wait for ' + str(wait) + ' seconds.')
        time.sleep(wait)

if not os.path.isfile('./majestic_million.csv'):
    download_file('http://downloads.majesticseo.com/majestic_million.csv')
random_traffic()
