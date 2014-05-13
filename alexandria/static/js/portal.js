window.login = function(){
    $.post("/api/portal/login/", $( document.forms.login ).serialize(), function(data, textStatus, jqXHR){
        $('#notification').hide();
        $('#message').html(data.success);
        $('#notification').removeClass();
        $('#notification').addClass('alert-box');
        $('#notification').addClass('success');
        $('#notification').show();
        setTimeout(function(){
            window.location = '/';
        }, 500);
    })
    .fail(function(data){
        $('#notification').hide();
        $('#message').html(data.responseJSON.error);
        $('#notification').removeClass();
        $('#notification').addClass('alert-box');
        $('#notification').addClass('alert');
        $('#notification').show();
    });
}

$('#login-submit').bind('click', function(){
    window.login();
});

$('#login-username').keypress(function (e) {
    if (e.which == 13) {
        window.login();
    }
});

$('#login-password').keypress(function (e) {
    if (e.which == 13) {
        window.login();
    }
});

window.register = function(){
    $.post("/api/portal/register/", $( document.forms.register ).serialize(), function(data, textStatus, jqXHR){
        console.log(1);
        $('#notification').hide();
        $('#message').html(data.success);
        $('#notification').removeClass();
        $('#notification').addClass('alert-box');
        $('#notification').addClass('success');
        $('#notification').show();
    })
    .fail(function(data){
        console.log(data);
        $('#notification').hide();
        $('#message').html(data.responseJSON.error);
        $('#notification').removeClass();
        $('#notification').addClass('alert-box');
        $('#notification').addClass('alert');
        $('#notification').show();
    });
}

$('#register-submit').bind('click', function(){
    console.log('hello');
    window.register();
});

$('#register-realname').keypress(function (e) {
    if (e.which == 13) {
        window.register();
    }
});

$('#register-username').keypress(function (e) {
    if (e.which == 13) {
        window.register();
    }
});

$('#register-emailadd').keypress(function (e) {
    if (e.which == 13) {
        window.register();
    }
});

$('#register-password').keypress(function (e) {
    if (e.which == 13) {
        window.register();
    }
});
