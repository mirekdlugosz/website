help:
	@echo 'Deprecated Makefile for a pelican Web site                                '
	@echo '                                                                          '
	@echo '           !!!!! This file is deprecated. Use "inv" instead !!!!!         '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make clean                          remove the generated files         '
	@echo '   make theme                          (re)generate theme                 '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make devserver [PORT=8000]          serve and regenerate together      '
	@echo '   make publish                        generate using production settings '
	@echo '   make ssh_upload                     upload the web site via SSH        '
	@echo '   make rsync_upload                   upload the web site via rsync+ssh  '
	@echo '   make clean-thumbnails               remove existing thumbnails         '
	@echo '   make thumbnails                     generate missing thumbnails        '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo '                                                                          '

clean:
	inv clean

thumbnails:
	inv thumbnails

theme:
	inv theme

html:
	inv html

serve:
	inv serve

devserver:
	inv devserver

publish:
	inv publish

rsync_upload: publish postpublish
	inv rsync-upload
