App.MenuController = Ember.Controller.extend({
    actions: {
        logout: function() {
            window.user.set('token', null);
            $.cookie('token', null);
            this.transitionTo('portal');
        }
    }
})

App.SettingsController = Ember.Controller.extend({
    actions: {
        save: function() {
            $.post('/api/settings/', {
                realname: this.get('realname'),
                emailadd: this.get('emailadd'),
                password: this.get('password'),
                token: window.user.get('token')
            }).then(function(){
                $('#failure').hide();
                $('#success').show();
            }, function(){
                $('#success').hide();
                $('#failure').show();
            });
        }
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
                },
                token: window.user.get('token')
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

App.PortalController = Ember.Controller.extend({
    actions: {
        login: function() {
            self = this;
            $.post('/api/portal/login/', {
                username: this.get('l_username'),
                password: this.get('l_password')
            }).then(function(response){
                window.user.set('token', response.token);
                $.cookie('token', response.token);
                var previousTransition = self.get('previousTransition');
                if (previousTransition) {
                    self.set('previousTransition', null);
                    previousTransition.retry();
                } else {
                    // Default back to homepage
                    self.transitionToRoute('index');
                }
            }, function(response){
                controller.set('positiveResponse', null);
                controller.set('negativeResponse', response.responseJSON.error);
            });
        },
        register: function() {
            controller = this;
            $.post('/api/portal/register/', {
                realname: this.get('n_realname'),
                username: this.get('n_username'),
                emailadd: this.get('n_emailadd'),
                password: this.get('n_password')
            }).then(function(response){
                controller.set('negativeResponse', null);
                controller.set('positiveResponse', response.success);
            }, function(response){
                controller.set('positiveResponse', null);
                controller.set('negativeResponse', response.responseJSON.error);
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
