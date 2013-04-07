'use strict';

hw.controller = {};

hw.controller.ERROR_OBJ = {message: "An error has occurred, please try again later or contact us.", status: "error"};

hw.controller.BodyCtrl = function ($scope, $element, $http, $cookies) {
	var that = this;

	$scope.username = $cookies.username;	//so that app remembers someone has logged in.

	this.publish_alert_msg = function(obj) {
		$scope.alert_msg = {
			class: "alert-" + obj.status,
			header: obj.status.charAt(0).toUpperCase() + obj.status.slice(1) + '!',
			text: obj.message
		};
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
				$cookies.username = $scope.username = $element.find("input[name=username]").val();
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
			$cookies.username = $scope.username = undefined;
			that.publish_alert_msg(data);
		}).error(function() {
			that.publish_alert_msg(hw.controller.ERROR_OBJ);
		});
	}
};
hw.controller.BodyCtrl.$inject = ["$scope", "$element", "$http", "$cookies"];

hw.controller.HomeCtrl = function ($scope) {
};
hw.controller.HomeCtrl.$inject = ["$scope"];
