all: libs

libs:

	rm -f master.zip
	rm -rf js-flex-vertical-align-master

	rm -rf alexandria/static/libs
	mkdir alexandria/static/libs

	bower install

	mkdir alexandria/static/libs/jquery-growl

	cp bower_components/growl/javascripts/jquery.growl.js alexandria/static/libs/jquery-growl/.
	cp bower_components/growl/stylesheets/jquery.growl.css alexandria/static/libs/jquery-growl/.
	
	mkdir alexandria/static/libs/mustache

	cp bower_components/mustache/mustache.js alexandria/static/libs/mustache/mustache.js
	
	mkdir alexandria/static/libs/dropzone

	cp bower_components/dropzone/downloads/dropzone.js alexandria/static/libs/dropzone/dropzone.js

	mkdir alexandria/static/libs/jquery

	cp bower_components/jquery/dist/jquery.min.js alexandria/static/libs/jquery/.

	mkdir alexandria/static/libs/foundation
	mkdir alexandria/static/libs/foundation/foundation
	mkdir alexandria/static/libs/foundation/vendor

	cp bower_components/foundation/css/foundation.min.css alexandria/static/libs/foundation/.
	cp bower_components/foundation/css/normalize.css alexandria/static/libs/foundation/.
	
	cp bower_components/foundation/js/foundation.min.js alexandria/static/libs/foundation/.
	cp -r bower_components/foundation/js/foundation alexandria/static/libs/foundation/.

	cp bower_components/fastclick/lib/fastclick.js alexandria/static/libs/foundation/vendor/.
	cp bower_components/jquery.cookie/jquery.cookie.js alexandria/static/libs/foundation/vendor/.
	cp bower_components/modernizr/modernizr.js alexandria/static/libs/foundation/vendor/.
	cp bower_components/jquery-placeholder/jquery.placeholder.js alexandria/static/libs/foundation/vendor/placeholder.js

	curl -OL https://github.com/devmatt/js-flex-vertical-align/archive/master.zip && unzip master.zip

	mkdir alexandria/static/libs/flexverticalcenter

	cp js-flex-vertical-align-master/flexverticalcenter.js alexandria/static/libs/flexverticalcenter/.

	rm -f master.zip
	rm -rf js-flex-vertical-align-master
