var kittyApp = angular.module('kittyApp', [
    'ngRoute',
    'ngCookies',
    'kittyControllers',
    'kittyFilters',
    'kittyServices',
 //   'kittyUserControllers'
]);

kittyApp.run(function run ($http, $cookies, typeheadService) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});