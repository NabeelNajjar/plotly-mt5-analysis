from bs4 import BeautifulSoup

import urllib.request

class ForexFactoryScraper:

    def __init__(self, month_select):
        self._url = 'https://www.forexfactory.com/calendar.php?month=' + month_select

    def _extract_day(self, row_html):
        day_date = row_html.find("td", {"class": "calendar__date"}).text.strip()

        return day_date[:3], day_date[3:]

    def _extract_currency(self, row_html):
        return row_html.find("td", {"class":"calendar__currency"}).text.strip()

    def _extract_event(self, row_html):
        return row_html.find("td", {"class":"calendar__event"}).text.strip()

    def _extract_html_data(self):

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        response = opener.open(self._url)
        result = response.read().decode('utf-8', errors='replace')

        return BeautifulSoup(result,"html.parser")

    def begin_extraction(self):
        parsed_html = self._extract_html_data()
        table = parsed_html.find_all("tr", class_="calendar_row")

        current_extracted_day, current_extracted_date = None, None
        
        for row in table:
            
            # Recurring day and date is blank
            day, date = self._extract_day(row)
            current_extracted_day = day or current_extracted_day
            current_extracted_date = date or current_extracted_date

            currency = self._extract_currency(row)
            event = self._extract_event(row)
            time = row.find_all("td", {"class":"calendar__time"})
            impact = row.find_all("td", {"class":"impact"})

            if current_extracted_day in ['Sat', 'Sun']:
                continue

            #print("\n\n")
            print(current_extracted_date)
            print(current_extracted_day)
            print(currency)
            print(event)
            print("\n\n")
            #print("\n\n")
            #print(time)
            #print("\n\n")
            #print(impact)

ff_scraper = ForexFactoryScraper('this')
ff_scraper.begin_extraction()