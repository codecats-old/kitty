kittyApp.requires.push('kittyUserServices');

var kittyUserServices = angular.module('kittyUserServices', ['ngResource']);

kittyUserServices.factory('User', ['$resource',
    function ($resource) {
        return  $resource('/user/:id.json', {}, {
            query:  {method: 'GET', params: {id: ''} },
            update: {method: 'PUT', params: {id: ''} }
        });
    }]);