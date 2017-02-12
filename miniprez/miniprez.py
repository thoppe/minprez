import sys
import bs4
import os
import codecs
from parser import file_iterator, section_iterator, section

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

f_base_html = os.path.join(os.path.dirname(__location__),
                           "static", "minipres_base.html")

if __name__ == "__main__":

    f_md = sys.argv[1]
    F = file_iterator(f_md)

    with open(f_base_html) as FIN:
        raw = FIN.read()
        base = bs4.BeautifulSoup(raw,'lxml')
        slides = base.find("article",{"id":"minislides"})

    for k,x in enumerate(section_iterator(F)):
        soup = section(x).soup
        soup.section["id"] = "slide-number-{}".format(k+1)
        soup.section["class"] = soup.section.get('class',[]) + ["slide",]
        slides.append(soup)

    f_html = '.'.join(os.path.basename(f_md).split('.')[:-1]) + '.html'
    with codecs.open(f_html,'w','utf-8') as FOUT:
        #output = unicode(base.prettify())
        output = unicode(base)

        FOUT.write(output)

    #print slides.prettify().encode('utf-8')

