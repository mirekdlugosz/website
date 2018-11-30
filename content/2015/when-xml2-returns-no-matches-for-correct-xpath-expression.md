Title: When xml2 returns "No matches" for obviously correct XPath expression
Slug: when-xml2-returns-no-matches-for-correct-xpath-expression
Tags: R
Category: Blog
Date: 2015-10-06 22:22:04

The other day I was trying to fetch some data from XML file using R package `xml2`, but `xml_find_one` function kept returning `Error: No matches`. Here's what was wrong, why it was wrong and how to fix it.

<!-- more -->

## The problem

The code I started with could have looked something like that:

	#!r
    library("xml2")
    
    xml <- read_xml("https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/5182108/XML/?response_type=display")
    node <- xml_find_one(xml, '/Record/Section/TOCHeading[text()="Names and Identifiers"]/..')

Saving it in file and then `source`ing it left me with following error message:

    Error in eval(expr, envir, enclos) : No matches

I proceeded with running it line-by-line in R console to track down the source of error. Sure enough, the last line was to blame. Provided XPath expression is not overly complex, but still leaves some room for mistakes and typos, so I started to tackle down the issue by simplifying it. After few tries I was left with the simplest expression ever - `xml_find_one(xml, '//Record')` - but the error just didn't want to go away.

## The source

After an hour of trial and error, reading the documentation cover to cover back and forth and searching the web, I have finally identified the root cause of the issue - XML namespaces.

As it turns out, when namespaces are present in XML document, `xml2` expects user to do two things:

- provide namespaces definition in all calls of `xml_find_*`;
- specify namespace of each element present in XPath expression, including **elements living in default namespace**.

This crucial information is hidden in plain sight in [package documentation](https://cran.r-project.org/web/packages/xml2/xml2.pdf). When `xml_find_*` functions are discussed, the final argument is described in following way (emphasis mine):

> Optionally, a named vector giving prefix-url pairs, as produced by xml_ns. If provided, all names will be explicitly qualified with the ns prefix, i.e. if the element bar is defined in namespace `foo`, it will be called `foo:bar`. (And similarly for atttributes). **Default namespaces must be given an explicit name**.

Default namespaces (these without identifiers) are given arbitrary names `d1`, `d2`, … `dn`.

On the side note, R package `XML` works in exactly the same way, which leads me to believe that these requirements are actually imposed by `libxml2`, C library underlying both of them.

## The solution

Problem can be solved by satisfying expectations of `xml2`, i.e. by providing both namespace prefixes for all elements in expression and namespaces definition in function call:

    #!r
    xml_find_one(xml, '/d1:Record/d1:Section/d1:TOCHeading[text()="Names and Identifiers"]/..', xml_ns(xml))

    {xml_node}
    <Section>
    [1] <TOCHeading>Names and Identifiers</TOCHeading>
    [2] <Description>Information describing the identity of this PubChem Compound recor ...
    [3] <Section>\n      <TOCHeading>Record Title</TOCHeading>\n      <Description>Text ...
    [4] <Section>\n      <TOCHeading>Computed Descriptors</TOCHeading>\n      <Descript ...
    [5] <Section>\n      <TOCHeading>Synonyms</TOCHeading>\n      <Description>Alternat ...
    [6] <Section>\n      <TOCHeading>Create Date</TOCHeading>\n      <Description>Date  ...
    [7] <Section>\n      <TOCHeading>Modify Date</TOCHeading>\n      <Description>Date  ...

Of course if you are going to call `xml_find_*` functions repeatedly, calling `xml_ns()` each time will come with performance penalty. Since that function returns named character vector, it's good idea to call it once and store result in separate variable.
