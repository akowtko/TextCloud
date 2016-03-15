#Name: Nicole Kowtko
#Date: December 7, 2011
#Final Project: Textcloud

from hmc_urllib import getHTML
#A list of words to not be included in the text cloud
stoplist = ['the','of','and','a','to','in','is','or','I','i','with','that',\
            'it','he','was','for','on','are','as','his','they','at','be',\
            'this','have','from','or','had','by','but','not','were','when'\
            'an','she','then','her','his','theirs','their','into','has',' ',\
            'my','you','oh','what','some','up','can','now','than','me','no',\
            'yes','one','two','three','four','around','inside','though','each',\
            'may','there','other','more','hold','theres','ive','weve','none',\
            'when','even','an','here']
MAXWORDS = 50
debug = False
visitedpage = []
test = ['cleans','fighter','fitter','brighten','kittens','smitten','fluffs',\
        'fluffs','kittens','quickly','snuggly','walking','jogging','runs',\
        'prettier','jogged','fluffiest','amazement','ability','condition',\
        'celebration','toughness','romance','resemblance','assistance',\
        'violinist','expression','speed']
test2 = ['this','this','this','cat','dog','dog','frog','dog']

def mtcURL(url, d=0):
    """Takes in a url and a depth parameter, and returns out an HTML textcloud
        of length MAXWORDS.
            Input: url, a string that is a url, d, depth parameter
            Output: a string of html"""
    #Gets the contents of the website as a string
    string = getstring(url,d)
    #Separates the individual words into a list, getting rid of punctuation
    wordList = createWordList(string)
    #Removes any words from stoplist
    cleanList = cleaningList(wordList)
    stemmedList = wordStemming(cleanList)
    orderedlist = frequency(stemmedList)
    totalwords = frequencycount(orderedlist)
    printstring = returnstring(orderedlist,totalwords)
    #clearing the string of visited pages for the next time it's run
    visitedpage = []
    return printstring
    
def getstring(URL,DEPTH):
    """Retrieves the text from the given url and crawls to other pages based on
        the depth parameter, storing it all in one string.
            Input: url, a string, depth, the depth parameter
            Output: string, a string of all the text on the given webpages"""
    #Base case
    if DEPTH == 0:
        #The string is simply the text on that page
        string = getHTML(URL)[0]
        #Add that page to a list of visited pages
        visitedpage.append(URL)
        return string
    else:
        #get the string for the current page
        string = getHTML(URL)[0]
        #Add that page to visited pages
        visitedpage.append(URL)
        #Create a list of the other links on the page
        otherlinks = getHTML(URL)[1]
        #Loop through the list of links
        for link in otherlinks:
            #If the link has not been visited yet
            if link not in visitedpage:
                #Add the page to the list of visited pages
                visitedpage.append(link)
                #Recurse on that link and add the text onto the string
                string = string + getstring(link,DEPTH - 1)
        return string
    

def createWordList(string):
    """Takes a string from a URL and separates out the individual words into a
    list.
        Input: string, a string
        Output: wordList, a list of words"""
    wordList = []
    currentWord = ''
    for index in range(len(string)):
        #The character is the string indexed at 'index'
        character = string[index]
        #If the character is a space
        if character.isspace():
            #And the current word isn't empty
            if currentWord != '':
            #append the current word to the word list
                wordList = wordList + [currentWord]
            #reset the list currentWord
            currentWord = ''
        #If the character is alphabetic (this is to avoid adding periods,
        #punctuation, or numbers)
        elif character.isalpha():
            #Add the character to the current word list
            currentWord = currentWord + character
    #Add the last word onto the word list as long as it's not ''
    if currentWord != '':
        wordList.append(currentWord)
    return wordList

def cleaningList(wordList):
    """Takes in the word list and removes unwanted words from stoplist
        Input: wordList, a list of words
        Output: cleanList, a list of words excluding words from stoplist"""
    cleanList = []
    for word in wordList:
        #If the word isn't in the stop list, add it to the new list
        if word not in stoplist:
            cleanList.append(word)
    return cleanList

def wordStemming(cleanList):
    """Stems words so that "jogs", "jogging", etc. are turned into "jog"
            Input: cleanList, a list of words
            Output: stemmedList, a list of stemmed words
    Tests for stemming:
--ing    take off the last three letters (walking -> walk)
--ing    if there was a double letter before the suffix, take off the last four
        letters (jogging -> jog)
--ling   take off the last three letters and add an 'e' (trembling -> tremble)
--cing  take off the last three letters and add an 'e' (placing -> place)
--s      take off the 's'
--sses  take off the last two letters (masses -> mass), a special case for 's'
--us     don't do anything, this is a special case for 's'
--er     take off the last two letters (fighter -> fight)
--er     if there was a double letter before the suffix, take off the last three
        letters (runner -> run)
--ier    (test for -er first, this is a special case) take off the last three
        letters and add a 'y'(fluffier -> fluffy)
--ed     take off the last two letters (walked -> walk)
--ed     if there was a double letter before the suffix, take off the last three
        letters (jogged -> jog)
--ied   take off the last three letters (worried -> worry) and add a y
--led   take off only the last letter, this is a special case for 'ed'
        (ambled -> amble)
--eed    don't do anything, this is a special case for 'ed'
--iest   take off the last four letters and add a 'y'(fluffiest -> fluffy)
--ment   take off the last four letters (contentment -> content)
--ility  take off the last five letters and add 'le' (capability -> capable)
--tion   take off the last three letters and add an 'e' (celebration ->celebrate)
--ition  don't do anything (even though condition ends in 'tion', 'condite' isn't
        a word). Special case for 'tion'
--ness   take off the last four letters (toughness -> tough)
--ance   take off the last four letters (assistance -> assist)
--lance  don't do anything (to avoid resemblance -> resembl) Special case for
        'ance')
--ist    take off the last three letters (violinist -> violin)
--en     take off the last two letters (brighten -> bright)
--en     if there was a double letter before the suffix, take off the last three
        letters and add an 'e' (smitten -> smite)
--ly     take off the last two letters (quickly -> quick)
--ly     if there was a double letter beofre the suffix, take off the last letter
        and add an 'e' (snuggly -> snuggle)
--ion    take off the last three leters (expression -> express)

I'm not doing the following because:
-y      I would run into too much trouble with (sky -> sk)
-or     I can't have doctor -> doct

I'm worried about:
-ance   Currently this will turn 'romance' into 'rom'
-eed    This will avoid 'agreed' from going to 'agree', but it prevents 'seed'
        from being turned into 'se'
-ing    it can't handle shining->shine, but if I change it to add an 'e' at the
        end, it will do walking->walke

"""
    cut1 = ('s')
    cut2 = ('er','en','ly','ed')
    cut3 = ('ist','ing','tion','ion')
    cut4 = ('iest','ment','ness','ance')
    cut5 = ('ility')
    for word in cleanList:
        if debug: print word
        #If the last letter is in cut1 and the last two letters aren't 's' or
        #'u', this is to avoid going into the if statement for 'ness' or turning
        #'adventurous' into 'adventurou'
        if word.endswith(cut1):
            if word[-2] == 's' or word[-2] == 'u':
                #don't do anything
                cleanList = cleanList
            elif len(word)<5:
                cleanList = filter(lambda x: x != word, cleanList)
                cleanList.append(word[:-1])
            #If the word ends in sses, get rid of 'es'
            elif word[-3] == 's' and word[-4] == 's':
                cleanList = filter(lambda x: x!= word, cleanList)
                cleanList.append(word[:-2])
            else:
                #remove all occurances of the word from the list
                cleanList = filter(lambda x: x != word, cleanList)
                #adds the word with the last letter cut off
                #the other instances of the word will be added later in the loop
                cleanList.append(word[:-1])
        elif word.endswith(cut2):
            if debug: print "Entering cut2"
            #to prevent hen -> en, don't apply this if the word is only 3
            #letters long
            if len(word)<4:
                cleanList = cleanList
            elif word.endswith('eed'):
                #don't do anything
                cleanList = cleanList
            else:
                cleanList = filter(lambda x: x != word, cleanList)
                #Checks to see if the word ends in 'ier' (a special case of 'er')
                #or in 'ied' (a special case of 'ed')
                if word.endswith('ier') or word.endswith('ied'):
                    #Chop off the last three letters and add a 'y' at the end
                    cleanList.append(word[:-3] +'y')
                elif word.endswith('led') and word[-4] != 'l':
                    #Chop off only the last letter
                    cleanList.append(word[:-1])
                #If there's a double letter before the suffix
                elif word[-3] == word[-4]:
                    if word.endswith('er') or word.endswith('ed'):
                        #If it ends in 'ssed', cut off only the last 2 letters
                        if word.endswith('ssed'):
                            cleanList.append(word[:-2])
                        else:
                            #chop off the last three letters
                            cleanList.append(word[:-3])
                    elif word.endswith('en'):
                        #chop off the last three letters and add an 'e'
                        cleanList.append(word[:-3]+'e')
                    elif word.endswith('ly'):
                        #chop off the last letter and add an 'e'
                        cleanList.append(word[:-1]+'e')
                else:
                    #Cut off only the last letter if the word's length is 4,
                    #so died -> die
                    if word.endswith('ed') and len(word) == 4:
                        cleanList.append(word[:-1])
                    else:
                        #chop off the last two letters
                        cleanList.append(word[:-2])
        elif word.endswith(cut3):
            if word.endswith('tion'):
                if word.endswith('ition'):
                    #don't do anything
                    cleanList = cleanList
                else:
                    cleanList = filter(lambda x: x != word, cleanList)
                    #cut off the last three letters and add an 'e'
                    cleanList.append(word[:-3]+'e')
            #I don't want to index -5th element if it's only 4 letters long
            elif len(word)==4:
                #don't do anything
                cleanList = cleanList
            elif word.endswith('ling') or word.endswith('cing'):
                #chop off the last three letters and add an 'e'
                cleanList.append(word[:-3]+'e')
            #If there are double letters before the suffix 'ing'
            elif word[-4] == word[-5] and word.endswith('ing'):
                cleanList = filter(lambda x: x != word, cleanList)
                #take off the last four letters
                cleanList.append(word[:-4])
            else:
                cleanList = filter(lambda x: x != word, cleanList)
                cleanList.append(word[:-3])
        elif word.endswith(cut4):
            if word.endswith('iest'):
                cleanList = filter(lambda x: x != word, cleanList)
                #Cut off the last four letters and add a 'y'
                cleanList.append(word[:-4]+'y')
            elif word.endswith('lance'):
                #don't do anything
                cleanList = cleanList
            else:
                cleanList = filter(lambda x: x != word, cleanList)
                cleanList.append(word[:-4])
        elif word.endswith(cut5):
            cleanList = filter(lambda x: x != word, cleanList)
            if word.endswith('ility'):
                #cut off the last five letters and add an 'e'
                cleanList.append(word[:-5]+'le')
    return cleanList


def frequency(stemmedList):
    """This counts the occurances of each word and creates a list of length
    MAXWORDS sorted in descending order with sublists in the form
    [occurances, word]
        Input: stemmedList, a list of stemmed words
        Output: cutlist, a list of words and their frequencies"""
    rawlist = []
    while stemmedList != []:
        #count the occurances of the word
        occurances = len(filter(lambda x: x == stemmedList[0], stemmedList))
        #add it to the list in the form [occurances, word]
        rawlist.append([occurances,stemmedList[0]])
        #delete the word from the original list
        stemmedList = filter(lambda x: x != stemmedList[0], stemmedList)
    #sorts the list in increasing order
    rawlist.sort()
    if len(rawlist) > MAXWORDS:
        #cuts the list so it is only maxwords long
        cutlist = rawlist[-MAXWORDS:]
    else:
        cutlist = rawlist
    #reverses the list so it's in decreasing order
    cutlist.reverse()
    return cutlist

def frequencycount(orderedlist):
    """Finds the total number of words in orderedlist and returns it.
            Input: orderedlist, a list of words
            Output: count, the number of words in the list"""
    count = 0
    for index in range(len(orderedlist)):
        count = count + orderedlist[index][0]
    return count

def returnstring(orderedlist,totalwords):
    """A function that formats all the words into HTML, scaling their size based
        on the number of times they appear.
            Input: orderedlist, a list of words, totalwords, the total # of words
            Output: printstring, a string of HTML"""
    printstring = ""
    #For each subset in orderedlist
    for element in orderedlist:
        #The first element in the subset is the times it appears
        count = element[0]
        #The second element is the word
        word = element[1]
        #The size is going to be it's frequency * 5000
        number = ((count*1.0)/totalwords)*5000
        #Generates the HTML
        rawstring = '<abbr title =' + str(count) + ' style ="font-size:' + \
                    str(number) + '%">' + word + '</abbr> &nbsp; &nbsp;'
        #Adds the string onto the previous string
        printstring = printstring + rawstring
    #returns, not prints, the string    
    return printstring
