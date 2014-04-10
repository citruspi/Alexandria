window.flexVerticalCenter(document.getElementById('notice'));

$(document.body).dropzone({
    url: "/upload",
    paramName: "file",
    clickable: true,
    previewsContainer: ".previewsContainer",
    success: function(file, response) {
        if (window.confirm){
            document.getElementById('query').value = file.name.split('.')[0];
            getResults();
            $('#myModal').foundation('reveal', 'open');
            window.token = response.filename;
        }
        else {
            noConfirm(response.filename, file.name.split('.')[0]);
        }
    }
});

$('#select').bind('change',function(){
    var e = document.getElementById("select");
    var value = e.options[e.selectedIndex].value;
    displayResult(value);
});

function noConfirm (token, query) {

    if (query !== null && query !== '') {

        $.getJSON( "https://www.googleapis.com/books/v1/volumes?q="+query, function( data ) {

            $.post("/confirm/"+token+'/'+data.items[0].id, function (response){
                $.growl.notice({
                    title: 'Success!',
                    message: data.items[0].volumeInfo.title + ' was uploaded!'
                });
            })
            .fail(function(data) {
                $.growl.error({
                    title: 'Error!',
                    message: data.responseJSON.error
                });
            });

        });

    }

}

function listResults () {
    window.results.forEach(function(i) {

        var opt = document.createElement('option');
        opt.value = i.id;
        opt.innerHTML = (function () {

            var title = i.volumeInfo.title;

            if (i.volumeInfo.authors !== null) {

                title += ' - ';

                if (i.volumeInfo.authors.length < 2) {
                    title += i.volumeInfo.authors[0] + ' ';
                }

                else {
                    i.volumeInfo.authors.forEach(function(author) {
                        title += author + '; ';
                    });
                }

            }

            if (i.volumeInfo.publishedDate !== null) {

                return title + '(' + i.volumeInfo.publishedDate.substring(0,4) + ')';

            }

        })();

        document.getElementById('select').appendChild(opt);

    });
}

function displayResult (id) {
    window.results.forEach(function(i){
        if (i.id == id){
            var template = $('#template').html();
            Mustache.parse(template);   // optional, speeds up future uses
            var rendered = Mustache.render(template, {
                title: i.volumeInfo.title,
                subtitle: i.volumeInfo.subtitle,
                authors: i.volumeInfo.authors,
                description: i.volumeInfo.description,
                "cover": function () {
                    var covers = i.volumeInfo.imageLinks;
                    if (covers.extraLarge !== null && covers.extraLarge !== '') {
                        return covers.extraLarge;
                    }
                    else if (covers.large !== null && covers.large !== '') {
                        return covers.large;
                    }
                    else if (covers.medium !== null && covers.medium !== '') {
                        return covers.medium;
                    }
                    else if (covers.small !== null && covers.small !== '') {
                        return covers.small;
                    }
                    else if (covers.thumbnail !== null && covers.thumbnail !== '') {
                        return covers.thumbnail;
                    }
                    else if (covers.smallThumbnail !== null && covers.smallThumbnail !== '') {
                        return covers.smallThumbnail;
                    }
                    else {
                        return '';
                    }
                }
            });
            $('#result').html(rendered);
        }
    });
}

$(document).on('closed', '[data-reveal]', function () {
    window.results = null;
    $("#select").empty();
    $("#result").empty();
});

function confirmResult() {
    var e = document.getElementById("select");
    var value = e.options[e.selectedIndex].value;

    $.post("/confirm/"+window.token+'/'+value, $( document.forms.confirm ).serialize());

    window.results.forEach(function(i){
        if (i.id == value){
            $.growl.notice({
                title: "Success!",
                message: i.volumeInfo.title + " was uploaded!"
            });
        }
    });

    $('#myModal').foundation('reveal', 'close');

    return false;
}

function getResults() {

    query = document.getElementById('query').value;

    if (query !== null && query !== '') {

        $("#select").empty();

        $.getJSON( "https://www.googleapis.com/books/v1/volumes?q="+query, function( data ) {

            window.results = data.items;

            listResults();
            displayResult(data.items[0].id);


        });

    }

    return false;
}
