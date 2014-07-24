var kittyFilters = angular.module('kittyFilters', []);
kittyFilters.
    filter('cut', function () {
        return function (value, wordwise, max, tail) {
            if (!value) return '';

            max = parseInt(max, 10);
            if (!max) return value;
            if (value.length <= max) return value;

            value = value.substr(0, max);
            if (wordwise) {
                var lastspace = value.lastIndexOf(' ');
                if (lastspace != -1) {
                    value = value.substr(0, lastspace);
                }
            }

            return value + (tail || ' …');
        };
    }).
    filter("nl2br", function($filter) {
        return function(data) {
            if (!data) return data;
            return data.replace(/\n\r?/g, '<br />');
        };
    }).
    filter('addplus', function($filter) {
        return function (data) {
            if ( ! data || isNaN(parseInt(data)) === true) return data;
            return '+' + data;
        };
    });