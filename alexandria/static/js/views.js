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
