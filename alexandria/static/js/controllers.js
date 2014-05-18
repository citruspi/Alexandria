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
            }).then(function(){
                $('#feedback').hide();
                $('#feedback').html('Your account was successfully registerd.');
                $('#feedback').removeClass();
                $('#feedback').addClass('alert');
                $('#feedback').addClass('alert-success');
                $('#feedback').show();
            }, function(){
                $('#feedback').hide();
                $('#feedback').html('There was problem registering your account.');
                $('#feedback').removeClass();
                $('#feedback').addClass('alert');
                $('#feedback').addClass('alert-danger');
                $('#feedback').show();
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
