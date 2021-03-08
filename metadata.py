#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

PROJECTS = [
    # First one is intentionally left blank as template
    {
        'name': '',
        'href': '',
        'imagetitle': '',
        'tags': [],
        'description': """
        """,
        'starred': False,
    },
    {
        'name': 'createPokémon.team',
        'href': 'https://createpokemon.team/',
        'imagetitle': 'createpokemonteam',
        'tags': ['Python', 'Angular', 'TypeScript', 'SCSS'],
        'description': """
            Web application that helps you build your own Pokémon team in any core series game.
            <a href="https://github.com/mirekdlugosz/create-pokemon-team">GitHub</a>.
        """,
        'starred': False,
    },
    {
        'name': 'Pelican Social Cards plugin',
        'href': 'https://github.com/mirekdlugosz/pelican-social-cards',
        'imagetitle': 'pelican-social-cards',
        'tags': ['Python', 'Pillow', 'pytest'],
        'description': """
            <a href="https://blog.getpelican.com/">Pelican</a> plugin that generates images to make your posts more visually appealing on social media.
            <a href="https://github.com/mirekdlugosz/pelican-social-cards">GitHub</a>.
        """,
        'starred': True,
    },
    {
        'name': 'Pelican Metadata Generator',
        'href': 'https://github.com/mirekdlugosz/pelican-metadata-generator',
        'imagetitle': 'pelican',
        'tags': ['Python', 'PyQt 5', 'unittest', 'Markdown'],
        'description': """
            Graphical application to create <a href="https://blog.getpelican.com/">Pelican</a> post metadata.
            <a href="https://github.com/mirekdlugosz/pelican-metadata-generator">GitHub</a>.
        """,
        'starred': False,
    },
    {
        'name': 'Airgun',
        'href': 'https://github.com/SatelliteQE/airgun',
        'imagetitle': 'airgun',
        'tags': ['Python', 'Selenium', 'XPath'],
        'description': """
            Framework to interact with
            <a href="https://www.redhat.com/en/technologies/management/satellite">Red Hat Satellite</a>,
            supporting automated web UI checks created by Satellite QE team.
            I was maintaining it from June 2019 to June 2020.
            <a href="https://github.com/SatelliteQE/airgun">GitHub</a>.
        """,
        'starred': True,
    },
    {
        'name': 'Civic engagement in Europe',
        'href': 'https://mzalewski.shinyapps.io/ESS-civic-engagement',
        'imagetitle': 'ess',
        'tags': ['R', 'ggplot2', 'Shiny (HTML, CSS)', 'data wrangling', 'visualisation'],
        'description': """
            R Shiny application to explore changes in civic engagement index in various European countries over time.
            <a href="https://github.com/mirekdlugosz/ESS-civic-engagement">GitHub</a>.
        """,
        'starred': False,
    },
    {
        'name': 'ansible-dotfiles',
        'href': 'https://github.com/mirekdlugosz/ansible-dotfiles',
        'imagetitle': 'ansible',
        'tags': ['Ansible'],
        'description': """
            Ansible playbook to deploy some of my configuration files and install utilities that are rarely packaged by distributions.
            <a href="https://github.com/mirekdlugosz/ansible-dotfiles">GitHub</a>.
        """,
        'starred': False,
    },
    {
        'name': 'My blog',
        'href': '/blog/',
        'imagetitle': 'blog',
        'tags': ['Pelican', 'Jinja2 (HTML, SCSS)', 'writing'],
        'description': """
            My current blog, focused mainly on testing and tech.
            <a href="https://github.com/mirekdlugosz/website">GitHub</a>.
        """,
        'starred': False,
    },
    {
        'name': 'Przepis na LibreOffice',
        'href': 'http://przepis-na-lo.pl/',
        'imagetitle': 'przepis-na-lo',
        'tags': ['Wordpress', 'PHP', 'HTML', 'CSS', 'writing'],
        'description': """
            My discontinued blog focused on <a href="https://libreoffice.org/">LibreOffice</a> tips and tricks. It was relatively popular in Polish open source and academic communities, attracting about 20&nbsp;000 unique visitors in peak months.
        """,
        'starred': False,
    },
    {
        'name': 'A Fistful of Links website',
        'href': 'https://afistfuloflinks.github.io/',
        'imagetitle': 'afol',
        'tags': ['Hugo', 'Github Actions', 'Python'],
        'description': """
            I prepared most of new website, based on <a href="https://gohugo.io/">Hugo</a>,
            and created automatic build system in Github Actions.
            I also ported historical content from intranet site.
            <a href="https://github.com/AFistfulOfLinks/afistfuloflinks">GitHub</a>.
        """,
        'starred': False,
    },
]
