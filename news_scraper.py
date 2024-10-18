import logging
import traceback
import sys
sys.path.append( '.' )
from pages.HomePage import HomePage
from pages.ResultsPage import ResultsPage
from time import sleep
import json

def news_scraper():
    """
    Task to automate the process of extracting data from a news site (e.g. The New York Times).
    Parameters:
        The process must process three parameters that are read from a JSON file:
        - search phrase
        - news category/section/topic
        - number of months for which you need to receive news:
          Example of how this should work: 0 or 1 - only the current month, 2 - current and previous month,
          3 - current and two previous months, and so on

    Process summary:
        Store in an Excel file the following information for each news found:
        - Date
        - Title
        - Description
        - Picture file name (if the news has a picture, it has to be downloaded in the output folder)
        - Count of search phrase in the title and description
        - Set to True if the title or description contains any amount of money. Otherwise, set to False
    """
    #Setup logger
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    #Possible values for news section filter
    valid_sections = ["Any", "Arts", "Business", "Great Homes & Destinations", "New York",
         "Opinion", "Real Estate", "Travel", "U.S", "World"]
    
    try:
        #Gets the search phrase, section and months from JSON file data source
        with open("test_data/data.json") as json_file:
            test_data = json.load(json_file)
            search_phrase = test_data["search_phrase"]
            section = test_data["section"]
            months = test_data["months"]

        print(f"Searching news with phrase: {search_phrase} - Section: {section} - Months: {months}")
        assert len(search_phrase) > 0, f"Search phrase can't be empty"
        assert months >= 0, f"Invalid month number. It must be greater than or equal to zero"
        assert len(section) > 0 and section in valid_sections, f"Invalid section. Possible values: {valid_sections}"
        try:
            #Initializes the page objects that will be used and executes the process described before
            home_page = HomePage()
            results_page = ResultsPage()
            home_page.open_site("https://www.nytimes.com/")
            home_page.click_search_button()
            home_page.search_text(search_phrase)
            if results_page.has_results():
                results_page.filter_dates(months)
                results_page.select_section(section)
                sleep(10)
                results_page.process_results(search_phrase)
            else:
                logger.error(f"No results found. Please check the search phrase or refine it.")
        except Exception:
            logger.exception(traceback.format_exc())
    except AssertionError as err:
        raise AssertionError(err)
    except Exception:
        raise Exception(traceback.format_exc())


if __name__ == "__main__":
    news_scraper()