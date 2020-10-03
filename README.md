# scrape

web scraping experiments

It's time for me to update my web scraping skills.

I'll put aside `curl`, `wget`, and my dusty old Perl scripts
and try something new.

## scrapy and 750words.com

I'll start with scrapy, and with a simple task:
I want to retrieve my daily writing from 750words.com.
The difficulty is I need to login to get my stuff.

But let's be patient and start with the tutorial.

<https://docs.scrapy.org/en/latest/intro/tutorial.html>

This looks like a good explanation of how to login:

<https://towardsdatascience.com/scrapy-this-is-how-to-successfully-login-with-ease-ea980e2c5901>

Well it's nice except the code example has about 10 bugs...
This page will also help:

<https://python.gotrained.com/scrapy-formrequest-logging-in/>

So we have two working examples:

    scrapy crawl quotes
    scrapy crawl login

And now a working program to get my writing of the day:

    scrapy crawl sevenfifty -s LOG_ENABLED=0

or better yet, to catch errors:

    scrapy crawl sevenfifty -s LOG_LEVEL=WARNING > words.txt

and better yet, a way to run the spider from anywhere:

    scrapy runspider ~/scrape/tutorial/tutorial/spiders/sevenfifty_spider.py -s LOG_LEVEL=WARNING

Now I've run into a problem for Strava, the `robots.txt` file disallows visiting the dashboard, and nearly all pages on the site.
That's OK, I can use `ROBOTS_OBEY=False`. like so:

    scrapy runspider ~/scrape/tutorial/tutorial/spiders/strava_spider.py -s ROBOTSTXT_OBEY=False

I have other problems with Strava, but that takes care of `robots.txt` exclusion.
