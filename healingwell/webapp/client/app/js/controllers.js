'use strict';

hw.controller = {};

hw.controller.ERROR_OBJ = {message: "An error has occurred, please try again later or contact us.", status: "error"};

hw.controller.BodyCtrl = function ($scope, $element, $http, $cookieStore, $location) {
    var that = this,
        nav_links = [
            {url: "#/workshop", title: "Workshop", group: "clerk", excluded_at: /^\/workshop($|\/)/},
            {url: "#/workshop", title: "Lounge", group: "clerk", included_at: /^\/workshop($|\/)/},
            {url: "#/workshop/ner_training_data", title: "NER Training Data", group: "clerk", included_at: /^\/workshop($|\/)/}
        ];

    $scope.username = $cookieStore.get("username"); //so that app remembers someone has logged in.
    $scope.groups = $cookieStore.get("groups");     //and the groups he belongs to

    this.publish_alert_msg = function(obj) {
        $scope.alert_msg = {
            "class": "alert-" + obj.status,
            header: obj.status.charAt(0).toUpperCase() + obj.status.slice(1) + '!',
            text: obj.message
        };
    };

    $scope.get_nav_links = function() {
        /* selects navigation links that 
         *      1. is not associated with any specific group
         *      2. belongs to the user's groups
         *      3. is included at current url
         *      4. is not excluded at current url
         * marks link of current url as active.
         */
        var path = $location.path();

        return _.map(_.filter(nav_links, function(item) {  
            return (!item.group || _.contains($scope.groups, item.group)) && 
                (!item.included_at || item.included_at.test(path)) &&
                !(item.excluded_at && item.excluded_at.test(path)); 
        }), function(item) {
            if (item.url === '#' + path) {
                item["class"] = "active";
            } else {
                delete item["class"];
            }
            return item;
        });
    };

    $scope.clear_alert_msg = function() {
        delete $scope.alert_msg;
    };

    $scope.login = function() {
        $http({
            method: "POST",
            url: "login",
            data: $element.find("#login_form").serialize(),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function(data) {
            if (data.status === "success") {
                $scope.username = $element.find("input[name=username]").val();
                $cookieStore.put("username", $scope.username);
                $scope.groups = data.groups;
                $cookieStore.put("groups", $scope.groups);
            }
            that.publish_alert_msg(data);
        }).error(function() {
            that.publish_alert_msg(hw.controller.ERROR_OBJ);
        });
    };

    $scope.logout = function() {
        $http({
            method: "GET",
            url: "logout"
        }).success(function(data, status) {
            $scope.username = undefined;
            $scope.groups = undefined;
            $cookieStore.remove("username");
            $cookieStore.remove("groups");
            that.publish_alert_msg(data);
        }).error(function() {
            that.publish_alert_msg(hw.controller.ERROR_OBJ);
        });
    };

    $scope.$on('$routeChangeSuccess', function (event, current, previous) {
        $scope.clear_alert_msg();
    });
};
hw.controller.BodyCtrl.$inject = ["$scope", "$element", "$http", "$cookieStore", "$location"];

hw.controller.HomeCtrl = function ($scope) {
};
hw.controller.HomeCtrl.$inject = ["$scope"];

hw.controller.workshop = {};

hw.controller.workshop.LoungeCtrl = function ($scope) {
};
hw.controller.workshop.LoungeCtrl.$inject = ["$scope"];

hw.controller.workshop.NERTrainingDataCtrl = function ($scope) {
};
hw.controller.workshop.NERTrainingDataCtrl.$inject = ["$scope"];
