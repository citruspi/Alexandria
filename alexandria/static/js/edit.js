$('#save').bind('click', function(){

    var description = document.createElement('input');
    description.type = "hidden";
    description.name = "description";
    description.value = window.descriptionEditor.getHTML();
    document.forms.edit.appendChild(description);

    $.post("/api/book/"+window.id, $( document.forms.edit ).serialize(), function(data, textStatus, jqXHR){
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

    document.forms.edit.removeChild(document.getElementsByName("description")[0]);

});

function loadEditor(){

  var descriptionEditor, cursorManager;

  descriptionEditor = new Quill('.editor-wrapper .editor-container', {
    modules: {
      'toolbar': {
        container: '.editor-wrapper .toolbar-container'
      },
      'link-tooltip': true,
      'image-tooltip': true,
    },
    theme: 'snow'
  });

  window.descriptionEditor = descriptionEditor;

}
