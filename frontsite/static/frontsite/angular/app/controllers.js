 'use strict';
  
 var kittyControllers = angular.module('kittyControllers', []);
  /* Controllers */
 
 kittyApp.
 controller('RhymeCtrl',['$scope', '$http',
                       function RhymeListCtrl($scope, $http) {
    if (typeof $scope.rhymes === 'undefined') $scope.rhymes = [];
    $scope.formState = 'Dodawanie';
    var rhymes = $('[rhyme]');
    rhymes.each(function(it) {
        var rhyme = $(rhymes[it]);
        $scope.rhymes[it + 1] = {
            'id': rhyme.find('id').html(),
            'title': rhyme.find('title').html(),
            'content': rhyme.find('content').html(),
            'category': rhyme.find('category').html()
        };
    });

    $scope.delete = function remove (e, loopCounter) {
        e.preventDefault();
        if (typeof $scope.fields === 'undefined') $scope.fields = {};
        $http.
            post(e.currentTarget.href).
            then(
                function success (response) {
                    document.location.reload();
                }
            );
    };

    $scope.edit = function edit (e, loopCounter) {
        e.preventDefault();
        if (typeof $scope.fields === 'undefined') $scope.fields = {};
        $scope.formState = 'Edycja';
        $scope.formAction = e.currentTarget.href;

        if (false === angular.element('#demo').hasClass('in')){
            angular.element('button[data-target=#demo]').click();
        }
        window.location.hash = '#demo';

        $scope.fields.title = $scope.rhymes[loopCounter].title;
        $scope.fields.content = $scope.rhymes[loopCounter].content;
        tinyMCE.activeEditor.setContent($scope.rhymes[loopCounter].content, {format : 'raw'});
        $scope.fields.category = $scope.rhymes[loopCounter].category;
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