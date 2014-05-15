all: libs

libs:

	rm -rf alexandria/static/libs
	mkdir alexandria/static/libs

	bower install

	mkdir alexandria/static/libs/dropzone

	cp bower_components/dropzone/downloads/dropzone.js alexandria/static/libs/dropzone/dropzone.js

	mkdir alexandria/static/libs/jquery

	cp bower_components/jquery/dist/jquery.min.js alexandria/static/libs/jquery/.
