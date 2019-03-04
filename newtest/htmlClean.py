testString = 'aloittaja ostaa punainen kikherne https://fi.wikipedia.org/wiki/KikherneOnkohan nyt jauho oikein pussi . punainen linssi < a target= " _blank " rel= " nofollo " href= " https://fi.wikipedia.org/wiki/Kylv " > https://fi.wikipedia.org/wiki/Kylvövirviläpapu sitten https://fi.wikipedia.org/wiki/Pavut#Pavut_arkik eless . C3.A4Mungo https://fi.wikipedia.org/wiki/MungopapuPieni ruokaopas papu < a target= " _blank " rel= " nofollow " href= " http://www.menaiset.fi/artikkeli/ruok /papujen_lyhyt_oppimaara " > http://www.menaiset.fi/artikkeli/ruoka/papujen_lyhyt_oppimaaraIlmavaivoja voida helpottaa ruoansulatus edistää yrtti , kuten anis , fenkoli , korianteri , minttu ja kumina ( kappakaali katajanmarja ) br / > http://www.etlehti.fi/artikkeli/terveys/mista_apua_ilmavaivoihin < a target= " _blank " rel= " nofollow " href= " http://www.tohtori.fi/?page=50 3584&id=3877639 " > http://www.tohtori.fi/?page=5033584&id=3877639'

## Clean html and urls
import re

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

noHTMLString = cleanhtml(testString)

noURLString = re.sub(r'http\S+', '', noHTMLString)
##
    
print(noURLString)