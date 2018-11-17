Title: The map of bakeries that sell genuine St. Martin Croissants
Slug: the-map-of-bakeries-that-sell-genuine-st-martin-croissants
Date: 2015-11-11 20:51:25
Category: Blog
Tags: tutorial, web scraping, R

97 years ago Poland regained independence after being partitioned for well over a century. The date coincidences with St. Martin Day, a holiday with pagan roots that somehow managed to be more important here in [Poznań](https://en.wikipedia.org/wiki/Pozna%C5%84). We celebrate by having a parade on one of main streets and eating ungodly amounts of *rogal świętomarciński* (St. Martin Croissant), a local cake with PGI status in European Union. In this blog post I will show how to plot locations of bakeries that are allowed to sell products with that name.
<!-- more -->

## Background

In 2008, *rogal świętomarciński* gained protected geographical indication (PGI) in European Union. This means that all products sold under that name must meet certain criteria (composition, creation procedure, place of origin etc.). Local *Cech Cukierników i Piekarzy w Poznaniu* (Poznań Guild of Pastry Chefs and Bakers) verifies if cakes on market do meet these criteria. They also manage [a list of bakeries allowed to sell products under "St. Martin Croissant" name](http://cechcukiernikowipiekarzy.pl/lista-cukierni-z-certyfikatem.html). Some people say it protects customers, as it gives objective way of ensuring that whatever they are buying does have certain quality. Other people say it supports oligopoly and hinders competition, as one collective has final word in saying who can and who can't use protected product name. Either way, it's probably a good idea to know where genuine croissants are made - and this is what we will do.

## Getting the data

As in every analysis, the first step is obtaining the data. List of bakeries on Guild website provides names and addresses in convenient tabular form, what makes it a good starting point.

Thanks to `rvest` package, that list can be downloaded, extracted and converted into `data.frame` in just few lines of code. Usually I prefer to perform web scraping tasks with `xml2` package, because it allows for finer control, but that would be an overkill in this case.

	#!r
	library('rvest')
	
    page.url <- 'http://cechcukiernikowipiekarzy.pl/lista-cukierni-z-certyfikatem.html'
    page.content <- read_html(page.url)
    bakeries <- html_node(page.content, 'table') %>% 
      html_table(header=TRUE, fill=TRUE)


### Cleaning it up

Unfortunately, our `data.frame` is not exactly the same as table on website. Instead of 103 rows, we've got 113, and instead of 3 columns, we've got… 11?

That's because Guild website contains nested tables, and they cause a bit of trouble for `rvest`. When such structure is supplied to `html_table` function, it might not be able to return `data.frame` with both correct dimensions and all the data. By default, preserving dimensions is deemed more important; users who prefer to retrieve as much data as possible may supply `fill=TRUE` argument and deal with untidy data on their own.

Since we are walking down a second path, now it's time to clean up the data. We could use some clever custom algorithm for that, but dataset is rather small and only few rows are wrong, so I guess that manual corrections are good enough.

    #!r
    wrong.rows <- c(97,98, 100,101, 103,104, 108:111)
    bakeries[wrong.rows-1, 3] <- bakeries[wrong.rows-1, 4]
    bakeries[107, 3] <- bakeries[107, 7]
    
    bakeries <- bakeries[-1*wrong.rows, c(2,3)]

On side note: if you happen to wonder why they decided to use nested tables in the most straightforward table ever, the answer is that they didn't. But they did use Microsoft Office to generate HTML. 

### Adding coordinates

Now that we have reproduced website's table in R, it's time to translate addresses into geographical coordinates.

This is made trivial by `geocode` function in `ggmap` package. To obtain `data.frame` with longitude and latitude values, all we need to do is call ``geocode(bakeries$`Miejsce produkcji`)``.

Of course `geocode` can't get addresses' coordinates out of thin air - it uses web service for that. By default it queries 
[Data Science Toolkit](http://www.datasciencetoolkit.org/), but Google Maps API is supported as well.
There are many reasons to use Data Science Toolkit (including openness), and there are many reasons to avoid Google Maps (including privacy concerns). But they hardly matter when faced with much higher quality results that Google produces. In this example, Data Science Toolkit failed to get coordinates of seven addresses and missed another ten by some 7000 kilometers (4000 miles). On the other hand, Google Maps API failed in just four cases - and they all share one root cause that can be corrected by small adjustments to source data.

And since we will be using Google Maps in next step anyway, there are hardly any reasons to avoid Google Maps API right now.

    #!r
    library('ggmap')
    
    bakeries[78,2] <- sub("Wlkp.", "Wielkopolska", bakeries[78,2], fixed = TRUE)
    bakeries[,2] <- sub("Wlkp.", "Wielkopolski", bakeries[,2], fixed = TRUE)
    coordinates <- geocode(bakeries[,2], source = "google")
    bakeries <- cbind(bakeries, coordinates)

## Plotting data

At this point we have everything that we need to create bakeries map. While `ggmap` could be used to produce it in raster image format, it will require us to go through few iterations of image rendering just to grasp the data and decide what features are worth highlighting. Something a bit more dynamic, something that allows user to zoom, pan and click to learn more about selected locations, would be much better suited for data exploration purposes.

And creating that something is extremely easy thanks to [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/), which solves all hard problems for us. We only really need basic HTML page, few lines of JavaScript to create map markers and data to plot.

We already have the last piece of puzzle, but only in R. We need to export it to a format that can be effortlessly handled by JavaScript, and that is long way of saying JSON. This is another task made easy by one of many packages in extensive R library.

    #!r
    library('rjson')
    writeLines(toJSON(bakeries), "./bakeries.json")

Handling JSON in JavaScript might be easy, but actually loading it is not. For security reasons, web browsers don't provide API to read local files content and it seems that the only way to fetch remote ones are asynchronous HTTP requests. Unfortunately, standard JavaScript library that handles these is quite low level and forces us to deal with success codes, failed requests and possible timeouts. We can take that weight off our shoulders by using third-party library, but again, that will probably mean loading quite a lot of completely unwanted code.

Either way, when we finish loading the data, we have to loop over all items in JSON array. For each row we want to create new marker at given coordinates and attach function that will create new pop-up window with bakery details as reaction to click event.

    #!javascript
    $.getJSON("bakeries.json", function(data){
    	items = data.Wnioskodawca.length;
    	for (var i=0; i < items; i++) {
    		var marker = new google.maps.Marker({
    			position: new google.maps.LatLng(data.lat[i], data.lon[i]),
    			title: data.Wnioskodawca[i],
    			map: map,
    			icon: 'rogal.png'
    		});
    
    		google.maps.event.addListener(marker, 'click', (function(marker, i) {
    			return function() {
    				infowindow.setContent(''.concat(
    							'<div id="content"><h2>', data.Wnioskodawca[i], '</h2>',
    							'<p><b>Address</b>: ', data["Miejsce produkcji"][i],
    							'</div>'
    						));
    				infowindow.open(map, marker);
    			}
    		})(marker, i));
    		Gmarkers.push(marker);
    	}
    })

Finally, we have to create skeleton HTML and JavaScript code. If I were to include them in snippet of code, I would pretty much had to paste the entire page. If you want to see that part, go ahead and look at source of [map I have prepared]({static}bakeries-map/index.htm).

## Closing words

In this blog post we have seen how to download data from website into R, use it to obtain coordinates of addresses and export data into JSON. Finally, we have used JavaScript to create dynamic map that can be used for data exploration. That last part was greatly inspired by [Fabio Veronesi](http://r-video-tutorial.blogspot.com/)'s preceding [work](http://r-video-tutorial.blogspot.com/2015/05/live-earthquake-map-with-shiny-and.html) that has not been mentioned before.

Both [R code]({static}bakeries-map/transform-data.R) and [the final product (map)]({static}bakeries-map/index.htm) are available for curious.
