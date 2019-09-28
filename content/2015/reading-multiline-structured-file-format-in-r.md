Title: Reading multiline structured file format in R
Slug: reading-multiline-structured-file-format-in-r
Date: 2015-10-21 22:14:35
Category: Blog
Tags: R

Reddit user [alignedletters](https://www.reddit.com/user/alignedletters) [asked how to read data stored in custom format into Microsoft Excel](https://www.reddit.com/r/excel/comments/3j924x/importing_txt_files_to_excel_in_a_specific/). The problem was twofold - each record was represented by two lines, there was no clear delimiter between fields and one of issues mentioned so far is actually more complicated than that. In this post, I show how that data can be read in R.

<!-- more -->

Example data file was uploaded by /u/alignedletters to [pastebin.ca](http://www.pastebin.ca/3147596); you can also find a copy on 
[BitBucket](https://bitbucket.org/mirzal/scrapbook/src/master/structured-multiline-data/sample-data.txt) and [GitHub](https://github.com/mirekdlugosz/scrapbook/blob/master/structured-multiline-data/sample-data.txt). I will refer to that file as `sample-data.txt` from now on.

Let's start by skimming over its content. Header at the top of file informs us that there are seven columns. Two of them are put inside parentheses, and one pair of fields is delimited by single dash. Reading actual records reveals that three fields are put in first line, while remaining four fields are placed below, in line indented by tab and six spaces. Before reaching 30th record we should have also noticed that missing values in second field are indicated by double dash. There is some cruft at beginning and end of file, as well as after every 10 records. 

To sum up, every record was split into two lines, but other than that, file format seems to be structured and easy to parse.

Let's start by reading file content into R. `readLines()` function can do that.

    #!r
	singles_file <- readLines("./sample-data.txt")

Character vector requires some cleaning, but we can take care of that later. First, let's try to parse single record. Since we will be doing that repeatedly, it makes sense to put relevant code inside function. It will take two lines from file as input and will return vector of field values.

First line is easy to parse, as fields are delimited by three spaces (if you see four spaces anywhere, that's because second field is space-padded number). We can use `strsplit()` to turn string into vector. That function returns list of vectors even if argument has only one element, so we will pass result through `unlist()` to reduce it back into simple vector.

Second line lacks common delimiter, although it does follow certain pattern. It starts with artist name that goes up to second-to-last opening bracket (not [first one](https://en.wikipedia.org/wiki/Was_(Not_Was))). Then there is label name inside parentheses. It is followed by single dash and number that represents number of weeks on chart. Finally, there is another number (peak position) inside parentheses. The entire pattern can be matched with following regular expression: `\s*(.*) \((.*)\)-([0-9]+) \(([0-9]+)\)`.

    #!r
    parse_record <- function(x) {
      first <- unlist(strsplit(x[1], "\\s{2,}"))
      second <- str_match(x[2],
                          paste0("\\s*(.*)",
                                 " \\((.*)\\)-([0-9]+)",
                                 " \\(([0-9]+)\\)"))[,-1]
      return(c(first, second))
    }

Regular expression was split into multiple lines for readability; `paste0` is required to join it back into single string. Function `str_match` comes from [stringr](https://cran.r-project.org/web/packages/stringr/) package and is used because base R does not provide simple interface for extracting grouped matches from string.

Our function is not prepared to handle data that falls outside of specified format, so it's time to clean up `singles_file`. I decided to use `grep()` to find boundaries of data inside lines vector and `grepl()` to identify decorations that were put every ten records. One drawback of that solution is hardcoded number of lines to skip after opening boundary and before closing one.

	#!r
    file_from <- grep("^TW", singles_file) + 2
    file_to <- grep("UNDER THE HOT 100", singles_file) - 2
    
    singles_file <- singles_file[file_from:file_to]
    delimiters <- grepl("------", singles_file, fixed = TRUE)
    singles_file <- singles_file[! delimiters]

Now we are ready to extract individual records from vector of lines and run our function on all of them. Since every record is exactly two lines long, the extraction part can be reduced to splitting `singles_file` into chunks of equal length.

	#!r
    parsed <- sapply(split(singles_file, ceiling(seq_along(singles_file)/2)),
                     parse_record)
    singles <- do.call("rbind", parsed)

<!-- force separation of code blocks -->

    :::text
    Warning message:
    In rbind(`1` = c("1", "1", "TOTAL ECLIPSE OF THE HEART", NA, NA, :
      number of columns of result is not a multiple of vector length (arg 83)

Hmph. That warning message is not exactly what we expected. If we look at `singles` data frame, we will see that there are multiple `NA`s in rows between 82 and 89; plus, the first row has only three fields. Let's go back to source file and see what is wrong.

Records number 82 and 87 are at fault - they span three lines instead of two. To complicate things further, they don't share the same format. The field that spans two lines is song title in one case and artist name in another. Either way, we have to teach our parsing function how to handle that.

We can transform longer records into two-line format we have already dealt with by joining some lines together. The problem is at deciding **which lines**. One detail I have noticed is: part of song name moved into separate line begins with tab and five spaces, while lines with artist name are indented by one space more. Unfortunately we have only two data points to work with and it's impossible to tell whether that difference is part of file format specification or not.

Code below looks up for lines resembling continuation of song title and concatenate them with first line; all remaining lines are joined together as well. Whitespace characters are removed to avoid gaps inside field values.

	#!r
    if (length(x) > 2) {
      begin <- grepl("^\\t\\s{5}\\S", x)
      begin[1] <- TRUE
      x <- gsub("^\\s+|\\s+$", "", x)
      x <- c(
        paste(x[begin], collapse = " "),
        paste(x[!begin], collapse = " ")
      )
    }

As for fields missing in first record, the issue is caused by additional commentary between sixth and seventh field. We can match it with catch-all regexp `.*`.

    #!r
    parse_record <- function(x) {
      if (length(x) > 2) {
        begin <- grepl("^\\t\\s{5}\\S", x)
        begin[1] <- TRUE
        x <- gsub("^\\s+|\\s+$", "", x)
        x <- c(
          paste(x[begin], collapse = " "),
          paste(x[!begin], collapse = " ")
        )
      }
      first <- unlist(strsplit(x[1], "\\s{2,}"))
      second <- str_match(x[2],
                          paste0("\\s*(.*)",
                                 " \\((.*)\\)-([0-9]+)",
                                 ".*",
                                 " \\(([0-9]+)\\)"))[,-1]
      return(c(first, second))
    }

After fixing `parse_record()` function, we have to revise a way we extract records from file content vector. My approach assumes that every record begins with (space-padded) number and takes advantage of R implicit type conversion.

    #!r
    parsed <- sapply(split(singles_file, 
                           cumsum(grepl("^\\s?[0-9]", singles_file))),
                     parse_record)
    singles <- data.frame(t(parsed), stringsAsFactors = FALSE)

This time R did not produce any warnings and the final data frame looks about right.

The only thing that's left to do is converting few columns from characters into numbers and assigning meaningful names to columns.

Final version of code can be found on [BitBucket](https://bitbucket.org/mirzal/scrapbook/src/master/structured-multiline-data/import.R) 
and [GitHub](https://github.com/mirekdlugosz/scrapbook/blob/master/structured-multiline-data/import.R). Another file in that directory shows alternate, regular expression oriented solution that you might find interesting. That approach was implemented in Python, although it would look almost the same in any other programming language.

**Takeaway lesson**: don't be that guy. If you are going to publish some data, use format for which there are libraries in programming languages popular at the moment. When in doubt, use CSV for tables and JSON/XML for all other structures.
