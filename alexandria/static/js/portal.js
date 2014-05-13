window.login = function(){
    $.post("/api/portal/login/", $( document.forms.login ).serialize(), function(data, textStatus, jqXHR){
        $('#notification').hide();
        $('#message').html(data.success);
        $('#notification').removeClass();
        $('#notification').addClass('alert-box');
        $('#notification').addClass('success');
        $('#notification').show();
        setTimeout(function(){
            window.location = '/library';
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
