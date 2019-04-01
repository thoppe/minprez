import mistune
import bs4
from emoji import emojize
from build_static import add_css, add_script, include_resource
from custom_mistune import parser

# https://github.com/webslides/WebSlides
# https://raw.githubusercontent.com/thoppe/miniprez/gh-pages/tutorial.md
# https://webslides.tv/demos/
# https://github.com/lepture/mistune

# Must start the line
# _line_class_pattern = re.compile("^\s*\.([\-\w\d]+[\.[\-\w\d]+]?)(.*)")
# _tag_pattern = re.compile(".@([a-z]+)")
# slide_class_pattern = re.compile(r"[^\\]\.\.[\-\w\d]+[\.[\-\w\d]+]?\s")


def slide_parser(html):
    """
    Takes a single slide after being markdown parsed and split by ----
    Returns the slide after parsing the class_patterns.
    """

    # Parse with a error-correcting soup
    soup = bs4.BeautifulSoup(html, "html5lib")

    # Create a new section and the slide-level classes in
    section = soup.new_tag("section")

    # Note the slide-level classes and remove them
    meta = soup.find("meta", attrs={"data-slide-classes": True})
    if meta:
        section["class"] = meta["data-slide-classes"]
        meta.decompose()

    # Replace the emoji with their targets
    for ele in soup.find_all("emoji"):
        symbol = emojize(ele["data-emoji-alias"], use_aliases=True)
        ele.replace_with(symbol)

    # Add the parsed soup to the section and unwrap the body tags
    section.append(soup.body)
    section.body.unwrap()

    return section


def miniprez_markdown(markdown_text):
    html = parser(markdown_text)
    # html = _tag_pattern.sub(r"<\1>", html)

    # Nest each block in a section div
    blocks = []
    strict_hr_tag = "<hr>"
    article = bs4.BeautifulSoup("", "html.parser").new_tag("article")
    article["id"] = "webslides"

    for slide_number, html in enumerate(html.split(strict_hr_tag)):
        section = slide_parser(html)

        # Give each slide a sequential number
        section["data-slide-number"] = slide_number

        article.append(section)

    return str(article)


def build_body(html):
    soup = bs4.BeautifulSoup(html, "html5lib")

    add_css(soup, "static/css/webslides.css")
    add_css(soup, "static/css/miniprez.css")

    add_script(soup, "static/js/jquery-3.1.1.min.js")
    add_script(soup, "static/js/slider.js")

    # If we used font-awesome, add the class and fonts
    if soup.find("span", class_="fa") is not None:
        add_css(soup, "static/css/font-awesome.min.css")
        include_resource("static/fonts/fontawesome-webfont.woff")
        include_resource("static/fonts/fontawesome-webfont.woff2")

    return soup


if __name__ == "__main__":
    text = """...bg-black.foo
introduction
..aligncenter 
### .text-data **miniprez**
--------------------------
slide two
"""

    html = parser(text)
    html = miniprez_markdown(text)

    print("****************************")

    soup = build_body(html)
    # with open('test.html', 'w') as FOUT:
    #    FOUT.write(str(soup))
    print(soup.prettify())
