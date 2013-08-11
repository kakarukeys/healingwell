'use strict';

hw.controller = {};

hw.controller.ERROR_OBJ = {message: "An error has occurred, please try again later or contact us.", status: "error"};
hw.controller.FORBIDDEN_ERROR_OBJ = {message: "You do not have permission for this or you have not logged in.", status: "error"};

hw.controller.BodyCtrl = function ($scope, $element, $http, $cookieStore, $location) {
    var that = this;

    var nav_links = [
        {url: "#/workshop", title: "Workshop", group: "clerk", excluded_at: /^\/workshop($|\/)/},
        {url: "#/workshop", title: "Lounge", group: "clerk", included_at: /^\/workshop($|\/)/},
        {url: "#/workshop/ner_training_data", title: "NER Training Data", group: "clerk", included_at: /^\/workshop($|\/)/}
    ];

    $scope.username = $cookieStore.get("username"); //so that app remembers someone has logged in.
    $scope.groups = $cookieStore.get("groups");     //and the groups he belongs to

    $scope.publish_alert_msg = function(obj) {
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
        }).then(function(response) {
            if (response.data.status === "success") {
                $scope.username = $element.find("input[name=username]").val();
                $cookieStore.put("username", $scope.username);
                $scope.groups = response.data.groups;
                $cookieStore.put("groups", $scope.groups);
            }
            $scope.publish_alert_msg(response.data);
        }, function() {
            $scope.publish_alert_msg(hw.controller.ERROR_OBJ);
        });
    };

    $scope.logout = function() {
        $http({
            method: "GET",
            url: "logout"
        }).then(function(response) {
            $scope.username = undefined;
            $scope.groups = undefined;
            $cookieStore.remove("username");
            $cookieStore.remove("groups");
            $scope.publish_alert_msg(response.data);
        }, function() {
            $scope.publish_alert_msg(hw.controller.ERROR_OBJ);
        });
    };

    $scope.$on('$routeChangeSuccess', function () {
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

hw.controller.workshop.NERTrainingDataCtrl = function($scope, $routeParams, $location, NERTrainingData) {
    var that = this;

    var page_total = 7;
    var current_id = parseInt($routeParams.id, 10);
    var page_no = Math.ceil(current_id / page_total);
    var offset = (page_no - 1) * page_total;
    var record;

    NERTrainingData.get({limit: page_total, page: page_no}).then(function(data) {
        $scope.page_range = _.range(offset + 1, offset + 1 + _.size(data));
        record = _.findWhere(data, {id: current_id});
        $scope.start_editing();
        $scope.is_last_page = _.size(data) < page_total;
    }, function(response) {
        $scope.$parent.publish_alert_msg(hw.controller[(response.status === 403 ? "FORBIDDEN_" : '') + "ERROR_OBJ"]);
    });

    //pagination
    $scope.prev_id = offset + 1 - page_total;
    $scope.next_id = offset + 1 + page_total;
    $scope.is_first_page = offset === 0;

    $scope.is_current = function(num) {
        return num === current_id;
    };

    //goto widget
    $scope.goto = function() {
        if (!isNaN($scope.goto_id)) {
            $location.path("/workshop/ner_training_data/" + $scope.goto_id);
        }
    };

    //save and undo buttons
    $scope.save_change = function() {
        $scope.record.save().then(function() {
            _.extend(record, angular.copy($scope.record));
            $scope.is_dirty = false;
            $scope.$parent.publish_alert_msg({status: "success", message: "Record no. " + record.id + " saved."});
        }, function(response) {
            $scope.$parent.publish_alert_msg(hw.controller[(response.status === 403 ? "FORBIDDEN_" : '') + "ERROR_OBJ"]);
        });
    };

    $scope.start_editing = function() {
        $scope.record = angular.copy(record);
        $scope.is_dirty = false;
    };

    $scope.on_change = function() {
        $scope.is_dirty = true;
    };

    $scope.$on("$locationChangeStart", function(e) {
        if ($scope.is_dirty && !confirm("You have unsaved changes. Are you sure you want to navigate away and lose them?")) {
            e.preventDefault();
        }
    });
};
hw.controller.workshop.NERTrainingDataCtrl.$inject = ["$scope", "$routeParams", "$location", "NERTrainingData"];
