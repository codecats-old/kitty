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
            var mode = hide;
            hide = (hide === true) ? 'hide' : 'show';

            element.collapse(hide);
            return mode;
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
            $scope.exportModeState = $scope.collapse();
            $scope.showCheckbox();
            var cancelBtn = angular.element('#cancelBtn').show('fast'),
                exportBtn = angular.element('#exportBtn');
            if ($scope.exportModeState) {

                $scope.selectModeBtn = 'Eksportuj';

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
                    $scope.cancelExport();
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
            $scope.exportModeState = $scope.collapse(false);
            $scope.showCheckbox(false);
        };
        $scope.dragMode = function (e) {
            $scope.dragModeState = $scope.collapse();
            if ($scope.dragModeState) {
                angular.element('#cancelDragDropBtn').removeClass('disabled');
                angular.element('#saveDragDropBtn').removeClass('disabled');
                var rhymes = angular.element('article.rhyme');
                rhymes.css('cursor', 'pointer');
                angular.element('#dragBtn').addClass('btn-danger');

                rhymes.unbind();
                var startPos = {},
                    dragRhyme = null;

                rhymes.draggable({
                    disabled:false,
                    revert: "invalid",
                    start: function (e, ui) {
                        dragRhyme = $(this);
                        startPos = dragRhyme.offset();
                    }
                });
                rhymes.droppable({
                    drop: function(e, ui){

                        var dropRhyme = angular.element(this),
                            offset = {y: dropRhyme.offset().top, x: dropRhyme.offset().left};
                        dropRhyme.offset({left: startPos.left, top: startPos.top});

                        dragRhyme.offset({left: offset.x, top: offset.y});
                        startPos = {};
                        $scope.$emit('dropDetected');

                    }
                });
                rhymes.bind('mousedown', function () {
                    var rhyme = angular.element(this);
                    rhyme.css('z-index', 1);
                });
                rhymes.bind('mouseup', function () {
                    var rhyme = angular.element(this);
                    rhyme.css('z-index', 'auto');
                });

            } else {
                angular.element('article.rhyme').css('cursor', '');
                angular.element('#dragBtn').removeClass('btn-danger');
            }
        };
        $scope.$on('dropDetected', function () {
            angular.element('#modalRefresh').modal('show').modal('hide');
        });
        $scope.cancelDrag = function (e) {
            document.location.reload();
        };
        $scope.saveDrag = function (e) {
            document.location.reload();
        };
        $scope.modalTitle = 'Zatwierdzić zmiany?';
        $scope.modalBody = 'Bez zatwierdzenia dane zostaną utracone';
        $scope.selectModeBtn = 'Eksportuj/Zaznacz';
        $scope.cancelBtn = 'Anuluj';
        $scope.exportModeState = false;
        $scope.dragModeState = false;
        angular.element('#cancelBtn').hide();
        $scope.showCheckbox();

 }]);