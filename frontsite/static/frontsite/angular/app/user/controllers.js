'use strict';
kittyApp.requires.push('kittyUserControllers');

var kittyUserControllers = angular.module('kittyUserControllers', []);
/* Controllers */

kittyUserControllers.
controller('UserCtrl', ['$scope', '$http', 'User',
                             function($scope, $http, User) {
    $scope.user = {errors: []};
    $scope.user = User.get({'id': angular.element('input[ng-model=user\\.id]').val()}, function () {
        $scope.user.password = '';
        $scope.user.confirm_password = '';
    });
    $scope.update = function (e) {
        $scope.user.$update({id:$scope.user.id},
            function success (data) {
                if (data.valid === false) {
                    //$scope = data;
                } else {
                    document.location.reload();
                }
            }
        );
        //$scope.user.$get({id:$scope.user.id});
    }
}]);