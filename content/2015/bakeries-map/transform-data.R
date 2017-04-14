library('rvest')

page.url <- 'http://cechcukiernikowipiekarzy.pl/lista-cukierni-z-certyfikatem.html'
page.content <- read_html(page.url)
bakeries <- html_node(page.content, 'table') %>% 
  html_table(header=TRUE, fill=TRUE)

wrong.rows <- c(97,98, 100,101, 103,104, 108:111)
bakeries[wrong.rows-1, 3] <- bakeries[wrong.rows-1, 4]
bakeries[107, 3] <- bakeries[107, 7]

bakeries <- bakeries[-1*wrong.rows, c(2,3)]

library('ggmap')

bakeries[78,2] <- sub("Wlkp.", "Wielkopolska", bakeries[78,2], fixed = TRUE)
bakeries[,2] <- sub("Wlkp.", "Wielkopolski", bakeries[,2], fixed = TRUE)
coordinates <- geocode(bakeries[,2], source="google")
bakeries <- cbind(bakeries, coordinates)

library('rjson')
writeLines(toJSON(bakeries), "./bakeries.json")