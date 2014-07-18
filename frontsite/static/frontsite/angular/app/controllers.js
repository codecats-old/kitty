 'use strict';
  
 var kittyControllers = angular.module('kittyControllers', []);
  /* Controllers */
 
 kittyApp.controller('RhymeListCtrl',['$scope',
                       function RhymeListCtrl($scope) {
	console.log('a');
	$scope.a = 'b';
 }]);