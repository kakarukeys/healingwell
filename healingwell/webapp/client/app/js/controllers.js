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

hw.controller.workshop.NERTrainingDataCtrl = function($scope, $routeParams, $location) {
    var that = this,
        page_total = 7,
        current_id = parseInt($routeParams.id),
        offset = page_total * Math.floor((current_id - 1) / page_total);

    this.loadData = function(limit, offset) {
        if (_.random(0, 10) == 0) {
            return [];
        } else {
            return [
                {
                    id: offset + 1,
                    post_content: "bla bla bla",
                    iob: [
                        {token: "bla", tag: "O"},
                        {token: "bla", tag: "B-PER"},
                        {token: "bla", tag: "I-PER"}
                    ]
                },
                {
                    id: offset + 1 + 1,
                    post_content: "bla bla bla la la",
                    iob: [
                        {token: "ble", tag: "O"},
                        {token: "ble", tag: "B-PER"},
                        {token: "ble", tag: "I-PER"}
                    ]
                },
                {
                    id: offset + 1 + 2,
                    post_content: "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    iob: [
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"},
                        {token: "Lorem", tag: "O"},
                        {token: "Overnumerousnesses", tag: "B-PER"},
                        {token: "ipsum", tag: "I-PER"}
                    ]
                },
                {
                    id: offset + 1 + 3,
                    post_content: "bla bla bla",
                    iob: [
                        {token: "bla", tag: "O"},
                        {token: "bla", tag: "B-PER"},
                        {token: "bla", tag: "I-PER"}
                    ]
                },
                {
                    id: offset + 1 + 4,
                    post_content: "bla bla bla la la",
                    iob: [
                        {token: "bla", tag: "O"},
                        {token: "bla", tag: "B-PER"},
                        {token: "bla", tag: "I-PER"}
                    ]
                },
                {
                    id: offset + 1 + 5,
                    post_content: "bla bla bla la la la",
                    iob: [
                        {token: "bla", tag: "O"},
                        {token: "bla", tag: "B-PER"},
                        {token: "bla", tag: "I-PER"}
                    ]
                },
                {
                    id: offset + 1 + 6,
                    post_content: "bla bla bla la la la",
                    iob: [
                        {token: "bla", tag: "O"},
                        {token: "bla", tag: "B-PER"},
                        {token: "bla", tag: "I-PER"}
                    ]
                }
            ];
        }
    };

    $scope.data = that.loadData(page_total, offset);

    //pagination
    $scope.prev_id = offset + 1 - page_total;
    $scope.next_id = offset + 1 + page_total;
    $scope.is_first_page = offset === 0;

    $scope.page_range = _.range(offset + 1, offset + 1 + _.size($scope.data));
    $scope.record = _.findWhere($scope.data, {id: current_id});
    $scope.is_last_page = _.size($scope.data) < page_total;

    $scope.is_current = function(num) {
        return num === current_id;
    };

    //goto widget
    $scope.goto = function() {
        if (!isNaN($scope.goto_id)) {
            $location.path("/workshop/ner_training_data/" + $scope.goto_id);
        }
    };
};
hw.controller.workshop.NERTrainingDataCtrl.$inject = ["$scope", "$routeParams", "$location"];
