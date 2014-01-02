import cairo, tempfile, random, feedparser, urllib, os
from PIL import Image
from BeautifulSoup import BeautifulSoup

__all__ = [ 'rss_to_image_surface']
	
def rss_to_image_surface(num_images = 1, urls = None):
	imageUrls = []
	urls_feed = []
	urls_list = []
	images = []
	
	if urls == None:
		urls_list = [
			'http://thisisnthappiness.com/rss',
			'http://n-a-s-a.tumblr.com/rss',
			'http://dailydoseofcelebrities.tumblr.com/rss',
			'http://celebrityclose-up.com/rss',
			'http://alwaysmichaeljackson.tumblr.com/rss'
		]
	elif type(urls) == str:
		urls_list.append(urls)
	else:
		urls_list = urls
	
	for u in urls_list:
		urls_feed.append(feedparser.parse(u))

	for feed in urls_feed:
		for entry in feed['entries']:
			if "summary" in entry:
				soup = BeautifulSoup(entry['summary'])
				if(soup.find("img") != None):
					imageUrls.append(soup.find("img")["src"])
	
	if num_images > len(imageUrls):
		num_images = len(imageUrls)

	images = random.sample(imageUrls, num_images)

	tempfilesJPG = []
	tempfilesPNG = []
	
	for i in range(num_images):
		tempfilesJPG.append(tempfile.NamedTemporaryFile())
		tempfilesPNG.append(tempfile.NamedTemporaryFile())
		
	for i in range(len(images)):
		urllib.urlretrieve(images[i], tempfilesJPG[i].name)
	
	for i in range(len(tempfilesJPG)):
		im = Image.open(tempfilesJPG[i])
		im.save(tempfilesPNG[i], "PNG")

	imageSurfaces = []
	for i in range(len(tempfilesPNG)):	
		imageSurfaces.append(cairo.ImageSurface.create_from_png(tempfilesPNG[i].name))
	
	for tmpfile in tempfilesJPG+tempfilesPNG:
		tmpfile.close()
	
	return imageSurfaces
		
		
		

		
