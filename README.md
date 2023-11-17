# Using Python for Slickdeals Frontpage Deals Scrapping into JSON format
The goal of this scrapping python script is to get all Slickdeals frontpage hot deals and conver them into json format and create alerts and send notifications to your own Discord Channel, Social Media, etc.

The script collects following data types:
* Title
* Store
* Price
* Likes
* Deal Link
* Image URL
* Posted Time

## Output Example:
```
[
  {
    "title": "16.5" SwissTech Executive Carry-On Underseater Luggage w/ Interlocking Zipper Pulls",
    "link": "https://slickdeals.net/f/17069485-16-5-swisstech-executive-carry-on-underseater-luggage-w-interlocking-zipper-pulls-black-15-free-s-h-w-walmart-or-35?src=frontpage_recombee_fallback",
    "image_url": "",
    "store": "Walmart",
    "price": "$15",
    "likes": "14",
    "time": "less than a minute",
    "time_in_min": 1
  },
  {
    "title": "Samsung EPP/EDU : 47mm Galaxy Watch6 Classic Smartwatch",
    "link": "https://slickdeals.net/f/17069410-galaxy-watch6-classic-smartwatch-wearables-samsung-us-59-49-with-trade-in-edu?src=frontpage_recombee_fallback",
    "image_url": "https://static.slickdealscdn.com/attachment/4/2/8/1/6/14546374.attach",
    "store": "Samsung",
    "price": "$59.50",
    "likes": "59",
    "time": "9 minutes",
    "time_in_min": 9
  }
]
```
