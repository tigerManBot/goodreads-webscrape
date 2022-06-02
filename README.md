Description
-----------

This project is a webscraper for the goodreads website. It features two programs.    
1) get_author_data  
2) get_book_data  


Input
-----

The author name/book title can be entered through command line arguments.  
If there are no command line arguments, then the program will ask for the author name/book title 
through terminal input.


get_author_data
---------------

This program gathers data for an author.  
The data this program gets for that author:  
Average rating, total ratings, total reviews, distinct works, most liked quote, and bio.


get_book_data
-------------


Requirements
------------

selenium and the Firefox browser are required (though changing the code to use chrome would be easy). 

Other used modules: time, sys, and re.

selenium potential issues
-------------------------

You need to have geckodriver.exe in the same folder as the python version you are using.
For me, that path is: 
C:\Users\User_name\AppData\Local\Programs\Python\Python310  
If you switch to google chrome, then you need chromedriver.exe in that python folder.  

Sample output folders
---------------------

There are two folders for each program showing some sample output.  
Do note that this data changes over time and might not perfectly match the current 
goodreads data.

