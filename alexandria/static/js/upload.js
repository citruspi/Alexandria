window.flexVerticalCenter(document.getElementById('notice'));
window.flexVerticalCenter(document.getElementById('text'));

var dropzone = new Dropzone("#box", {
    url: "/api/upload/",
    paramName: "file",
    clickable: true,
    previewsContainer: ".previewsContainer",
    autoProcessQueue: false,
    maxFiles: 1,
    addedfile: function(file) {

        file.previewElement = document.getElementsByClassName('previewsContainer')[0];
        $('#fileName').text(file.name);
        $('#query').val(file.name.split('.')[0]);
        $("#search")[0].click();

        $('#box').addClass('animated bounceOutLeft');
        $('#box').css("display", "none");
        $('#part-1').show();
        $('#part-1').addClass('animated bounceInRight');

    },
    uploadprogress: function(file, progress, bytesSent) {

        $('#meter').width(progress*'%');

        if (progress === 100){
            $("#progress").addClass("success");
        }

    },
    sending: function(file, xhr, formData) {

        formData.append('title', $('#title').val());
        formData.append('subtitle', $('#subtitle').val());

        var table = document.getElementById('authors').getElementsByTagName('tbody')[0];

        authors = []

        for(var i=0; i<table.rows.length;i++){
            authors.push(table.rows[i].cells[0].innerHTML);
        }

        formData.append('authors', authors);

        formData.append('publisher', $('#publisher').val());
        formData.append('date-published', $('#datepublished').val());
        formData.append('isbn-10', $('#isbn-10').val());
        formData.append('isbn-13', $('#isbn-13').val());

        var table = document.getElementById('genres').getElementsByTagName('tbody')[0];

        genres = []

        for(var i=0; i<table.rows.length;i++){
            genres.push(table.rows[i].cells[0].innerHTML);
        }

        formData.append('genres', genres);

        formData.append('description', window.descriptionEditor.getHTML());
        formData.append('cover', $('#pcover').val());

    },
    success: function(file, response) {
        $('#part-5').addClass('animated bounceOutLeft');
        $('#part-5').css("display", "none");
        $('#part-6').show();
        $('#part-6').addClass('animated bounceInRight');
        window.flexVerticalCenter(document.getElementById('notice'));
    }
});

$('#repeat').bind('click', function(){
    window.location.reload(false);
})

$('#library').bind('click', function(){
    window.location = '/library';
})

$('#add-author').bind('click', function(){
    var table = document.getElementById('authors').getElementsByTagName('tbody')[0];
    var row = table.insertRow(table.rows.length);
    var cell = row.insertCell(0);
    var content  = document.createTextNode($('#pauthor').val());
    cell.appendChild(content);
    window.flexVerticalCenter(document.getElementById('notice'));
});

$('#add-genre').bind('click', function(){
    var table = document.getElementById('genres').getElementsByTagName('tbody')[0];
    var row = table.insertRow(table.rows.length);
    var cell = row.insertCell(0);
    var content  = document.createTextNode($('#pgenre').val());
    cell.appendChild(content);
    window.flexVerticalCenter(document.getElementById('notice'));
});

$('#preview-cover').bind('click', function() {
    $('#cover-view').attr('src', $('#pcover').val());
    window.flexVerticalCenter(document.getElementById('notice'));
})

$('#continue-1').bind('click', function(){
    $('#part-1').addClass('animated bounceOutLeft');
    $('#part-1').css("display", "none");
    $('#part-2').show();
    $('#part-2').addClass('animated bounceInRight');
    window.flexVerticalCenter(document.getElementById('notice'));
});

$('#continue-2').bind('click', function(){
    $('#part-2').addClass('animated bounceOutLeft');
    $('#part-2').css("display", "none");
    $('#part-3').show();
    $('#part-3').addClass('animated bounceInRight');
    window.flexVerticalCenter(document.getElementById('notice'));
});

$('#continue-3').bind('click', function(){
    $('#part-3').addClass('animated bounceOutLeft');
    $('#part-3').css("display", "none");
    $('#part-4').show();
    $('#part-4').addClass('animated bounceInRight');
    window.flexVerticalCenter(document.getElementById('notice'));
});

$('#continue-4').bind('click', function(){
    $('#part-4').addClass('animated bounceOutLeft');
    $('#part-4').css("display", "none");
    $('#part-5').show();
    $('#part-5').addClass('animated bounceInRight');
    dropzone.processQueue();
    window.flexVerticalCenter(document.getElementById('notice'));
})

$('#search').bind('click', function(){
    $.getJSON('/api/upload/search/'+$('#query').val(), function (data) {
        book = data.results.items[0];

        $('#title').val(book.volumeInfo.title);
        $('#subtitle').val(book.volumeInfo.subtitle);

        book.volumeInfo.authors.forEach(function(author) {
            var table = document.getElementById('authors').getElementsByTagName('tbody')[0];
            var row = table.insertRow(table.rows.length);
            var cell = row.insertCell(0);
            var content  = document.createTextNode(author + ' (' + String.fromCharCode(215) + ')');
            cell.appendChild(content);
        });

        $('#publisher').val(book.volumeInfo.publisher);
        $('#date-published').val(book.volumeInfo.publishedDate);

        book.volumeInfo.industryIdentifiers.forEach(function(entry){
            if (entry.type === "ISBN_10") {
                $("#isbn-10").val(entry.identifier);
            }
            if (entry.type === "ISBN_13") {
                $("#isbn-13").val(entry.identifier);
            }
        });

        window.descriptionEditor.setHTML(book.volumeInfo.description);

        var covers = book.volumeInfo.imageLinks;

        if (covers.extraLarge !== null && covers.extraLarge !== '' && typeof covers.extraLarge !== 'undefined') {
            $('#pcover').val(covers.extraLarge);
            $('#cover-view').attr('src', covers.extraLarge);
        }
        else if (covers.large !== null && covers.large !== '' && typeof covers.large !== 'undefined') {
            $('#pcover').val(covers.large);
            $('#cover-view').attr('src', covers.large);
        }
        else if (covers.medium !== null && covers.medium !== '' && typeof covers.medium !== 'undefined') {
            $('#pcover').val(covers.medium);
            $('#cover-view').attr('src', covers.medium);
        }
        else if (covers.small !== null && covers.small !== '' && typeof covers.small !== 'undefined') {
            $('#pcover').val(covers.small);
            $('#cover-view').attr('src', covers.small);
        }
        else if (covers.thumbnail !== null && covers.thumbnail !== '' && typeof covers.thumbnail !== 'undefined') {
            $('#pcover').val(covers.thumbnail);
            $('#cover-view').attr('src', covers.thumbnail);
        }
        else if (covers.smallThumbnail !== null && covers.smallThumbnail !== '' && typeof covers.smallThumbnail !== 'undefined') {
            $('#pcover').val(covers.smallThumbnail);
            $('#cover-view').attr('src', covers.smallThumbnail);
        }
    })
});

var genres = ['Computers', 'Fiction', 'Non-Fiction', 'Comics', 'Graphic Novels'];

var substringMatcher = function(strs) {
    return function findMatches(q, cb) {

        var matches, substringRegex;

        matches = [];

        substrRegex = new RegExp(q, 'i');

        $.each(strs, function(i, str) {
            if (substrRegex.test(str)) {
                matches.push({ value: str });
            }
        });

        cb(matches);
    };
};

(function() {

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

}).call(this);


$('#pgenre').typeahead({
    hint: true,
    highlight: true,
    minLength: 0
},
{
    name: 'genres',
    displayKey: 'value',
    source: substringMatcher(genres)
});

$('.tt-input').width(550);
