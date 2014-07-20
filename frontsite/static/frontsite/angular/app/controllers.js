 'use strict';
  
 var kittyControllers = angular.module('kittyControllers', []);
  /* Controllers */
 
 kittyApp.
 controller('RhymeCtrl',['$scope', '$http',
                       function RhymeListCtrl($scope, $http) {
    $http.get('', function (data) {
        $scope.rhymes = data.data;
    });
    $scope.edit = function edit (e) {
        e.preventDefault();
        if (typeof $scope.fields === 'undefined') $scope.fields = {};
        if (typeof $scope.rhymes === 'undefined') $scope.rhymes = {};

        if (false === angular.element('#demo').hasClass('in')){
            angular.element('button[data-target=#demo]').click();
        }
        //window.location.hash = '#demo';
        $scope.fields.title = 'aaaaaaa';
        console.log($scope.rhymes[2]);
        $scope.rhymes[2] = $scope.rhymes[2] || {}
         console.log($scope.rhymes[2]);
       // $scope.rhymes[2].title = '444444444';
        window['e'] = e;
        window['sc']=$scope
    };

	$scope.add = function add (e) {
        if (typeof $scope.fields === 'undefined') $scope.fields = {};
        $scope.errors = {};
        $scope.fields.content = tinyMCE.activeEditor.getContent();

        $http.
            post(e.currentTarget.action, $scope.fields).
            then(
                function success (response) {
                    var data = response.data;
                    if (data.valid) {
                        document.location.reload();
                    } else {
                        var errors = data.errors;
                        for (var i in errors) {
                            console.log(errors[i][0]);
                            $scope.errors[errors[i][0]] = errors[i][1];
                        }
                    }
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