import urllib2, re, sys, smtplib
from ConfigParser import SafeConfigParser




"""Login to Gmail and send notification email with body (msg)."""
def sendGmailMessage(username,password,msg):
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(username, username, msg)
	server.quit()

def checkOpodo(searchURL,maxPrice,username,password):
    #be sure that you are seartching in GBP currency, or the regular 
    #expression will fail
    searchTerm = 'pound'

    #GET from server
    try:
        response = urllib2.urlopen(searchURL)
    except Exception:
        sys.exit('Problem finding your search page, please check the address in config.txt (searchURL) is correct and your network connection.')

    #the entire page as a string
    htmlPageAsString = response.read()

    #look for prices
    priceIndices = [m.start() for m in re.finditer(searchTerm, htmlPageAsString)]
    #print priceIndices
    minPrice=1e9
    for index in priceIndices: 
        priceSubString = htmlPageAsString[index:index+20].split()[1].split("<")[0].replace(",","")
        price = float(priceSubString)
        if price < minPrice: minPrice = price
        if price < maxPrice:
            message = "Time to check the flight company; the flight is available for "+str(price)+" GBP.\nFollow this link for the search results: "+searchURL+"\nGo, go, go!"
	    print message,type(message)
            sendGmailMessage(username,password,message)
            return 
    print 'Min price for search was '+minPrice+'... better luck next time!'
    return 


if __name__ == "__main__":
    parser = SafeConfigParser()
    parser.read("config.txt")
    
    try:
        gmailUser = parser.get('emailSettings','gmailUsername')
        gmailPassword = parser.get('emailSettings','gmailPassword')
    except Exception:
        sys.exit('Could not find/parse email settings in config.txt')
    
    try:
    	priceMax= parser.getfloat('searchSettings',"flightMaxPriceForEmail")
	searchURL= parser.get('searchSettings',"searchURL",1)
    except Exception:
        sys.exit('Could not find/parse search settings in config.txt')

    checkOpodo(searchURL,priceMax,gmailUser,gmailPassword)
