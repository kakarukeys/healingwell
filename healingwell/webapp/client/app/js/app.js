'use strict';

// Setting up namespace
var hw = {};

// Declare app level module which depends on filters, and services
angular.module('healingwell', ['ngCookies', 'healingwell.filters', 'healingwell.services', 'healingwell.directives'])
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('', {
            title: "Healingwell Analytics", 
            templateUrl: 'partials/home.html', 
            controller: hw.controller.HomeCtrl
        })
        .otherwise({redirectTo: ''});
    }])
    .run(['$location', '$rootScope', function($location, $rootScope) {
        $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
            /* changes title automatically on routing */
            if (current.$route) {
                $rootScope.title = current.$route.title;
            }
        });
    }]);
