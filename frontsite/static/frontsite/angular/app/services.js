var kittyServices = angular.module('kittyServices', []);

kittyServices.
    factory('typeheadService', [function() {

        var rhymeSearcher = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
            remote: '../typehead-rhymes/%QUERY.json'
        });
        
        rhymeSearcher.initialize();

        $('[name=search]').typeahead(null, {
            name: 'rhyme-search',
            displayKey: 'title',
            highlight: true,
            source: rhymeSearcher.ttAdapter(),
            templates: {
                suggestion: function (value) {
                    var voteStrength = (value.vote_strength) ? value.vote_strength : '0';
                    return '' +
                        '<div>' +
                            '<p>' +
                                value.title +
                            '</p>' +
                            '<span><small class="text-muted">' +
                                value.content.substr(0, 100) +
                            '</small></span>' +
                            '<small class="pull-right"> głosów</small>' +
                            '<label class="badge pull-right">' +
                                '+' + voteStrength +
                             '</label>' +
                        '</div>';
                },
                empty: [
                    '<div class="empty-message">',
                    'Brak podpowiedzi.',
                    '</div>'
                ].join('\n')
            }
        });

    }]);

