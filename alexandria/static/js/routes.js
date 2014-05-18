App.IndexRoute = Ember.Route.extend({
    beforeModel: function() {
        this.transitionTo('library');
    }
});

App.BookRoute = Ember.Route.extend({
    model: function(params) {
        return Ember.$.getJSON('/api/book/'+params.book_id).then(function(data){
            console.log(data.book);
            return data.book;
        });
    }
});

App.EditRoute = Ember.Route.extend({
    model: function(params) {
        return Ember.$.getJSON('/api/book/'+params.book_id).then(function(data){
            console.log(data.book);
            return data.book;
        });
    },
    setupController: function(controller, model) {
        controller.set('id', model.id);
        controller.set('title', model.title);
        controller.set('subtitle', model.subtitle);
        controller.set('authors', model.authors.join(','));
        controller.set('description', model.description);
        controller.set('cover', model.cover);
        controller.set('genres', model.genres.join(','));
        controller.set('positiveResponse', null);
        controller.set('negativeResponse', null);
    }
});


App.LibraryRoute = Ember.Route.extend({
    model: function(){
        return Ember.$.getJSON('/api/books/').then(function(data) {
            var chunks = [];

            while (data.books.length > 0) {
                chunks.push(data.books.splice(0,6))
            }

            return chunks;
        });
    }
});

App.SettingsRoute = Ember.Route.extend({
    model: function(){
        return Ember.$.getJSON('/api/settings/').then(function(data) {
            return data.settings;
            console.log(data);
        });
    },
    setupController: function(controller, model) {
        controller.set('realname', model.realname);
        controller.set('emailadd', model.email_address);
    }
});

App.AuthorRoute = Ember.Route.extend({
    model: function(params){
        return Ember.$.getJSON('/api/books/author/'+params.author_id).then(function(data) {
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

App.GenreRoute = Ember.Route.extend({
    model: function(params){
        return Ember.$.getJSON('/api/books/genre/'+params.genre_id).then(function(data) {
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
