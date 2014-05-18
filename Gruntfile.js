module.exports = function(grunt) {

    grunt.initConfig({
        bowercopy: {
            options: {
                clean: true,
                destPrefix: 'alexandria/static/libs'
            },
            bootstrap: {
                files: {
                    'bootstrap/bootstrap.css': 'bootstrap/dist/css/bootstrap.css',
                    'bootstrap/bootstrap.js': 'bootstrap/dist/js/bootstrap.js'
                }
            },
            dropzone: {
                files: {
                    'dropzone/dropzone.js': 'dropzone/downloads/dropzone.js'
                }
            },
            jquery: {
                files: {
                    'jquery/jquery.js': 'jquery/dist/jquery.js'
                }
            },
            tagmanager: {
                files: {
                    'tagmanager/tagmanager.js': 'tagmanager/tagmanager.js',
                    'tagmanager/tagmanager.css': 'tagmanager/tagmanager.css'
                }
            },
            fontawesome: {
                files: {
                    'fontawesome/css': 'font-awesome/css',
                    'fontawesome/fonts': 'font-awesome/fonts',
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-bowercopy');

};
