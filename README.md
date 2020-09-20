# Introduction

While using some of the many other Instagram comment scraping scripts on the internet, I ran into an issue: none of them scraped the date and time at which each comment was posted. This was an issue for me, as part of my job required tracking new comments on posts with lots of engagement day-to-day. This script allows a user to scrape comments on an Instagram post (plus the comments' date and time of posting, author, and number of likes) from before or after a certain date and time, or scrape all comments on the post.

### Notes
Only public posts can be scraped.

# Installation

This script runs using Python 3.

1. Clone or download this repository.
2. Pip install the dependencies listed below.
3. Install [Chromedriver](https://chromedriver.chromium.org/). In "main.py", change the DRIVER_PATH variable to the absolute path of the Chromedriver file.

## Dependencies

You will need to install the following libraries (consider doing this inside of a Python virtual environment):

* [BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/)
* [pytz](https://pypi.org/project/pytz/)
* [Selenium](https://pypi.org/project/selenium/)

# Usage

```
main.py [post_link] [range_identifier] [date] [time]

Required arguments:

- post_link                                 Link to the Instagram post to be scraped.

Optional arguments (as of now, all optional arguments must be present):

- range_identifier                          Specifies comments to be scraped before or after a certain datetime. 'before' or 'after'
- date                                      Specifies the before or after date. Format mm/dd/yyyy
- time                                      Specifies the before or after time. Timezone is UTC, 24-hour clock. Format hh:mm

```

### Example 1

Suppose you want to scrape all comments on one of Google's Instagram posts. Run the following commands:

```
python main.py https://www.instagram.com/p/CFKVfCiFL81/
```

### Example 2

Suppose you want to scrape all comments posted after September 16, 2020 at 4 PM EST. Run the following commands:

```
python main.py https://www.instagram.com/p/CFKVfCiFL81/ after 09/16/2020 20:00
```