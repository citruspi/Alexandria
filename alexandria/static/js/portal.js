$.ajax({
    url: '/static/handlebars/portal.hbs',
    dataType: 'text',
    async: false,
    success: function (response) {
        Ember.TEMPLATES['portal'] = Ember.Handlebars.compile(response);
    }
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
    this.resource('portal', { path: '/' });
});

App.PortalController = Ember.Controller.extend({
    actions: {
        login: function() {
            console.log('helo');
            $.post('/api/portal/login/', {
                username: this.get('l_username'),
                password: this.get('l_password')
            }).then(function(){
                $('#feedback').hide();
                window.location = '/';
            }, function(){
                $('#feedback').hide();
                $('#feedback').html('There was problem logging you in.');
                $('#feedback').removeClass();
                $('#feedback').addClass('alert');
                $('#feedback').addClass('alert-danger');
                $('#feedback').show();
            });
        },
        register: function() {
            $.post('/api/portal/register/', {
                realname: this.get('n_realname'),
                username: this.get('n_username'),
                emailadd: this.get('n_emailadd'),
                password: this.get('n_password')
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
