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
