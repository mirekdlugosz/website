Title: Found on web: Radiologist are testers, too
Slug: found-on-web-radiologist-are-testers-too
Date: 2018-02-25 15:14:28
Category: Blog
Tags: found on web, testing

Luke Oakden-Rayner, PhD candidate in field of radiology, explains why certain X-ray images database is not really fit to task of training medical systems to do diagnostics. His observations apply to pretty much any dataset used to train machines.

<!-- more -->

Read [*Exploring the ChestXray14 dataset: problems* by Luke Oakden-Rayner](
https://lukeoakdenrayner.wordpress.com/2017/12/18/the-chestxray14-dataset-problems/).

It's worth your time for few reasons:

* He clearly demonstrates that quality of automated predictions is based solely on quality of input data; how they sometimes call it: garbage in, garbage out.
* He stresses out that automated diagnostic systems are only as good as they are useful in the context of established medical practice; but since they cannot learn medical practice and meaning behind text labels, there is danger of spending considerable resources on creating something that is not particularly useful, or, even worse, is actively harmful.
* He shows that reducing complex, multidimensional reality to single performance metric might lead to erroneous conclusions.

However, I wanted to highlight one quote:

> Radiology reports are not objective, factual descriptions of images. The goal of a radiology report is to provide useful, actionable information to their referrer, usually another doctor. In some ways, the radiologist is guessing what information the referrer wants, and culling the information that will be irrelevant.

Isn't this exactly what good testers do, too?
