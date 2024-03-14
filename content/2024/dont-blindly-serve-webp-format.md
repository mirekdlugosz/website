Title: Don't blindly serve WebP format
Slug: dont-blindly-serve-webp-format
Date: 2024-03-12 17:57:46
Category: Blog
Tags: planet AST, planet MoT, testing, tutorial

If you have done any webdev work in last few years, you must have heard about WebP. It's an image format that promises up to 34% smaller file sizes without noticeable quality downgrade. It's pretty much universally supported since late 2020.

With smaller file sizes and widespread support, you might think it's a good idea to just serve all your images in WebP. Or, if you want to be extra backward-compatible - serve WebP to all browsers that claim to support it, and original image to remaining few.

I also thought it's a good idea, and made a switch on this very website. I'm creating WebP with a compression factor set to 80. And then I noticed that one file is actually larger after conversion.

Following this thread, I compared size of all WebP images with their original counterparts. Turned out WebP produced larger files in 3% (4 out of 117). In worst case, 20 kB PNG file turned into 122 kB WebP - over sixfold increase in size!

Since then, when I generate WebP, I compare file size to original and keep it only if new format produces smaller file. This way browsers will always receive the smallest file I can produce, regardless of the format.

I guess the main takeaway here is ages old "measure before optimizing".
