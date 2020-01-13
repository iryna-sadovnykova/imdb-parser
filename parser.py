# coding=utf-8
import urllib2
import csv
import re


ids = []
movies = []


def parse_title(id):
    link = 'https://www.imdb.com/title/%s/' % id
    url = urllib2.urlopen(link)
    page = url.read()
    spage = page.split('\n')
    name = ''
    year = ''
    category = ''
    for i in range (0, len(spage)):
        line = spage[i]
        if '<h1' in line:
            name_match = re.search('class="">(.+?)&nbsp', line)
            year_match = re.search('year/(.+?)/', line)
            if name_match:
                name = name_match.group(1)
            if year_match:
                year = year_match.group(1)
        if 'releaseinfo' in line:
            # print spage[i + 1]
            match = re.search('dates" >(.+?)$', spage[i + 1])
            if match:
                release_info = match.group(1)
                if 'TV' in release_info:
                    category = 'TV'
                    year_match = re.search('\((.+?)–', release_info)
                    if year_match:
                        year = year_match.group(1)
                if 'game' in release_info:
                    category = 'Game'
                else:
                    category = 'Movie'
        if 'ratingValue' in line:
            rating_match = re.search('ratingValue">(.+?)<', line)
            if rating_match:
                rating = rating_match.group(1)
        if 'ratingCount' in line:
            votes_match = re.search('ratingCount">(.+?)<', line)
            if votes_match:
                votes = votes_match.group(1)
    if name == '' or year == '' or category == '' or rating == '' or votes == '':
        print '%s | %s | %s | %s | %s' % (name, year, category, rating, votes)
        print link



def parse_page(i):
    address = 'https://www.imdb.com/search/title/?country_of_origin=ua&sort=num_votes,desc&start=%s' % (i * 50 + 1)
    try:
        url = urllib2.urlopen(address)
    except urllib2.HTTPError:
        print "Page %s does not exist" % i
    page = url.read()
    spage = page.split('\n')
    for line in spage:
        if '/title/' in line:
            match = re.search('href="/title/(.+?)/"', line)
            if match:
                id = match.group(1)
                if id not in ids:
                    ids.append(id)
                    parse_title(id)


def main():
    movies = []
    
    for i in range(0, 2462 / 50 + 1):
        parse_page(i)
        

    # if len(musicians) == 0:
    #     print "Sorry, we couldn't find anything\n"
    #     quit()

    # musicians.sort(key=lambda x: x[1], reverse=True)

    # file_name = 'musicians.csv'
    # with open(file_name, 'w') as output:
    #     writer = csv.writer(output, lineterminator='\n')
    #     for m in range(max_art):
    #         if m > len(musicians) - 1:
    #             break
    #         writer.writerow(musicians[m])

    # print "Done! Check the file musicians.csv\n"

main()