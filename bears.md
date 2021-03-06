# Scraping images for fast.ai

For the "bear detector" of [Chapter 2](https://github.com/fastai/fastbook/blob/master/02_production.ipynb) of the fast.ai book, we need to collect images of bears (see "Gathering Data" section).

I had problems using the Bing image search API, the currently recommended method for fast.ai.
I can't use the authorized Bing API because it seems I need to pay to get a key, perhaps because I already made use of a free account in the past, dunno...

## Trying to scrape Google image search

So I thought of using something like [scrapy](https://scrapy.org/) to get the required bunch of images from a Bing or Google search, but searching around I found an attractive method:

[How to scrape Google for Images to train your Machine Learning classifiers on](https://medium.com/@intprogrammer/how-to-scrape-google-for-images-to-train-your-machine-learning-classifiers-on-565076972ce)

... except it's of course out-of-date. And the method doesn't tell you what it's trying to do: it just applies a recipe, asking us to "invoke the following command":

```javascript
urls = Array.from(document.querySelectorAll('.rg_di .rg_meta')).map(el=>JSON.parse(el.textContent).ou);
window.open('data:text/csv;charset=utf-8,' + escape(urls.join('\n')));
```

But what is it trying to do? Give a man a scrape, he'll scrape for a day. But I'd like to learn how to scrape...

This other page gives the same code, with no more explanation of what we are trying to do:

<https://mc.ai/fast-deployment-of-an-image-classification-web-app-with-fast-ai/>

So does this one:

<https://towardsdatascience.com/fantastic-and-straightforward-image-classification-with-fastai-library-for-pytorch-30c3380ac284>

Wow, that's a popular technique... No wonder Jeremy now suggests using the Bing API. He says in his lecture that non-API techniques would be against the terms of service of the search engine, but he does mention techniques can readily be found online...

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

## Trying to scrape Bing image search

How about trying the same thing with Bing image search? That was the original goal, right, to get Bing images. I couldn't use the API for some reason, so let's try another way?

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

Hmm, looks like on Bing, the actual image URL doesn't appear unless you click on the image thumbnail... Grr... Woops! No, that was duckduckgo that I was looking at...

Bing looks more promising. Using Inspect, I see an `<a>` element of class `iusc`  that contains a promising URL buried in some JSON stored in a custom attribute called `m` (which apparently stands for "media"):

```html
<a class="iusc" style="height:180px;width:269px" m="{"cid":"Ebdz7mQw","purl":"https://someinterestingfacts.net/10-facts-grizzly-bear/","murl":"https://someinterestingfacts.net/wp-content/uploads/2016/07/Canadian-Grizzly-Bear.jpg","turl":"https://tse1.mm.bing.net/th?id=OIP.Ebdz7mQwVEny-uVn3MWrOwHaE8&pid=15.1","md5":"11b773ee64305449f2fae567dcc5ab3b","shkey":"Y3pyj5i+UrMMPbfCwtWgEQ+gzRRt1j12rjFGyUX4VSc=","t":"10 Facts About Grizzly Bears - Some Interesting Facts","mid":"CB1AF235DF865E3CE2C61B8E5D897386CEC2541C","desc":"grizzly bear facts bears canadian grolar interesting"}" onclick="sj_evt.fire('IFrame.Navigate', this.href); return false;" href="/images/search?view=detailV2&ccid=Ebdz7mQw&id=CB1AF235DF865E3CE2C61B8E5D897386CEC2541C&thid=OIP.Ebdz7mQwVEny-uVn3MWrOwHaE8&mediaurl=https%3a%2f%2fsomeinterestingfacts.net%2fwp-content%2fuploads%2f2016%2f07%2fCanadian-Grizzly-Bear.jpg&exph=1068&expw=1600&q=grizzly+bear&simid=608025979016708716&ck=87468A39749C9C4C3F21A32C7BF7D149&selectedIndex=0&FORM=IRPRST" h="ID=images,5189.1" data-focevt="1">
  <div class="img_cont hoff">
    <img class="mimg" style="color: rgb(140, 98, 63);" height="180" width="269" src="https://th.bing.com/th/id/OIP.Ebdz7mQwVEny-uVn3MWrOwHaE8?w=269&h=180&c=7&o=5&dpr=1.5&pid=1.7" alt="Image result for grizzly bear" data-thhnrepbd="1" data-bm="176">
  </div>
</a>
```

Looking closer at that JSON...

```json
{"cid":"Ebdz7mQw","purl":"https://someinterestingfacts.net/10-facts-grizzly-bear/","murl":"https://someinterestingfacts.net/wp-content/uploads/2016/07/Canadian-Grizzly-Bear.jpg","turl":"https://tse1.mm.bing.net/th?id=OIP.Ebdz7mQwVEny-uVn3MWrOwHaE8&pid=15.1","md5":"11b773ee64305449f2fae567dcc5ab3b","shkey":"Y3pyj5i+UrMMPbfCwtWgEQ+gzRRt1j12rjFGyUX4VSc=","t":"10 Facts About Grizzly Bears - Some Interesting Facts","mid":"CB1AF235DF865E3CE2C61B8E5D897386CEC2541C","desc":"grizzly bear facts bears canadian grolar interesting"}
```

we see a `murl` property which has what we want!

<https://someinterestingfacts.net/wp-content/uploads/2016/07/Canadian-Grizzly-Bear.jpg>

OK, so let's try to catch them all. To get all the elements of this type:

```javascript
all = document.querySelectorAll('.iusc')

<- NodeList(35) [a.iusc, a.iusc, a.iusc, a.iusc, ...]
```

That gives us a `NodeList` of 35 elements. Let's look at what's in the `m` attribute of the first element, `all[0]`, and lo, we have the JSON string:

```javascript
el = all[0]
el.attributes.m.value

<- {"cid":"Ebdz7mQw","purl":"https://someinterestingfacts.net/10-facts-grizzly-bear/","murl":"https://someinterestingfacts.net/wp-content/uploads/2016/07/Canadian-Grizzly-Bear.jpg","turl":"https://tse1.mm.bing.net/th?id=OIP.Ebdz7mQwVEny-uVn3MWrOwHaE8&pid=15.1","md5":"11b773ee64305449f2fae567dcc5ab3b","shkey":"Y3pyj5i+UrMMPbfCwtWgEQ+gzRRt1j12rjFGyUX4VSc=","t":"10 Facts About Grizzly Bears - Some Interesting Facts","mid":"CB1AF235DF865E3CE2C61B8E5D897386CEC2541C","desc":"grizzly bear facts bears canadian grolar interesting"}
```

We can get the part we want out of the JSON string using the same method used by the original Google-scraping script that doesn't work anymore:

```javascript
JSON.parse(el.attributes.m.value).murl

<- "https://someinterestingfacts.net/wp-content/uploads/2016/07/Canadian-Grizzly-Bear.jpg"
```

Hooray, that's one URL. 

Now let's try to get them all at once. We get the elements we are interested in with `querySelectorAll()`, put them in an `Array`, use `map()` to apply `JSON.parse()` to each `m` element attribute, and get the `murl` attribute from that... All in one line of JavaScript in the console:

```javascript
urls = Array.from(document.querySelectorAll(".iusc")).map(el => JSON.parse(el.attributes.m.value).murl)

<- (35) ["https://someinterestingfacts.net/wp-content/uploads/2016/07/Canadian-Grizzly-Bear.jpg", "https://images.gearjunkie.com/uploads/2015/07/Grizzly-Bear.jpg", "https://www.pbs.org/wnet/nature/files/2018/07/Bear133-1280x720.jpg", "https://upload.wikimedia.org/wikipedia/commons/e/e2/Grizzlybear55.jpg", ... ]
```

Hooray!

Now all we need to do is add the hack to download the list into a CSV text file (really just a text file listing URLs, one per line):

```javascript
urls = Array.from(document.querySelectorAll(".iusc")).map(el => JSON.parse(el.attributes.m.value).murl);
window.open('data:text/csv;charset=utf-8,' + escape(urls.join('\n')));
```

Note: this is where turning off any ad-blocker software in the browser is important. ublock prevented me from downloading or downloaded an empty file until I disabled it.

Next I should make sure that this works if I scroll down a bit to collect more than the default 35 images.

So, to recap, 

1. Open your browser and go here: <https://www.bing.com/images/search?q=grizzly+bear>
2. Press Ctrl-Shift-J to bring up the developer tools console
3. Paste this text in 
```javascript
urls = Array.from(document.querySelectorAll(".iusc")).map(el => JSON.parse(el.attributes.m.value).murl);
window.open('data:text/csv;charset=utf-8,' + escape(urls.join('\n')));
```

Oh my, now that blanks out the Bing image search for a time... That was with Google Chrome. I wonder if using Microsoft Edge, a pretty good browser, works better with Bing... Nope.

Well... Bing Search in general is responding very poorly now. I can only get the default 35 hits, the interface shows a lot of broken images (which don't matter for my purposes, but it's a bad sign). It was working fine yesterday...

It reminds me of when I was in China, and I searched for something considered "problematic" by the Great Firewall, and I was "punished for a few minutes by my Internet connection getting all broken. I may be paranoid. But there's something about the process that makes you paranoid...

For now I'll just push through to get the whole process done with sets of 35 images, and we'll see if Bing works better later, otherwise I may explore other possibilities, sigh...

Update: indeed Bing works much better a day later! I got over 800 image URLs for each type of bear. Perhaps my paranoia was unwarranted, and it was Bing Search that was having a bad day, not me!

The updated sequence to follow is:

1. Open the developer console first
2. Do the search
3. Scroll down to the end of the page, which will load more search results, and keep scrolling until it doesn't go further. You can use the space bar or Page Down key to scroll down.
4. Click the "See more images" button to load more search results, and repeat step 3.
5. Enter the magic Javascript formula in the console to do the download.

## Loading the images into a Jupyter notebook

The method suggested by the book, using the Bing API, does everything "in the cloud".
But using the Image search scraping method, we produce a file using a browser on the local PC with a list of URLs. This file needs to be transferred from the local PC to the cloud-based Notebook somehow.

The fast.ai library has a `download_images()` which requires a list...

 It turns out you can go to the directory view and upload anything you want, so those files, I can just make them accessible that way.

This seems to be what's recommended in the old "How to scrape Google" article cited at the top:

```python
download_images(/path/to/download/file, destination_folder)
```
