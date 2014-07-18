 'use strict';
  
 var kittyControllers = angular.module('kittyControllers', []);
  /* Controllers */
 
 kittyApp.
 controller('RhymeListCtrl',['$scope',
                       function RhymeListCtrl($scope) {
	console.log('a');
	$scope.a = 'b';
 }]).
 controller('VoteRhymeCtrl', ['$scope', '$http',
                        function VoteRhymeCtrl($scope, $http) {
    $scope.log = function (e) {
        e.preventDefault();
        window['h'] = $http;
        $http.get(e.currentTarget.href).success(function (data) {
            e.target.textContent = ' ' + data.strength;
        });
        window['e'] = e;
        window['t'] = this;

    };
 }]);