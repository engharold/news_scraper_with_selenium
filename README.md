# News web scraper robot

This is a robot example using Python with Selenium to automate the process of extracting data from The New York Times news site (https://www.nytimes.com/), which searches for a phrase, generates an Excel file with the desired data from the news and downloads the pictures into the output folder. The project uses the POM design pattern.


## Parameters used:

The process uses the following parameters via a JSON file:
- search phrase
- news category/section/topic
- number of months for which you need to receive news:
    Example of how this should work: 0 or 1 - only the current month, 2 - current and previous month,
    3 - current and two previous months, and so on


## Process summary:

When executed, the task will do the following steps: 
    
1. Open The New York Times site
2. Input a phrase in the search field
3. If found any results, filter them by the section and date range according to the parameters defined in the JSON file
4. For each news, download its picture and store in an Excel file the following information:
    - Date
    - Title
    - Description
    - Picture file name
    - Count of search phrase in the title and description
    - Set to True if the title or description contains any amount of money. Otherwise, set to False
