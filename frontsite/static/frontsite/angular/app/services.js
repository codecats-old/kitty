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
                    return '<div><p>' + value.title + '</p><span><small>' + value.content + '</small></span></div>';
                },
                empty: [
                    '<div class="empty-message">',
                    'Brak podpowiedzi.',
                    '</div>'
                ].join('\n')
            }
        });

    }]);

