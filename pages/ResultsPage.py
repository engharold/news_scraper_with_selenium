import sys
sys.path.append('.')
from utils.DateUtils import DateUtils
from utils.MoneyUtils import MoneyUtils
from openpyxl import Workbook
from pages.BasePage import BasePage
from selenium.webdriver.common.by import By


class ResultsPage(BasePage):
    ORDER_BY = (By.CSS_SELECTOR, "[data-testid='SearchForm-sortBy']")
    NEWEST_OPTION = (By.CSS_SELECTOR, "option[value='newest']")
    DATE_RANGE_DROPDOWN = (By.CSS_SELECTOR, "[data-testid='search-date-dropdown-a']")
    RESULTS_LIST = (By.CSS_SELECTOR, "[data-testid='search-results']")
    RESULT_ITEM = (By.CSS_SELECTOR, "[data-testid='search-bodega-result']")
    RESULT_PICTURE = (By.CSS_SELECTOR, "[data-testid='search-bodega-result'] img[src]")
    SPECIFIC_DATES_OPTION = (By.CSS_SELECTOR, "button[value='Specific Dates']")
    SHOW_MORE_BUTTON = (By.CSS_SELECTOR, "button[data-testid='search-show-more-button']")
    START_DATE = (By.CSS_SELECTOR, "[data-testid='DateRange-startDate']")
    END_DATE = (By.CSS_SELECTOR, "[data-testid='DateRange-endDate']")
    AVAILABLE_SECTIONS = (By.CSS_SELECTOR, "[data-testid='multi-select-dropdown-list']")
    SECTION_BUTTON = (By.CSS_SELECTOR, "[data-testid='section']")
    SECTION_CHECKBOX = "[data-testid='DropdownLabelCheckbox']"

    def __init__(self):
        super().__init__()

    def has_results(self):
        if self.find_elements(self.RESULT_ITEM):
            return True
        else:
            return False

    def order_results_by_newest(self):
        self.select_value_from_list(self.ORDER_BY, value="newest")

    def select_section(self, section: str):
        self.click_element(self.SECTION_BUTTON)
        sections = self.find_elements(self.AVAILABLE_SECTIONS)
        if section in sections[0].text:
            checkbox_to_select = (By.CSS_SELECTOR, f"{self.SECTION_CHECKBOX}[value^='{section}']")
            self.click_element(checkbox_to_select)
        else:
            raise ValueError(f"Please check the filters or refine the search phrase. \n"
                             f"{section} section is not available for the results with the applied filters.")

    def filter_dates(self, months: int):
        """
        Defines the start date and end date to use in the date range filter, according to the number of months
        for which you need to receive news.
        Example of how this should work: 0 or 1 - only the current month, 2 - current and previous month,
        3 - current and two previous months, and so on
        """
        if months == 0 or months == 1:
            start_date = DateUtils.get_beginning_of_month(DateUtils.get_current_date())
            end_date = DateUtils.get_current_date_formatted()
        elif months > 1:
            past_months = months - 1  # Excluding current month
            end_date = DateUtils.get_current_date_formatted()
            start_date = DateUtils.calculate_start_date(
                reference_date=DateUtils.get_current_date(),
                months=past_months
            )
        else:
            raise ValueError(f"Please check. Month number must be greater than or equal to zero")

        self.select_date_range(start_date, end_date)

    def select_date_range(self, start_date: str, end_date: str):
        self.click_element(self.DATE_RANGE_DROPDOWN)
        self.click_element(self.SPECIFIC_DATES_OPTION)
        self.input_text(self.START_DATE, value=start_date)
        self.input_text(self.END_DATE, value=end_date)
        self.select_value_from_list(self.ORDER_BY, value="newest")

    def process_results(self, search_phrase: str, ):
        try:
            # Checks if there are still results after applying the different filters
            if self.find_elements(self.RESULT_ITEM):
                # Clicks the Show More button while it is present in the page
                while self.is_element_present(self.SHOW_MORE_BUTTON):
                    self.scroll_to_element(self.SHOW_MORE_BUTTON)
                    self.click_element_with_javascript(self.SHOW_MORE_BUTTON)

                # Gets all results
                results = self.find_elements(self.RESULT_ITEM)

                # creates an Excel workbook and worksheet that will be used to save the respective news info
                work_book = Workbook()
                work_sheet = work_book.active
                work_sheet['A1'] = "Date"
                work_sheet['B1'] = "Title"
                work_sheet['C1'] = "Description"
                work_sheet['D1'] = "Picture file name"
                work_sheet['E1'] = "Count of search phrase"
                work_sheet['F1'] = "Contains amount of money"
                for i in range(len(results)):
                    # Splits the text from the result to get the date, title, description
                    news_info = results[i].text.splitlines(keepends=False)

                    # Defines the locator to get the picture for the news
                    picture_locator = (By.XPATH, f"//*[@data-testid='search-bodega-result'][{str(i + 1)}]//img[@src]")

                    # Searches the picture element for the news
                    news_picture = self.find_element(picture_locator)

                    # Checks if there is a picture for the news
                    if news_picture:
                        # Reads picture info as byte
                        picture_bytes = news_picture.screenshot_as_png

                        # Defines the picture file name according to the row number of the news in the Excel file
                        picture_file_name = f"row_{str(i + 2)}_news_picture.png"

                        # Saves the picture in the output folder
                        open(f"./output/{picture_file_name}", 'wb').write(picture_bytes)
                    else:
                        picture_file_name = 'No picture available'

                    # Fills the cell with the news date which is the first item in news_info list
                    work_sheet['A' + str(i + 2)] = news_info[0]

                    """
                    Some times the news_info list may have a different length because of the info from the news.
                    If the length of the list is less than 4 the news title will be in the second item, and the 
                    description in the third one. Otherwise, the news title will be in the third item, and the
                    description in the fourth one.
                    """
                    if len(news_info) < 4:
                        news_title = news_info[1]
                        news_description = news_info[2]

                    else:
                        news_title = news_info[2]
                        news_description = news_info[3]

                    # Fills the cell with the news title:
                    work_sheet['B' + str(i + 2)] = news_title

                    # Fills the cell with the news description
                    work_sheet['C' + str(i + 2)] = news_description

                    # Fills the cell with the picture file name
                    work_sheet['D' + str(i + 2)] = picture_file_name

                    # Counts the search phrase in the title and description
                    news_title_description = f"{news_title} {news_description}".lower()
                    search_phrase_occurrences = news_title_description.count(search_phrase.lower())
                    work_sheet['E' + str(i + 2)] = search_phrase_occurrences

                    # Checks if the text from title and description contains any amount of money
                    # Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
                    news_has_money = MoneyUtils.text_has_money(news_title_description)

                    # Fills the cell with the count of the search phrase
                    work_sheet['F' + str(i + 2)] = news_has_money

                # Saves the Excel file
                work_book.save("./output/news_results.xlsx")

                # Closes the browser and the driver
                self.teardown()
            else:
                self.logger.debug(f"Please check. There are no results for the filter criteria.")

        except Exception as exc:
            self.logger.error(f"There was an error while processing the results: {exc}")
