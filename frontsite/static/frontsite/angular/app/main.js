var kittyApp = angular.module('kittyApp', [
    'ngRoute',
    'ngCookies',
//    'phonecatControllers',
    'kittyFilters',
    'kittyServices'
]);

kittyApp.run(function run ($http, $cookies, typeheadService) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});