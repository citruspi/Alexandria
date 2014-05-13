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
    beforeModel: function(params) {
        $.getScript('/static/js/edit.js');
    },
    model: function(params) {
        return Ember.$.getJSON('/api/book/'+params.book_id).then(function(data){
            console.log(data.book);
            return data.book;
        });
    }
});


App.LibraryRoute = Ember.Route.extend({
    model: function(){
        return Ember.$.getJSON('/api/books/').then(function(data) {
            return data.books;
        });
    }
});

App.SettingsRoute = Ember.Route.extend({
    model: function(){
        return Ember.$.getJSON('/api/settings/').then(function(data) {
            return data.settings;
            console.log(data);
        });
    }
});

App.AuthorRoute = Ember.Route.extend({
    model: function(params){
        return Ember.$.getJSON('/api/books/author/'+params.author_id).then(function(data) {
            return {
                books: data.books,
                author: params.author_id
            }
        });
    }
});

App.GenreRoute = Ember.Route.extend({
    model: function(params){
        return Ember.$.getJSON('/api/books/genre/'+params.genre_id).then(function(data) {
            return {
                books: data.books,
                genre: params.genre_id
            }
        });
    }
});
