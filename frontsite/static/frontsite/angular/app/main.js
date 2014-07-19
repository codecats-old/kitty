var kittyApp = angular.module('kittyApp', [
    'ngRoute',
    'ngCookies'
//    'phonecatControllers',
//    'phonecatFilters',
//    'phonecatServices'
]);

kittyApp.run(function run ($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});