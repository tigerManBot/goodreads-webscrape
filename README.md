Description
-----------

This project is a webscraper for the goodreads website. It features two programs.    
1) get_author_data: takes an author's name as input and delivers data about that author.

2) get_book_data: takes a book title as input and delivers data about that book.


Input
-----

The author name/book title can be entered through command line arguments.  
If there are no command line arguments, then the program will ask for the author name/book title 
through terminal input.  

The author name/book title does not need to be spelled perfectly.  
However, the search will fail if the spelling is too far off.  


get_author_data
---------------

This program gathers data for an author.  
The data this program gets for that author:  
Average rating, total ratings, total reviews, distinct works, most liked quote, and bio.


get_book_data
-------------

This program gathers data for a book and opens the 3 most liked reviews.  
The data this program gets for that book:  
Average rating, total ratings, total reviews, and the rating distribution. 

The rating distribution is the distribution of stars, shown by % of star ratings, and the number of 
star ratings.  
For example: Five Stars: 42% (4415), Four Stars: 42% (4415), etc.  

After the data is displayed, the 3 most liked reviews open up in new tabs.  
Once the user is done reading the reviews, they can press any key(via terminal prompt) to exit.


Requirements
------------
selenium and the Firefox/Chrome are required.  
The default browser used is Firefox.  
To change the default browser, replace: browser = webdriver.Firefox()  
with: browser = webdriver.Chrome()  
This line can be found near the top of def main(). 

Other used modules: time, sys, and re.

selenium potential issues
-------------------------

if you are using Firefox, then you need to have geckodriver.exe in the same folder as the python version you  
are using.  
For me, that path is: 
C:\Users\User_name\AppData\Local\Programs\Python\Python310  

If you switch to google chrome, then you need chromedriver.exe in that python folder.  

Sample output folders
---------------------

There are two folders for each program showing some sample output.  
Do note that this data changes over time and might not perfectly match the current 
goodreads data.  
Especially for popular books and authors, this data changes daily.  

