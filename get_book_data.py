from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from time import sleep
import sys


def get_title():
    """Returns the book name as a list as each word is needed separately for the get url function.
    This can be given either by command line arguments or by temrinal input if no command line argument was given."""
    if len(sys.argv) <= 1:
        # in case there was no command line arguments given
        book_title = input("Enter a book title: ")
        return book_title.split()
    else:
        return [word for word in sys.argv[1:]]  # skips the program name


def get_url(book_title):
    """returns the url that will be opened in the browser.
    At this point, book_title is still a list."""
    first_part = "https://www.goodreads.com/search?q="
    second_part = ""
    for index, word in enumerate(book_title):
        if index == len(book_title) - 1:
            second_part += word
            break
        else:
            second_part += word + '+'

    return first_part + second_part


def exit_sign_in_popup(browser):
    """Closes the sign-in pop up."""
    x_button = browser.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]')
    x_button.click()
    sleep(1)


def exit_beta_version(browser):
    """There is a beta version of the site that sometimes pops up, this function reverts the site back to
    the original version."""
    try:
        beta_button = browser.find_element(By.XPATH, '/html/body/div[1]/div[1]/main/div[5]/div/button')
        beta_button.click()
        sleep(1)
        leave_button = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/button/span')
        leave_button.click()
        sleep(3)
        # the sign-in pop up shows again
        exit_sign_in_popup(browser)
    except NoSuchElementException:
        return()


def display_rating_data(title, avg_rating, total_ratings, total_reviews):
    """Displays the rating data to terminal."""
    print(f"Title: {title}")
    print(f"Average rating: {avg_rating}")
    print(f"Total ratings: {total_ratings}")
    print(f"Total reviews: {total_reviews}")


def display_rating_distribution(rating_distribution):
    """Displays the distribution of 1-5 star ratings.
    Shows % and total."""
    print("\nRatings distribution: ")
    print(f"Five stars: {rating_distribution[0]}")
    print(f"Four stars: {rating_distribution[1]}")
    print(f"Three stars: {rating_distribution[2]}")
    print(f"Two stars: {rating_distribution[3]}")
    print(f"One star: {rating_distribution[4]}")


def main():
    print()

    title_as_lst = get_title()
    url = get_url(title_as_lst)

    # open a browser page that is the result of a book search on goodreads
    browser = webdriver.Firefox()
    browser.get(url)

    # click on the appropriate book
    # book_link = browser.find_element(By.PARTIAL_LINK_TEXT, book_title_as_str)
    book_link = browser.find_element(By.CLASS_NAME, 'bookTitle')
    book_link.click()
    sleep(2)

    # close the sign-in pop ups and exits the beta version if the browser defaults to that version of goodreads
    exit_sign_in_popup(browser)
    exit_beta_version(browser)

    # get the book title, properlly formatted
    formatted_book_title = browser.find_element(By.ID, "bookTitle").text

    # get the average rating located at the top of the page
    avg_rating = browser.find_element(By.XPATH, './/span[@itemprop = "ratingValue"]').text

    # get the total ratings located nearby the avg_rating
    review_totals = browser.find_elements(By.XPATH, './/a[@class = "gr-hyperlink"]')
    total_ratings = review_totals[0].text
    total_reviews = review_totals[1].text

    # click 'Rating details' located next to the average rating
    rating_details_option = browser.find_element(By.LINK_TEXT, "Rating details")
    rating_details_option.click()
    sleep(1)    # see later if this can be brought down to 1

    # Get the ratings distribution, % of 5 star, total 5 stars, etc.
    rating_distribution = []
    five_stars_distribution = browser.find_element(By.XPATH, '//*[@id="rating_distribution"]/tbody/tr[1]/td[2]').text
    rating_distribution.append(five_stars_distribution)

    four_stars_distribution = browser.find_element(By.XPATH, '//*[@id="rating_distribution"]/tbody/tr[2]/td[2]').text
    rating_distribution.append(four_stars_distribution)

    three_stars_distribution = browser.find_element(By.XPATH, '//*[@id="rating_distribution"]/tbody/tr[3]/td[2]').text
    rating_distribution.append(three_stars_distribution)

    two_stars_distribution = browser.find_element(By.XPATH, '//*[@id="rating_distribution"]/tbody/tr[4]/td[2]').text
    rating_distribution.append(two_stars_distribution)

    one_star_distribution = browser.find_element(By.XPATH, '//*[@id="rating_distribution"]/tbody/tr[5]/td[2]').text
    rating_distribution.append(one_star_distribution)

    display_rating_data(formatted_book_title, avg_rating, total_ratings, total_reviews)
    display_rating_distribution(rating_distribution)

    # open in a new tab the top three reviews (click 'see review' at the bottom of the review)
    top_reviews = browser.find_elements(By.LINK_TEXT, "see review")
    for review in top_reviews[:3]:
        review.send_keys(Keys.CONTROL, Keys.ENTER)  # opens link in new tab
        sleep(1)

    still_reading = input("\nEnter any key once you're done reading the top reviews: ")
    browser.quit()


if __name__ == "__main__":
    main()

    print()
