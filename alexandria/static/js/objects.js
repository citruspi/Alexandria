App.User = Ember.Object.extend({
    token: null,
    name: null
})

window.user = App.User.create({
    token: $.cookie('token')
});
