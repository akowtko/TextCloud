#! /usr/local/bin/python

import cgi
import cgitb; cgitb.enable()
import textcloud

def htmlFormat( body = 'No text supplied', title = 'CS 5 project page' ):
    """ takes the title and body of your webpage (as a string)
    and adds the html formatting, returning the resulting
    string. If you want to use some features, you may have to
    change this function (or not use it at all...)
                                    """
    startString = """\
Content-Type: text/html;

<html>
<head>
<title>
"""
    afterTitle = """\
</title>
</head>

<body>
"""
    afterBody = """\
</body>
</html>
"""
    return startString + title + afterTitle + body + afterBody




form = cgi.FieldStorage()
if form.has_key( 'inputurl' ) and len(form['inputurl'].value.strip()) > 0:
    url = form['inputurl'].value
    depth = form['depth'].value
    try:
        depth = int(depth) # make it an int!
    except:
        depth = 0 # if it's not an int, make it 0
    url.strip()
    textcloudbody = textcloud.mtcURL( url, depth )
else:
    text = 'I don\'t know what\'s going on.'
    textcloudbody = text

    

originalURL = "<h3><a href=\"./index.html\">Back to text-cloud creation</a></h3>\n"
htmlout = htmlFormat(textcloudbody)
print htmlout  # this renders the page
