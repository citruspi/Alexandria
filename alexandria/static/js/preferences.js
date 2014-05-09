function save(){
    $.post("/preferences", $( document.forms.edit ).serialize(), function(data, textStatus, jqXHR){
        $.growl.notice({
            title: "Success!",
            message: "Settings saved!"
        });
    })
    .fail(function(data){
        $.growl.error({
            title: 'Error!',
            message: 'Your settings failed to save!'
        });
    });
}
