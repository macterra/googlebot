import urllib2, simplejson

class SearchResult:
    def __init__(self, result):
        self.URL = result['url']
        self.title = result['titleNoFormatting']

class SearchResponse:
    def __init__(self, results):
        self.status = results['responseStatus']
        self.results = []
        for result in results['responseData']['results']:
            self.results.append(SearchResult(result))

def doGoogleSearch(terms):
    url = ('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + urllib2.quote(terms))
    request = urllib2.Request(url) #, None, {'Referer': /* Enter the URL of your site here */})
    response = urllib2.urlopen(request)
    results = simplejson.load(response)
    return SearchResponse(results)
