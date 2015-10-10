import urllib.request, re

def get_synonims(word):
    opener = urllib.request.build_opener()
    
    html = opener.open('http://www.thesaurus.com/browse/' + word).read(100000).decode(encoding='utf-8', errors='replace')
    
    synonyms_a = re.findall(r'<span class="text">([a-z\ ]+)<\/span>', html)
    synonyms_b = re.findall(r'<a href="[^\"]+">\n([a-z\ ]+)<\/a>', html)

    return synonyms_a + synonyms_b
    

get_synonims('understand')

