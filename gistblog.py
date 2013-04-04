#!/usr/bin/env python
 
import json, urllib2, requests, os

choice = 0
app_name = 'Gist blog CLI app'
key = ".mytoken.key"
os.chdir('/home/orjanv/gistblog')

def WriteTokenToFile(token):
	# Write token to file
	f = open(key, 'w')
	f.write(token)
	print "\nWrote token to file:", token
	f.close()

def ReadTokenFromFile(token):
	f = open(key, 'r')
	for line in f:
		token = line.strip()
	f.close()

def login():
	# Login to Github
	user = raw_input("Github username: ")
	password = raw_input("Github password: ")
	token = GetToken(user, password)
	WriteTokenToFile(token)
	return token

def GetToken(user, password):
	# login to gist.github.com to get a token and write to config file

	# Check there isn't already an auth code for your app:
    r = requests.get('https://api.github.com/authorizations', auth=(user, password))
    for auth in r.json():
        if auth['note'] == app_name \
            and 'gist' in auth['scopes']:
            print "Retrieving existing token"
            #print json.dumps(auth, indent=4)
            #print auth['token']
            return auth['token']
            
    print "Creating new token"
    # Otherwise create a new token
    r = requests.post('https://api.github.com/authorizations',
        data=json.dumps({
            'scopes':['gist'],
            'note':app_name
            }),
        headers={'content-type':'application/json'},
        auth=(user, password)
    )
    return r.json()['token']

def ReadGist():
	req = urllib2.Request("https://api.github.com/users/orjanv/gists")
	req.add_header('Authorization', 'token ' + token)
	data = json.load(urllib2.urlopen(req))

	#print data
	for d in data:
		print d[u'created_at']
		print d[u'description']
		print '\n'

def PostGist():

	with open('post.md', 'r') as f:
		input3 = f.read()
		
	print "\nBlogfile read\n"
	#print "".join(input3)
		
	input1 = raw_input("Gist Title: ")
	input2 = raw_input("Gist Ingress: ")
	#input3 = raw_input("Gist Content: ")

	gist = {"description": input2, "public": "true", "files": {input1: {"content": input3}}}
	json_data = json.dumps(gist)

	req = urllib2.Request("https://api.github.com/gists")
	req.add_header('Authorization', 'token ' + token)
	result = urllib2.urlopen(req, json_data)

	print "\nGist posted"
	f.close()

def GistBlogMenu():
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
			ReadGist()
		elif choice == 3:
			loop = 0

# Grab token or login to get token
token = login()

# Call Gist Blog Menu
GistBlogMenu()
