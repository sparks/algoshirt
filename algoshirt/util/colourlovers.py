#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import requests
import colorsys

__all__ = [ 'randomPallette', 'newPallettes', 'topPallettes', 'pallettes', 'randomPattern', 'newPatterns', 'topPatterns', 'patterns' ]

def hex_to_rgb(hex_str):
    """Returns a tuple representing the given hex string as RGB.
    
    >>> hex_to_rgb('CC0000')
    (204, 0, 0)
    """
    if hex_str.startswith('#'):
        hex_str = hex_str[1:]
    return tuple([int(hex_str[i:i + 2], 16) for i in xrange(0, len(hex_str), 2)])

def extractPallettes(request):
	if request == None or request.status_code != 200:
		return []

	soup = BeautifulSoup(request.text)

	palletteTags = soup.findAll("palette")
	pallettes = []

	for palletteTag in palletteTags:
		pallette = {}

		palletteIDTag = palletteTag.findAll("id")
		if len(palletteIDTag) > 0:
			pallette['id'] = int(palletteIDTag[0].findAll(text=True)[0])

		hexTags = palletteTag.findAll("hex")
		hexes = []
		for hexTag in hexTags:
			hexes.append(hex_to_rgb(hexTag.findAll(text=True)[0]))
		pallette['colors'] = hexes

		colorWidthTag = palletteTag.findAll("colorwidths")
		if len(colorWidthTag) > 0:
			colorWidthText = colorWidthTag[0].findAll(text=True)
			pallette['colorWidths'] = [float(width) for width in colorWidthText[0].split(",")]

		pallettes.append(pallette)

	return pallettes

def randomPallette():
	payload = { 'showPaletteWidths' : "1" }
	r = requests.get("http://www.colourlovers.com/api/palettes/random", params = payload)

	return extractPallettes(r)

def newPallettes(
	lover = None,
	hueOption = None,
	hex = None,
	hex_logic = None,
	keywords = None,
	keywordExact = None,
	orderCol = None,
	sortBy = None,
	numResults = None):
	payload = {
		'showPaletteWidths' : "1",
		'lover' : lover,
		'hueOption' : hueOption,
		'hex' : hex,
		'hex_logic' : hex_logic,
		'keywords' : keywords,
		'keywordExact' : keywordExact,
		'orderCol' : orderCol,
		'sortBy' : sortBy,
		'numResults' : numResults
	}
	r = requests.get('http://www.colourlovers.com/api/palettes/new', params = payload)

	return extractPallettes(r)

def topPallettes(
	lover = None,
	hueOption = None,
	hex = None,
	hex_logic = None,
	keywords = None,
	keywordExact = None,
	orderCol = None,
	sortBy = None,
	numResults = None):
	payload = {
		'showPaletteWidths' : "1",
		'lover' : lover,
		'hueOption' : hueOption,
		'hex' : hex,
		'hex_logic' : hex_logic,
		'keywords' : keywords,
		'keywordExact' : keywordExact,
		'orderCol' : orderCol,
		'sortBy' : sortBy,
		'numResults' : numResults
	}
	r = requests.get('http://www.colourlovers.com/api/palettes/top', params = payload)

	return extractPallettes(r)

def pallettes(
	lover = None,
	hueOption = None,
	hex = None,
	hex_logic = None,
	keywords = None,
	keywordExact = None,
	orderCol = None,
	sortBy = None,
	numResults = None):
	payload = {
		'showPaletteWidths' : "1",
		'lover' : lover,
		'hueOption' : hueOption,
		'hex' : hex,
		'hex_logic' : hex_logic,
		'keywords' : keywords,
		'keywordExact' : keywordExact,
		'orderCol' : orderCol,
		'sortBy' : sortBy,
		'numResults' : numResults
	}
	r = requests.get('http://www.colourlovers.com/api/palettes', params = payload)

	return extractPallettes(r)

def extractPatterns(request):
	if request == None or request.status_code != 200:
		return []

	soup = BeautifulSoup(request.text)

	patternTags = soup.findAll("pattern")
	patterns = []

	for patternTag in patternTags:
		pattern = {}

		patternIDTag = patternTag.findAll("id")
		if len(patternIDTag) > 0:
			pattern['id'] = int(patternIDTag[0].findAll(text=True)[0])

		hexTags = patternTag.findAll("hex")
		hexes = []
		for hexTag in hexTags:
			hexes.append(hex_to_rgb(hexTag.findAll(text=True)[0]))
		pattern['colors'] = hexes

		imageURLTags = patternTag.findAll("imageurl")
		if len(imageURLTags) > 0:
			pattern['imageURL'] = imageURLTags[0].findAll(text=True)[0]

		patterns.append(pattern)

	return patterns

def randomPattern():
	r = requests.get("http://www.colourlovers.com/api/patterns/random")

	return extractPatterns(r)

def newPatterns(
	lover = None,
	hueOption = None,
	hex = None,
	hex_logic = None,
	keywords = None,
	keywordExact = None,
	orderCol = None,
	sortBy = None,
	numResults = None):
	payload = {
		'showPaletteWidths' : "1",
		'lover' : lover,
		'hueOption' : hueOption,
		'hex' : hex,
		'hex_logic' : hex_logic,
		'keywords' : keywords,
		'keywordExact' : keywordExact,
		'orderCol' : orderCol,
		'sortBy' : sortBy,
		'numResults' : numResults
	}
	r = requests.get('http://www.colourlovers.com/api/patterns/new', params = payload)

	return extractPatterns(r)

def topPatterns(
	lover = None,
	hueOption = None,
	hex = None,
	hex_logic = None,
	keywords = None,
	keywordExact = None,
	orderCol = None,
	sortBy = None,
	numResults = None):
	payload = {
		'showPaletteWidths' : "1",
		'lover' : lover,
		'hueOption' : hueOption,
		'hex' : hex,
		'hex_logic' : hex_logic,
		'keywords' : keywords,
		'keywordExact' : keywordExact,
		'orderCol' : orderCol,
		'sortBy' : sortBy,
		'numResults' : numResults
	}
	r = requests.get('http://www.colourlovers.com/api/patterns/top', params = payload)

	return extractPatterns(r)

def patterns(
	lover = None,
	hueOption = None,
	hex = None,
	hex_logic = None,
	keywords = None,
	keywordExact = None,
	orderCol = None,
	sortBy = None,
	numResults = None):
	payload = {
		'showPaletteWidths' : "1",
		'lover' : lover,
		'hueOption' : hueOption,
		'hex' : hex,
		'hex_logic' : hex_logic,
		'keywords' : keywords,
		'keywordExact' : keywordExact,
		'orderCol' : orderCol,
		'sortBy' : sortBy,
		'numResults' : numResults
	}
	r = requests.get('http://www.colourlovers.com/api/patterns', params = payload)

	return extractPatterns(r)
