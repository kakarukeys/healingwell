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
        function NERTrainingData(obj) {
            _.extend(this, {
                id: obj.id,
                post_content: obj.gerd.post_content,
                tags: _.map(obj.conllstr.split('\n'), function(line) {
                    return _.object(["token", "pos", "iob"], line.split(' '));
                })
            });
        }

        NERTrainingData.prototype.save = function() {
            return NERTrainingDataRest
                .put({
                    id: this.id,
                    conllstr: _.map(this.tags, function(tag) {
                        return tag.token && tag.token + ' ' + tag.pos + ' ' + tag.iob;
                    }).join('\n')
                })
                .error(hw.error_callback);
        };

        return function(limit, page_no) {
            return NERTrainingDataRest
                .get(undefined, {params: {limit: limit, page: page_no}})
                .then(function(response) {
                    return _.map(response.data.objects, function(obj) {
                        return new NERTrainingData(obj);
                    });
                }, hw.error_callback);
        };
    }]);
