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

App.EditController = Ember.Controller.extend({
    actions: {
        addAuthor: function(){
            var table = document.getElementById('authors').getElementsByTagName('tbody')[0];
            var row = table.insertRow(table.rows.length);
            var cell = row.insertCell(0);
            var content  = document.createTextNode(this.get('author'));;
            cell.appendChild(content);
            window.flexVerticalCenter(document.getElementById('notice'));
        },
        addGenre: function(){
            var table = document.getElementById('genres').getElementsByTagName('tbody')[0];
            var row = table.insertRow(table.rows.length);
            var cell = row.insertCell(0);
            var content  = document.createTextNode(this.get('genre'));;
            cell.appendChild(content);
            window.flexVerticalCenter(document.getElementById('notice'));
        },
        save: function(){
            id = location.href.split("/").slice(-1);
            $.post('/api/book/'+id, {
                title: this.get('title'),
                subtitle: this.get('subtitle'),
                cover: this.get('cover'),
                description: this.get('description'),
                authors: function() {

                    var table = document.getElementById('authors').getElementsByTagName('tbody')[0];

                    authors = [];

                    for(var i=0; i<table.rows.length;i++){
                        authors.push(table.rows[i].cells[0].innerHTML);
                    }

                    return authors;
                },
                genres: function() {

                    var table = document.getElementById('genres').getElementsByTagName('tbody')[0];

                    genres = [];

                    for(var i=0; i<table.rows.length;i++){
                        genres.push(table.rows[i].cells[0].innerHTML);
                    }

                    return genres;
                }
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
})
