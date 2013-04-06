## GistBlog

My first attempt to learn Python resulted in a Gist Blog.

I had seen someone diong a similar thing, but wanted to learn more programming and how to use IO to files and connecting to APIs.

You will need a GitHub account and register an "app" before using this script. I recommend reading this page
	http://developer.github.com/guides/getting-started/

The program read markdown text from a file, "post.md" and posts the content from that file instead of asking for content. This way you can use markup in your blogspot on gist.

I will look at a better way of handeling different files etc later.

1. Remember to change file location at the beginning of the file, just after the import:

		os.chdir('/home/orjanv/gistblog')

2. You also want to change the App Name:

		APP_NAME = 'Gist blog CLI app'

### Features to come

Planned improvements:

* Download all gists
* Download one gist and edit it
* Use an editor inline to write a draft
* Publish a saved draft
