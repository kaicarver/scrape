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

... except it's of course out-of-date. And it doesn't tell you what it's trying to do: it just applies a recipe, asking us to "invoke the following command":

```javascript
urls = Array.from(document.querySelectorAll('.rg_di .rg_meta')).map(el=>JSON.parse(el.textContent).ou);
window.open('data:text/csv;charset=utf-8,' + escape(urls.join('\n')));
```

But what is it trying to do? Give a man a scrape, he'll scrape for a day. But I wish to be taught how to scrape...

This other page gives the same code, with no more explanation of what we are trying to do:

<https://mc.ai/fast-deployment-of-an-image-classification-web-app-with-fast-ai/>

So does this one:

<https://towardsdatascience.com/fantastic-and-straightforward-image-classification-with-fastai-library-for-pytorch-30c3380ac284>

Wow, that's a popular technique... No wonder Jeremy now suggests using the Bing API and suggests that non-API techniques would be against the terms of service of the search engine, though techniques can be found online...

Anyway, at least in that last article I see an image of what the resulting CSV is supposed to look like... OK so we want URLs of the original image hosted by the indexed sites. We don't want to use Google's thumbnails, though I bet they would work OK too. But ok let's go for the originals.

I wonder if some sites may prevent downloading images directly, if you are not coming from the original artcile... Well I'll deal with that if it comes to it. The search does give us that info too, so it probably wouldn't be too hard to pretend like we come from the article...

Google has changed (obfuscated?) something since that bit of code was excerpted. If we check out one of the results returned by this kind of image search:

<https://www.google.com/search?q=grizzly+bear&tbm=isch>

we see the result is an `<a>` tag containing a `<div>` containg an image thumbnail:

```html
<a class="wXeWr islib nfEiy mM5pbd" jsname="sTFXNd" jsaction="click:J9iaEb;" data-nav="1" tabindex="0" style="height: 180px;" href="/imgres?imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fa%2Fa9%2FGrizzlyBearJeanBeaufort.jpg&amp;imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FGrizzly_bear&amp;tbnid=wOKSLxVmunP82M&amp;vet=12ahUKEwif78fQjJrsAhVQSxoKHR82CGoQMygAegUIARDQAQ..i&amp;docid=OAt6mxS_RUoSZM&amp;w=1920&amp;h=1381&amp;q=grizzly%20bear&amp;ved=2ahUKEwif78fQjJrsAhVQSxoKHR82CGoQMygAegUIARDQAQ" data-navigation="server">
  <div class="bRMDJf islir" jsname="DeysSe" style="height: 181px; margin-left: -14px; margin-right: -29px;" jsaction="mousedown:npT2md; touchstart:npT2md;">
    <img class="rg_i Q4LuWd" src="data:image/jpeg;base64,/9j/...H1/TBP3v/AFDhZJDxkz//2Q==" data-deferred="1" jsname="Q4LuWd" width="251" height="181" alt="Grizzly bear - Wikipedia" data-iml="720.0449999945704" data-atf="true">
  </div>
  <div class="c7cjWc"></div>
</a>
```

It looks like somewhere in the link, the complicated `href` attribute of the `<a>`:

<pre>
/imgres?
imgurl=
<b>https%3A%2F%2Fi.guim.co.uk%2Fimg%2Fmedia%2F9b7827c38c5ab2dd2fc07d8b5b744d3d246c8999%2F0_55_3500_2100%2Fmaster%2F3500.jpg%3Fwidth%3D1200%26height%3D900%26quality%3D85%26auto%3Dformat%26fit%3Dcrop%26s%3D471fd2c6885b8679de17245c7ed6238f</b>
&imgrefurl=
https%3A%2F%2Fwww.theguardian.com%2Fworld%2F2017%2Fjun%2F22%2Fyellowstone-grizzly-bears-endagered-species-protections-lifted&tbnid=JWFktgKEdWk3OM&vet=12ahUKEwiOwpiUnJnsAhUVgHMKHUfRDfYQMygCegUIARDRAQ..i
&docid=
_tfcMJ_JE6SviM&w=1200&h=900&q=grizzly%20bear
&ved=2ahUKEwiOwpiUnJnsAhUVgHMKHUfRDfYQMygCegUIARDRAQ
</pre>

we should be something like this image, which appears in the linked article:

```html
https://i.guim.co.uk/img/media/9b7827c38c5ab2dd2fc07d8b5b744d3d246c8999/0_55_3500_2100/master/3500.jpg?width=620&quality=85&auto=format&fit=max&s=7f39252becb078b8494b056b611bb38e
```

and indeed it looks like it's there, in the URL parameter `imgurl`:

<pre>
<b>https%3A%2F%2Fi.guim.co.uk%2Fimg%2Fmedia%2F9b7827c38c5ab2dd2fc07d8b5b744d3d246c8999%2F0_55_3500_2100%2Fmaster%2F3500.jpg%3Fwidth%3D1200%26height%3D900%26quality%3D85%26auto%3Dformat%26fit%3Dcrop%26s%3D471fd2c6885b8679de17245c7ed6238f</b>
</pre>

It just needs to be URL decoded. Enter `decodeURIComponent()` which gives us:

<pre>
<b>
https://i.guim.co.uk/img/media/9b7827c38c5ab2dd2fc07d8b5b744d3d246c8999/0_55_3500_2100/master/3500.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=471fd2c6885b8679de17245c7ed6238f
</b>
</pre>

Hey, that looks like an image URL! Close enough to the one we can see in the article.

Now that we know what we're looking for, all we need to do is produce the equivalent piece of code, that we can hopefully just plug in to all those helpful articles, and we'll be all set.

Let's go back to the first line of that magical command that doesn't work anymore and understand what it does so we can fix it:

```javascript
urls = Array.from(document.querySelectorAll('.rg_di .rg_meta'))
  .map(el => JSON.parse(el.textContent).ou);
```

I'll guess it's trying to make a list of URLs, which Google in its wisdom now stores somewhere slightly different.

More specifically, `querySelectorAll()` is getting all the document elements of class `rg_di` and `rg_meta`, putting them in an `Array`, then via `map()`, for each of these elements, it's... parsing the JSON content of the tag, which apparently produces an object whose member `ou` (aha, an abbreviation for "original url") contains a URL, each of which is then stored in the `urls` array.

OK, whatever, the HTML code is different now, all we know is we want to produce an array of URL strings. The tags now have different classes, and the URL has to be dug out of part of a long string and translated.

Let's try this:

```javascript
urls = Array.from(document.querySelectorAll('.wXeWr'))
  .map(el => el.href);
```

It looks like it will work and... Woops!

```javascript
(48) ["https://www.google.com/imgres?imgurl=https%3A%2F%2…d=2ahUKEwif78fQjJrsAhVQSxoKHR82CGoQMygAegUIARDQAQ", "https://www.google.com/imgres?imgurl=https%3A%2F%2…d=2ahUKEwif78fQjJrsAhVQSxoKHR82CGoQMygBegUIARDSAQ", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
```

It looks like it doesn't actually fill in the `href` attribute unless you actually interact with the image thumbnail. Tricky, tricky, Google...

One solution would be to actually click on every thumbnail... I actually tried to do that in an automated way, and it didn't work. Google, you win, I give up now, before attempting to write my own [Selenium](https://www.selenium.dev/)...

How about trying the same thing with Bing image search? That was the original goal, right, to get Bing images? I can't do it via the authorized Bing API because it seems I need to pay to get a key, perhaps because I already made use of a free account in the past, dunno...

So to recap, the Google image search I was unable to hack 

<https://www.google.com/search?q=grizzly+bear&tbm=isch>

has this Bing equivalent search:

<https://www.bing.com/images/search?q=grizzly+bear>

Let's go!

And by the way, if I fail with Bing, I can also try my own personal favorite search tool, Duckduckgo, or Baidu, or Yandex, etc.

<https://duckduckgo.com/?q=grizzly+bear&iax=images&ia=images>

<https://image.baidu.com/search/index?tn=baiduimage&word=grizzly+bear>

<https://yandex.com/images/search?text=grizzly%20bear>

fast.ai already recommends to search for things in other languages, for a variety of results, so why not other search engines too. But let's not go too far down that rabbit hole for now, let's try if Bing is nicer than Google for my modest hacking attempt.

And really, scraping is an interesting endeavor. You feel a bit like a criminal... It's like Ocean's 11! Will the hero be able to walk away scott-free with a big bag of images? Oh my. I promise, I am not a criminal, and what I want to do is not a bad thing. But Google & co have the perfect right to try to stop me, because I'm sure there are plenty of abusers... Just not me!

So...

<https://www.bing.com/images/search?q=grizzly+bear>

Inspect...

Hmm, looks like the actual image URL doesn't appear unless you click on the image thumbnail... Grr...
