'use strict';

 var kittyStoredControllers = angular.module('kittyStoredControllers', []);
  /* Controllers */

 kittyApp.controller('ExportCtrl', ['$scope', '$http',
                                 function($scope, $http) {
        $scope.collapse = function (hide) {
            var trigger = '[name=collapsible-content]';
            if (typeof hide === 'undefined') hide = null;

            var element = angular.element(trigger);
            hide = (hide === null) ? element.hasClass('in') : hide;
            $scope.exportModeState = hide;
            hide = (hide === true) ? 'hide' : 'show';

            element.collapse(hide);
        };
        $scope.showCheckbox = function (hide) {
            var trigger = '[name=export-checkbox]';
            if (typeof hide === 'undefined') hide = null;
            var element = angular.element('.checkbox');

            hide = (hide === null) ? ! element.is(':visible') : hide;
            if (hide === false) {
                element.hide();
            } else {
                element.show();
            }
        };
        $scope.exportMode = function (e) {
            $scope.collapse();
            $scope.showCheckbox();
            var cancelBtn = angular.element('#cancelBtn').show('fast'),
                exportBtn = angular.element('#exportBtn');
            if ($scope.exportModeState) {

                $scope.selectModeBtn = 'Eksportuj';

                console.log($scope.selectModeBtn);
                exportBtn.addClass('btn-danger');
                cancelBtn.show('fast');
                cancelBtn.removeClass('disabled');
                exportBtn.unbind();
                exportBtn.bind('click', $scope.exportAction);
            } else {
                exportBtn.removeClass('btn-danger');
                cancelBtn.hide('fast');
                cancelBtn.addClass('disabled');
            }

        };
        $scope.exportAction = function (e) {
            e.preventDefault();
            var selection = angular.element('input[select-name=rhymeIds]'),
                exportIds = [];

            selection.each(function () {
                var item = angular.element(this);
                if (item.is(':checked')) {
                    exportIds.push(item.val());
                }
            });
            var url = '/pdf/export/' + JSON.stringify(exportIds);
            window.open(url,'_blank');
        };
        $scope.cancelExport = function (e) {
            var cancelBtn = angular.element('#cancelBtn').show('fast'),
                exportBtn = angular.element('#exportBtn');
            $scope.selectModeBtn = 'Eksportuj/Zaznacz';
            exportBtn.unbind('click');
            exportBtn.bind('click', $scope.exportMode);
            exportBtn.removeClass('btn-danger');
            cancelBtn.hide('fast');
            cancelBtn.addClass('disabled');
            $scope.collapse(false);
            $scope.showCheckbox(false);
        }

        $scope.selectModeBtn = 'Eksportuj/Zaznacz';
        $scope.cancelBtn = 'Anuluj';
        $scope.exportModeState = false;
        angular.element('#cancelBtn').hide();
        $scope.showCheckbox();
      window.s = $scope;

 }]);