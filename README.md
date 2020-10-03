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

## scraping for fast.ai

I could probably use scrapy to get a bunch of images from a Bing or Google search as required by fast.ai, but here's a shortcut

[How to scrape Google for Images to train your Machine Learning classifiers on](https://medium.com/@intprogrammer/how-to-scrape-google-for-images-to-train-your-machine-learning-classifiers-on-565076972ce)

... except it's of course out-of-date. And it doesn't tell you what it's trying to do: it just applies a recipe.

This page gives the same code, with no more explanation of what we are trying to do:

<https://mc.ai/fast-deployment-of-an-image-classification-web-app-with-fast-ai/>

So does this one:

<https://towardsdatascience.com/fantastic-and-straightforward-image-classification-with-fastai-library-for-pytorch-30c3380ac284>

Wow, that's a popular technique... No wonder Jeremy now suggests using the Bing API and suggests that non-API techniques would be against the terms of service of the search engine, though techniques can be found online...

Anyway, at least in that last article I see an image of what the resulting CSV is supposed to look like... OK so we want URLs of the original image hosted by the indexed sites. We don't want to use Google's thumbnails, though I bet they would work OK too. But ok let's go for the originals.

I wonder if some sites may prevent downloading images directly, if you are not coming from the original artcile... Well I'll deal with that if it comes to it. The search does give us that info too, so it probably wouldn't be too hard to pretend like we come from the article...

Google has changed (obfuscated?) something since that bit of code was excerpted.

So somewhere in here:

```
/imgres?
imgurl=
https%3A%2F%2Fi.guim.co.uk%2Fimg%2Fmedia%2F9b7827c38c5ab2dd2fc07d8b5b744d3d246c8999%2F0_55_3500_2100%2Fmaster%2F3500.jpg%3Fwidth%3D1200%26height%3D900%26quality%3D85%26auto%3Dformat%26fit%3Dcrop%26s%3D471fd2c6885b8679de17245c7ed6238f
&imgrefurl=
https%3A%2F%2Fwww.theguardian.com%2Fworld%2F2017%2Fjun%2F22%2Fyellowstone-grizzly-bears-endagered-species-protections-lifted&tbnid=JWFktgKEdWk3OM&vet=12ahUKEwiOwpiUnJnsAhUVgHMKHUfRDfYQMygCegUIARDRAQ..i
&docid=
_tfcMJ_JE6SviM&w=1200&h=900&q=grizzly%20bear
&ved=2ahUKEwiOwpiUnJnsAhUVgHMKHUfRDfYQMygCegUIARDRAQ
```

should be something like this image, which appears in the linked article:

```
https://i.guim.co.uk/img/media/9b7827c38c5ab2dd2fc07d8b5b744d3d246c8999/0_55_3500_2100/master/3500.jpg?width=620&quality=85&auto=format&fit=max&s=7f39252becb078b8494b056b611bb38e
```

and indeed it looks like it's there, in the URL parameter `imgurl`:


```
https%3A%2F%2Fi.guim.co.uk%2Fimg%2Fmedia%2F9b7827c38c5ab2dd2fc07d8b5b744d3d246c8999%2F0_55_3500_2100%2Fmaster%2F3500.jpg%3Fwidth%3D1200%26height%3D900%26quality%3D85%26auto%3Dformat%26fit%3Dcrop%26s%3D471fd2c6885b8679de17245c7ed6238f

```

It just needs to be URL decoded. Enter `decodeURIComponent()` which gives us:

```
https://i.guim.co.uk/img/media/9b7827c38c5ab2dd2fc07d8b5b744d3d246c8999/0_55_3500_2100/master/3500.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=471fd2c6885b8679de17245c7ed6238f
```

seems close enough.

Now all we need to do is produce the equivalent piece of code, and we can follow all those helpful articles...

Let's l;ook into that tomorrow!
