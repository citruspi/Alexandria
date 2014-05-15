['application', 'book', 'author', 'genre', 'library', 'settings', 'edit', 'upload'].forEach(function(template){
    $.ajax({
        url: '/static/handlebars/'+template+'.hbs',
        dataType: 'text',
        async: false,
        success: function (response) {
            Ember.TEMPLATES[template] = Ember.Handlebars.compile(response);
        }
    });
});

var App = Ember.Application.create({
    LOG_TRANSITIONS: true,
    LOG_BINDINGS: true,
    LOG_VIEW_LOOKUPS: true,
    LOG_STACKTRACE_ON_DEPRECATION: true,
    LOG_VERSION: true,
    debugMode: true
});

App.Router.map(function () {
    this.resource('library');
    this.resource('settings');
    this.resource('upload');
    this.resource('book', { path: '/book/:book_id' });
    this.resource('edit', { path: '/edit/:book_id' });
    this.resource('genre', { path: '/genre/:genre_id' });
    this.resource('author', { path: '/author/:author_id' });
});
