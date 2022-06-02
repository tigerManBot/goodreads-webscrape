Description
-----------

This project is a webscraper for the goodreads website. It features two programs.    
1) get_author_data  
2) get_book_data  

get_author_data
---------------

This program gathers data for an author. The user can enter the author's name through the  
command line. If no command line arguments are present, then the program gets the author's name 
through terminal input.  
The data this program gets for that author:  
Average rating, total ratings, total reviews, distinct works, most liked quote, and bio.

Sample output for get_author_data
---------------------------------
![](../Users/Adam Anwar/Pictures/Screenshots/Screenshot (658).png)


get_book_data
-------------


Requirements
------------

selenium and the Firefox browser are required (though changing the code to use chrome would be easy). 

Other used modules: time, sys, and re.

selenium and Firefox potential issues
-------------------------------------

You need to have geckodriver.exe in the same folder as the python version you are using.
For me, that path is: 
C:\Users\User_name\AppData\Local\Programs\Python\Python310  
If you switch to google chrome, then you need chromedriver.exe in that python folder.  

