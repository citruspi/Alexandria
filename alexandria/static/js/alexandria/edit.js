function save(){
    $.post("/edit/"+window.id, $( document.forms.edit ).serialize(), function(data, textStatus, jqXHR){
        $.growl.notice({
            title: "Success!",
            message: "Edit saved!"
        });
    })
    .fail(function(data){
        $.growl.error({
            title: 'Error!',
            message: 'The edit failed to save!'
        });
    });
}
