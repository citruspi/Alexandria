App.SettingsController = Ember.Controller.extend({
    save: function() {
        $.post('/api/settings/', {
            realname: this.get('realname'),
            emailadd: this.get('emailadd'),
            password: this.get('password')
        }).then(function(){
            $('#failure').hide();
            $('#success').show();
        }, function(){
            $('#success').hide();
            $('#failure').show();
        });
    }
});

App.EditController = Ember.Controller.extend({
    actions: {
        save: function(){
            id = location.href.split("/").slice(-1);
            controller = this;
            $.post('/api/book/'+id, {
                title: this.get('title'),
                subtitle: this.get('subtitle'),
                cover: this.get('cover'),
                description:  this.get('description'),
                authors: function() {
                    return $("#authors").tagsManager('tags');
                },
                genres: function(){
                    return $("#genres").tagsManager('tags');
                }
            }).then(function(response){
                controller.set('negativeResponse', null);
                controller.set('positiveResponse', 'Your edit was successfully saved.');
            }, function(response){
                controller.set('positiveResponse', null);
                controller.set('negativeResponse', 'There was a problem saving your edit.');
            });
        }
    }
});

App.UploadController = Ember.Controller.extend({
    actions: {
        save: function(){
            window.dropzone.processQueue();
        }
    }
});
