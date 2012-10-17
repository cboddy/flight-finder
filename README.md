flight-finder
=============

A short dirty python script to ping a Flight Comparison website and send an email notifying if a maximum price (or below) is available.

The crux of the whole thing is that the flight comparison sites (such as Opodo) pass all your search settings (entirely unsecurely) over the http URL.


Short version:

Go yo www.opodo.co.uk, enter your serach criteria and hit search. Then add the resulting URL to config.txt (searchURL = ) along with the price threshold for which you wish to be sent an email telling you (flightMaxPriceForEmail = ). Then add your Gmail credentials to config.txt and add flight_finder_script.py script to crontab

crontab -e

add for hourly running: 
1  * * * * python /path/to/this/README/flight_finder_script.py	


Aaaaand you're done. This script will now be run at 1 minute past the hour, every hour that your computer is turned on. To remove it, again type
crontab -e 
and remove that line.


Long version:

So, we use the nice flight comparison site (www.opodo.co.uk) to search for say, flights to Kuala Lumpur next year or something. Then once it shows the results we copy the entire URL (the thing that begins www.opodo.co.uk/opodo/flights/search?...) and add it to config.txt (where it says searchURL = "...").

This is used by the script to ping the same website as if we had done so in a browser. The script then reads the resulting HTML page, and searches for prices. If it finds a price below the value set in config.txt (flightMaxPriceForEmail) it sends an email telling us to check the site since the price has become reasonable.

To send an email we need to input our email credentials, I can't think of a way around this... maybe someone on GitHub will do something clever-er. The address and password you set in emailSettings will then send an email from that address to itself with the price and a link to the search page.

Note, I've set this up so it uses Gmail. If you want to use another mail server it's a bit fiddly getting the authentication correct but replace "smtp.gmail.com:587" with your other mail server.

Now you should be able to run the script (assuming you have python installed with)

python flight_finder_script.py

To run it at some time interval (say, hourly) on Linux/Unix/Mac systems, we use cron. Assuming it's installed (it should be), type 

crontab -e

To edit the scheduled tasks. Then add for hourly running: 

1 * * * * python /path/to/this/README/flight_finder_script.py	

where /path/to/this/README/ is the full path to the directory with the script.

Aaaaand you're done. To remove it, again type
crontab -e 
and remove that line.

Have fun, please let me know of any suggestions. For other flight sites (or currencies), you'll have to tweak the regular expression that looks for the prices in the results page.

Peace,
Chris 
