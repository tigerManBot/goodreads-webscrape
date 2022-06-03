from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from time import sleep
import sys
import re


def get_author_name():
    """Returns the authors name as a list (first/middle/last are all needed separately for the url
    Can be given either by command line arguments or by terminal input if no command line argument was given."""
    if len(sys.argv) <= 1:
        # in case there was no command line arguments given
        name = input("Enter an author's name: ").title()
        return name.split()  # turn into a list
    else:
        return [word.title() for word in sys.argv[1:]]
        # skips the program name and uses title instead of capitalize
        # because capitalize breakes with names like George R.R. Martin


def get_url(author_name):
    """returns the url that will be opened in the browser."""
    first_part = "https://www.goodreads.com/search?utf8=✓&q="
    second_part = ""
    for index, word in enumerate(author_name):
        if index == len(author_name) - 1:
            second_part += word
            break
        else:
            second_part += word + '+'

    return first_part + second_part


def get_author_link(browser, user_inputed_author_name):
    """Gets the correct author link to click on.
    It compares each author link with the user inputted author_name.
    The link with the the most matches will be the link that gets clicked.

    This is necessary because some search results will have multiple authors listed.
    Without this function, the user_inputed_author_name would have to match exactly what the
    author's name is on goodreads. This function allows for some spelling/spacing issues in user input,
    though the user input could still break depending on how bad their spelling is."""
    author_links = browser.find_elements(By.XPATH, './/a[@class = "authorName"]')[:5]
    # There are many author links on the page, so I don't want to compare them all
    # I arbitrariliy chose to cap the links at size 5 as this seems reasonable

    author_links_lowered = [name.text.lower() for name in author_links]     # lowered for string comparisons
    user_inputed_author_name = user_inputed_author_name.lower()

    # compare each name in author_links_lowered to the user_inputed_author_name
    # getting the character match count for each name in author_links_lowered
    match_counts = []
    for name in author_links_lowered:
        matches = 0
        for j in range(min(len(user_inputed_author_name), len(name))):  # if one string is smaller, don't out of range
            matches += user_inputed_author_name[j] == name[j]

        match_counts.append(matches)

    max_index = match_counts.index((max(match_counts)))     # index with the most matches
    return author_links[max_index]


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
        return


def display_rating_data(name, avg_rating, total_ratings, total_reviews, distinct_works, quote):
    """prints all author data to terminal"""
    print(f"Author: {name}")
    print(f"Average rating: {avg_rating}")
    print(f"Total ratings: {total_ratings}")
    print(f"Total reviews: {total_reviews}")
    print(f"Distinct works: {distinct_works}")
    print(f"Most liked quote: {quote}")


def get_id(current_url):
    """every author has a unique id on good reads. This number can be helpful in gathering information on
    the author, and is found in the current url"""
    id_regex = re.compile(r"\d+")   # the only number in the url
    match_obj = id_regex.search(current_url)

    if match_obj:
        return match_obj.group()
    else:
        print("\nError, could not find the author's id.")
        exit()


def get_bio(author_unique_id, browser):
    """Function that returns the author's bio.
    The entire bio might have a '...more' option to click to the get the rest of the bio.
    Though, this more option is not present in all author bios."""
    # first, check fore the more option
    try:
        more_dropdown_dots = browser.find_element(By.CSS_SELECTOR, 'body > div.content > div.mainContentContainer > '
                                                                   'div.mainContent > div.mainContentFloat > d'
                                                                   'iv.reverseColumnSizes > div.rightContainer > '
                                                                   'div.aboutAuthorInfo > a')
        more_dropdown_dots.click()
        sleep(1)
        bio = browser.find_element(By.XPATH, f'//span[@id="freeTextauthor{author_unique_id}"]').text
    except NoSuchElementException:
        # otherwise, the bio element will be different
        bio = browser.find_element(By.XPATH, f'//span[@id="freeTextContainerauthor{author_unique_id}"]').text

    return bio


def main():
    print()

    author_name_as_lst = get_author_name()
    url = get_url(author_name_as_lst)

    # open a browser page that is the result of an author search on goodreads
    browser = webdriver.Firefox()
    browser.get(url)
    sleep(1)

    # click on the link under the book that has the author's name
    author_name_as_str = ' '.join(author_name_as_lst)
    author_link = get_author_link(browser, author_name_as_str)
    author_link.click()
    sleep(3)    # sometimes the browser can stall

    # close the sign-in pop ups and exits the beta version if the browser defaults to that version of goodreads
    exit_sign_in_popup(browser)
    exit_beta_version(browser)

    # get the current url in order to get the unique author id which is needed for the bio variable
    current_url = browser.current_url
    author_unique_id = get_id(current_url)

    # get the average rating
    avg_rating = browser.find_element(By.XPATH, './/span[@class = "average"]').text

    # get the total ratings and reviews
    totals_lst = browser.find_elements(By.XPATH, './/span[@class = "value-title"]')
    total_ratings = totals_lst[0].text
    total_reviews = totals_lst[1].text

    # get the number of distinct works
    distinct_works = browser.find_element(By.PARTIAL_LINK_TEXT, "distinct works").text

    most_liked_quote = browser.find_element(By.XPATH, './/div[@class = "quoteText"]').text
    sleep(1)

    # get the authors bio
    bio = get_bio(author_unique_id, browser)

    sleep(1)
    browser.quit()

    display_rating_data(author_name_as_str, avg_rating, total_ratings, total_reviews, distinct_works, most_liked_quote)
    print(f"\nBio:\n {bio}")


if __name__ == "__main__":
    main()

    print()
