 'use strict';
  
 var kittyControllers = angular.module('kittyControllers', []);
  /* Controllers */
 
 kittyApp.
 controller('RhymeCtrl',['$scope', '$http',
                       function RhymeListCtrl($scope, $http) {
	$scope.add = function (e) {
        if (typeof $scope.fields === 'undefined') $scope.fields = {};
        $scope.fields.content = tinyMCE.activeEditor.getContent();
        $http.
            post(e.currentTarget.action, $scope.fields).
            then(
                function success (response) {
                    console.log(response);
                },
                function failure (response) {

                }
            );
    };
 }]).
 controller('VoteRhymeCtrl', ['$scope', '$http',
                        function VoteRhymeCtrl($scope, $http) {
    $scope.vote = function (e) {
        e.preventDefault();
        $http.get(e.currentTarget.href).success(function (data) {
            e.target.textContent = ' ' + data.strength;
        });
    };
 }]);