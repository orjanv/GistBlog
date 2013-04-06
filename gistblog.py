#!/usr/bin/env python
 
import json, urllib2, os, getpass
from urlparse import urljoin
from base64 import encodestring

GITHUB_API = 'https://api.github.com'
os.chdir('/home/orjanv/gistblog')
KEY = '.mytoken.key'
APP_NAME = 'Gist blog CLI app'

def WriteTokenToFile(token):
	try:
		with open(KEY, 'w+'):
			# Write token to file
			f = open(KEY, 'w+')
			f.write(token + "\n")
			print "Wrote token:",token, "to file:", KEY
			f.close()
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
		#return None

	#print data
	for auth in data:
		if auth['note'] == APP_NAME and 'gist' in auth['scopes']:
			#print "Retrieving existing token:", auth['token']
			#WriteTokenToFile(auth['token'])
			return auth['token']

def ReadGist(token):
	url = urljoin(GITHUB_API, 'users/orjanv/gists')
	req = urllib2.Request(url)
	req.add_header('Authorization', 'token ' + token)
	data = json.load(urllib2.urlopen(req))

	#print data
	for d in data:
		print d[u'description']
		print "." * 10

def PostGist():

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

def main():
	token = ''
	token = ReadTokenFromFile(token)
	choice = 0
	loop = 1
	while loop == 1:
		print " "
		print "Gist blog menu"
		print " "
		print "1: Add a gist post"
		print "2: Get all gist posts"
		print "3: Quit"
		choice = input("Choose from the menu: ")
		if choice == 1:
			PostGist()
		elif choice == 2:
			ReadGist(token)
		elif choice == 3:
			loop = 0

if __name__ == '__main__':
    main()
