'use strict';

angular.module('healingwell.services', [])
    .factory("NERTrainingDataRest", ["$http", function($http) {
        return {
            get: function(id, config) {
                return $http.get("api/nertrainingdata/" + (_.isUndefined(id) ? '' : id + '/'), config);
            },
            put: function(obj, config) {
                return $http.put("api/nertrainingdata/" + obj.id + '/', _.omit(obj, "id"), config);
            }
        };
    }])
    .factory("NERTrainingDataSource", ["NERTrainingDataRest", function(NERTrainingDataRest) {
        return function(limit, page_no) {
            return NERTrainingDataRest
                .get(undefined, {params: {limit: limit, page: page_no}, cache: true})
                .then(function(response) {
                    return _.map(response.data.objects, function(obj) {
                        return {
                            id: obj.id,
                            post_content: obj.gerd.post_content,
                            tags: _.map(obj.conllstr.split('\n'), function(line) {
                                return _.object(["token", "pos", "iob"], line.split(' '));
                            })
                        };
                    });
                }, function() {
                    alert("There seems to be an error. Please try again later.");
                });
        };
    }]);
