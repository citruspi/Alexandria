App.AuthenticatedRoute = Ember.Route.extend({
    beforeModel: function (transition) {
        if (!window.user.get('token')){
            var loginController = this.controllerFor('portal');
            loginController.set('previousTransition', transition);
            this.transitionTo('portal');
        }
    },
    events: {
        error: function(reason, transition){
            if (reason.status === 403) {
                var loginController = this.controllerFor('portal');
                loginController.set('previousTransition', transition);
                this.transitionTo('portal');
            }
        }
    }
});

App.IndexRoute = Ember.Route.extend({
    beforeModel: function() {
        this.transitionTo('library');
    }
});

App.BookRoute = App.AuthenticatedRoute.extend({
    model: function(params) {
        return Ember.$.getJSON('/api/book/'+params.book_id, {token:window.user.get('token')}).then(function(data){
            console.log(data.book);
            return data.book;
        });
    }
});

App.PortalRoute = Ember.Route.extend({
    beforeModel: function(transition){
        if (window.user.get('token')){
            this.transitionTo('library');
        }
    }
})

App.EditRoute = App.AuthenticatedRoute.extend({
    model: function(params) {
        return Ember.$.getJSON('/api/book/'+params.book_id, {token:window.user.get('token')}).then(function(data){
            return data.book;
        });
    },
    setupController: function(controller, model) {
        controller.setProperties({
            id: model.id,
            title: model.title,
            subtitle: model.subtitle,
            authors: model.authors.join(','),
            description: model.description,
            cover: model.cover,
            genres: model.genres,
            positiveResponse: null,
            negativeResponse: null
        });
    }
});

App.LibraryRoute = App.AuthenticatedRoute.extend({
    model: function(){
        return $.getJSON('/api/books/', {token:window.user.get('token')}).then(function(data) {
            var chunks = [];

            while (data.books.length > 0) {
                chunks.push(data.books.splice(0,6))
            }

            return chunks;
        });
    }
});

App.SettingsRoute = App.AuthenticatedRoute.extend({
    model: function(){
        return Ember.$.getJSON('/api/settings/', {token:window.user.get('token')}).then(function(data) {
            return data.settings;
            console.log(data);
        });
    },
    setupController: function(controller, model) {
        controller.set('realname', model.realname);
        controller.set('emailadd', model.email_address);
    }
});

App.AuthorRoute = App.AuthenticatedRoute.extend({
    model: function(params){
        return Ember.$.getJSON('/api/books/author/'+params.author_id, {token:window.user.get('token')}).then(function(data) {
            var chunks = [];

            while (data.books.length > 0) {
                chunks.push(data.books.splice(0,6))
            }

            return {
                chunks: chunks,
                author: params.author_id
            }
        });
    }
});

App.GenreRoute = App.AuthenticatedRoute.extend({
    model: function(params){
        return Ember.$.getJSON('/api/books/genre/'+params.genre_id, {token:window.user.get('token')}).then(function(data) {
            var chunks = [];

            while (data.books.length > 0) {
                chunks.push(data.books.splice(0,6))
            }

            return {
                chunks: chunks,
                author: params.genre_id
            }
        });
    }
});
