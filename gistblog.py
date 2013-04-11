#!/usr/bin/env python

import json, urllib2, os, getpass
from urlparse import urljoin
from base64 import encodestring

# Setting some global variables
GITHUB_API = 'https://api.github.com'
PATH = '/home/orjanv/gistblog'
KEY = '.mytoken.key'
APP_NAME = 'Gist blog CLI app'
DEBUG = '0'

def WriteTokenToFile(token):
	try:
		with open(KEY, 'w+'):
			# Write token to file
			f = open(KEY, 'w+')
			f.write(token + "\n")
			print "Wrote token:",token, "to file:", KEY
			f.close()
	# Catch file errors
	except IOError:
		print "File error: could not write to file:", KEY

def ReadTokenFromFile(token):
	try:
		with open(KEY):
			# Read token from file
			f = open(KEY, 'r')
			for line in f:
				token = line.strip()
			f.close()
			
			if DEBUG == '0':
				# Test if token in file matches token online
				tokenOnline = ''
				tokenOnline = GetToken(token)
				if tokenOnline == token:
					print "Used token from file"
					return token
				elif token != tokenOnline:
					token = tokenOnline
					print "Local token does not match token from GitHub, using that insted"
					WriteTokenToFile(token)
					return token
			return token
			
	# Catch file errors
	except IOError:
		print "File error: grabbing token from GitHub instead"
		tokenOnline = GetToken(token)
		token = tokenOnline
		WriteTokenToFile(token)
		return token

def GetToken(token):
	# User Input
	username = raw_input('Github username: ')
	password = getpass.getpass('Github password: ')
	url = urljoin(GITHUB_API, 'authorizations')

	req = urllib2.Request(url)
	base64string = encodestring('%s:%s' % (username, password)).replace('\n', '')
	req.add_header('Authorization', 'Basic %s' % base64string)

	try:
		data = json.load(urllib2.urlopen(req))
	except urllib2.URLError, e:
		print "Something broke connecting to Github: %s" % e
		quit()

	#print data
	for auth in data:
		if auth['note'] == APP_NAME and 'gist' in auth['scopes']:
			return auth['token']

def ListGists(token):
	url = urljoin(GITHUB_API, 'users/orjanv/gists')
	req = urllib2.Request(url)
	req.add_header('Authorization', 'token ' + token)
	data = json.load(urllib2.urlopen(req))

	posts = []
	print "ID        TITLE"
	print "*" * 15
	for d in data:
		postID = d[u'id']
		for title in d[u'files']:
			print d[u'id'], "-",title
			posts.append(d[u'id'])

	print "\nOldest post is:",min(posts)
	print "Newest post is:",max(posts)
	print "Number of posts is:",len(posts)
	
def PostGist(token):

	# read content from blogpostfile
	with open('post.md', 'r') as f:
		input3 = f.read()
	f.close()

	input1 = raw_input("Gist Title: ")
	input2 = raw_input("Gist Ingress: ") 

    # Compose Request
	url = urljoin(GITHUB_API, 'gists')	
	gist = {"description": input2, "public": "true", "files": {input1: {"content": input3}}}
	req = urllib2.Request(url)
	req.add_header('Authorization', 'token ' + token)
	result = urllib2.urlopen(req, json.dumps(gist))
	print "\nGist posted"

def DownloadGist(token):
	# Show files and make dict with them, letting you 
	# choose one to download, by choose the dict number
	ListGists(token)
	
	# Choose a file to download
	myID = raw_input("Choose an ID to download: )
		
	
	# Check if file already is downloaded
	
	# Write to local file
	return None

def ClearScreen():
	os.system('cls' if os.name=='nt' else 'clear')

def main():
	ClearScreen()
	try:
		os.chdir(PATH)
	# Catch file errors
	except OSError:
		print "File error: could not open directory, creating it instead"
		os.mkdir(PATH, 0755)
		os.chdir(PATH)
		
	token = ''
	token = ReadTokenFromFile(token)
	choice = 0
	loop = 1
	while loop == 1:
		print " "
		print APP_NAME,"\n"
		print "   A: Add a gist post"
		print "   G: Get all gist posts"
		print "   D: Download a gist"
		print "   Q: Quit\n"
		choice = raw_input("Choose from the menu: ")
		if choice == 'A' or choice == 'a':
			ClearScreen()
			PostGist(token)
		elif choice == 'G' or choice == 'g':
			ClearScreen()
			ListGists(token)
		elif choice == 'D' or choice == 'd':
			ClearScreen()
			DownloadGist(token)
		elif choice == 'Q' or choice == 'q':
			loop = 0

if __name__ == '__main__':
    main()
