'use strict';

// Setting up namespace
var hw = {};

hw.TITLE = "Healingwell Analytics";

// Declare app level module which depends on filters, and services
angular.module('healingwell', ['ngCookies', 'healingwell.filters', 'healingwell.services', 'healingwell.directives'])
    .config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('', {
            title: "", 
            templateUrl: 'partials/home.html', 
            controller: hw.controller.HomeCtrl
        })
        .when('/workshop', {
            title: "Workshop", 
            templateUrl: 'partials/workshop/lounge.html', 
            controller: hw.controller.workshop.LoungeCtrl
        })
        .when('/workshop/ner_training_data', {
            title: "NER Training Data Editor", 
            templateUrl: 'partials/workshop/ner_training_data.html', 
            controller: hw.controller.workshop.NERTrainingDataCtrl
        })
        .otherwise({redirectTo: ''});
    }])
    .run(['$location', '$rootScope', function($location, $rootScope) {
        $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
            /* changes title automatically on routing */
            if (current.$route) {
                $rootScope.title = current.$route.title + (current.$route.title ? " - " : '') + hw.TITLE;
            }
        });
    }]);
