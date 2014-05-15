App.EditView = Ember.View.extend({
      didInsertElement : function(){
          this._super();
          console.log(this);
          Ember.run.scheduleOnce('afterRender', this, function(){
              $('#description').summernote({
                  toolbar: [
                      ['style', ['bold', 'italic', 'underline', 'clear']],
                      ['font', ['strike']],
                      ['para', ['ul', 'ol']],
                      ['insert', ['link', 'picture']]
                  ]
              });
              $(".tm-input").tagsManager();
              var genreTags = $("#genres").tagsManager({
                  prefilled: this.controller.get('genres')
              });
              var authorTags = $("#authors").tagsManager({
                  prefilled: this.controller.get('authors')
              });
          });
      }
});

App.UploadView = Ember.View.extend({
      didInsertElement : function(){
          this._super();
          Ember.run.scheduleOnce('afterRender', this, function(){

              var controller = this.controller;

              $(".tm-input").tagsManager();

              window.dropzone = new Dropzone("#upload", {
                  url: "/api/upload/",
                  paramName: "file",
                  clickable: true,
                  previewsContainer: ".previewsContainer",
                  autoProcessQueue: false,
                  maxFiles: 1,
              });

              dropzone.on('addedfile', function(file){

                  file.previewElement = document.getElementsByClassName('previewsContainer')[0];

                  $.getJSON('/api/upload/search/'+file.name.split('.')[0], function (data) {

                      book = data.results.items[0];

                      controller.set('filename', file.name);
                      controller.set('filesize', file.size);
                      controller.set('title', book.volumeInfo.title);
                      controller.set('subtitle', book.volumeInfo.subtitle);

                      var covers = book.volumeInfo.imageLinks;

                      if (covers.extraLarge !== null && covers.extraLarge !== '' && typeof covers.extraLarge !== 'undefined') {
                          controller.set('cover', covers.extraLarge);
                      }
                      else if (covers.large !== null && covers.large !== '' && typeof covers.large !== 'undefined') {
                          controller.set('cover', covers.large);
                      }
                      else if (covers.medium !== null && covers.medium !== '' && typeof covers.medium !== 'undefined') {
                          controller.set('cover', covers.medium);
                      }
                      else if (covers.small !== null && covers.small !== '' && typeof covers.small !== 'undefined') {
                          controller.set('cover', covers.small);
                      }
                      else if (covers.thumbnail !== null && covers.thumbnail !== '' && typeof covers.thumbnail !== 'undefined') {
                          controller.set('cover', covers.thumbnail);
                      }
                      else if (covers.smallThumbnail !== null && covers.smallThumbnail !== '' && typeof covers.smallThumbnail !== 'undefined') {
                          controller.set('cover', covers.smallThumbnail);
                      }

                    var authorTags = $("#authors").tagsManager({
                        prefilled: book.volumeInfo.authors.join(',')
                    });

                    var genreTags = $("#genres").tagsManager({
                        prefilled: []
                    });

                    controller.set('published', book.volumeInfo.publishedDate);
                    controller.set('publisher', book.volumeInfo.publisher);

                    book.volumeInfo.industryIdentifiers.forEach(function(entry){
                        if (entry.type === "ISBN_10") {
                            controller.set('isbn10', entry.identifier);
                        }
                        if (entry.type === "ISBN_13") {
                            controller.set('isbn13', entry.identifier);
                        }
                    });

                    controller.set('description', book.volumeInfo.description);
                 });

             });

             dropzone.on('sending', function(file, xhr, formData) {
                 formData.append('title', controller.get('title'));
                 formData.append('subtitle', controller.get('subtitle'));
                 formData.append('cover', controller.get('cover'));
                 formData.append('description', controller.get('description'));
                 formData.append('isbn-10', controller.get('isbn10'));
                 formData.append('isbn-13', controller.get('isbn13'));
                 formData.append('publisher', controller.get('publisher'));
                 formData.append('date-published', controller.get('published'));
                 formData.append('authors', $("#authors").tagsManager('tags'));
                 formData.append('genres', $("#genres").tagsManager('tags'));
             });

             dropzone.on('success', function(file, response) {
                 console.log(response);
             });
          });
    }
});
