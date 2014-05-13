['book', 'author', 'genre', 'library', 'application'].forEach(function(template){
    $.ajax({
        url: '/static/handlebars/'+template+'.hbs',
        dataType: 'text',
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
    this.resource('book', { path: '/book/:book_id' }, function() {
        this.route('edit');
    });
    this.resource('genre', { path: '/genre/:genre_id' });
    this.resource('author', { path: '/author/:author_id' });
});
