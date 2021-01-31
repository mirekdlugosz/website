Title: Why I love Pokémon
Slug: why-i-love-pokemon
Date: 2018-07-01 20:39:49
Category: Blog
Tags: personal, JavaScript, projects

This is software release announcement disguised as impressions on pop culture phenomena.

<!-- more -->

I discovered Pokémon when I was a kid, back around year 2000. I watched every episode of anime that was on TV with almost religious commitment. I bought a lot of cards and I played with my friends and neighbours. I read every single article in kids magazine I could find. I saved my pocket money for months to buy Game Boy and Pokémon game (I wanted Red or Blue, but they only had Silver in the store). I vividly remember in-game clock going over 99 hours mark.

I think it's fair to say that I was a huge fan. But eventually Pokémon craze died out and I moved on to other things.

I re-discovered Pokémon in 2015. I was on strong medicines then and I needed something that would keep me occupied without requiring my full attention. After some discussions with my girlfriend, we decided to buy 3DS with Pokémon Y. 

That game was great. Beautiful 3D graphics. Few hundred unknown creatures (remember, I was familiar only with first 150 Pokémon and some from generation II). Unique Pokémon catch list in almost every route, giving impression of almost real-life ecosystem. Pokémon Amie that allowed us to create real, even if extremely shallow, relationships with our Pokémon. Surprisingly deep and complex battle and team building mechanics. Global Trade System, where I could trade Pokemon for the first time in my life. What was supposed to be innocent distraction at harder times turned out to be extremely engaging and fun experience that took embarrassingly huge amount of my time.

Around mid-2015 I started toying with idea of Pokémon team builder application. I wanted to have one team that could defeat any trainer. Back then I still wanted to enter data science market and was using R extensively, so I decided to try and code something in that language. I chose Shiny for UI - not because I wanted to publish my work, but because it was easy way of creating graphical UIs in R.

That version was extremely simple - you could choose six Pokémon and **type** (not actual name) of four attacks for each of them. Below the form, there was bare-bones table filled with cryptic numbers. There was no data validation (you could choose type of move that given Pokémon couldn't use at all). There was no way of mapping type with particular move that Pokémon knew. Moves that didn't do any damage had to be omitted. There was no way to preserve team across sessions - form had to be filled after each restart of app. It was low-quality software that provided huge value.

{% gallery
    {attach}why-i-love-pokemon/shiny_1.png | caption=R Shiny app - team builder form
    {attach}why-i-love-pokemon/shiny_2.png | caption=R Shiny app - team details
    {attach}why-i-love-pokemon/shiny_3.png | caption=R Shiny app - team overview
%}

Fast forward to December 2016, I was expecting to switch teams inside my company and become responsible for writing automated tests in Protractor (pardon my French, that was before I discovered Bach and Bolton who taught me that testing can't be automated). I didn't have any experience with Protractor and was eager to get some fast. Pokémon Moon was still fresh on my mind, so I added pieces together again and decided it's time to rewrite my old Pokémon team builder Shiny app in AngularJS.

After few weeks I had *something*. The basic idea was the same - you select six Pokémon and their moves (by name or type!) and get table with cryptic numbers in return. But non-damaging moves were ignored, team definition was stored in URL (as base64-encoded JSON object...) and it run in real browser! Sure, it was readable only on computers, entire frontend was unmaintainable mess in single JavaScript file and I never wrote these Protractor checks, but it was so much better.

{% gallery
    {attach}why-i-love-pokemon/angular_1.png | caption=AngularJS app - team builder form
    {attach}why-i-love-pokemon/angular_2.png | caption=AngularJS app - team details
    {attach}why-i-love-pokemon/angular_3.png | caption=AngularJS app - team overview
%}

This project and potential of what it could become was lingering on my mind more or less constantly since then. I had so many ideas on how it could be improved. Support all core Pokémon games. Work on mobile devices. *Look nice*. Keep team definition in URL in readable format. Use Angular (not to be confused with AngularJS). I wanted to finish it before job hunting. I wanted to finish it before Ultra Sun and Ultra Moon release. I wanted to finish it before returning to Poland.

And I finally did finish it today.

Head on to [createPokémon.team](https://createpokemon.team/) to see the results of couple of months of my work. There are still some things that could be implemented or improved, but overall I feel happy and proud of what I have achieved. You can find source code on [Github](https://github.com/mirekdlugosz/create-pokemon-team/); there is also ever-growing [list of known issues and improvement ideas](https://github.com/mirekdlugosz/create-pokemon-team/issues). Feel free to poke around the code, comment on issues and send a PR or two!

And that's why I love Pokémon. They inspire me to learn, create and share with others.
