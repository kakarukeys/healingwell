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
    .factory("NERTrainingData", ["NERTrainingDataRest", "$cacheFactory", "$q", function(NERTrainingDataRest, $cacheFactory, $q) {
        function NERTrainingData(obj) {
            _.extend(this, {
                id: obj.id,
                post_content: obj.gerd.post_content,
                tags: _.map(obj.conllstr.split('\n'), function(line) {
                    return _.object(["token", "pos", "iob"], line.split(' '));
                })
            });
        }

        var cache = $cacheFactory('NERTrainingData');

        NERTrainingData.iob_options = [
            "B-FOOD",
            "B-MEDICINE",
            "B-INTERVENTION",
            "B-SYMPTOM",
            "B-DIAGNOSIS",
            "B-PHYSICIAN",
            "O",
            "I-FOOD",
            "I-MEDICINE",
            "I-INTERVENTION",
            "I-SYMPTOM",
            "I-DIAGNOSIS",
            "I-PHYSICIAN"
        ];

        NERTrainingData.get = function(options) {
            var storageKey = angular.toJson(options);
            var result = cache.get(storageKey);
            var params, deferred;

            if (_.isUndefined(result)) {
                params = _.defaults(_.omit(options, "id"), {ordering: "id"});

                return NERTrainingDataRest
                    .get(options.id, {params: params})
                    .then(function(response) {
                        result = _.map(response.data.objects, function(obj) {
                            return new NERTrainingData(obj);
                        });
                        cache.put(storageKey, result);
                        return result;
                    });
            } else {
                deferred = $q.defer();
                deferred.resolve(result);
                return deferred.promise;
            }
        };

        NERTrainingData.prototype.save = function() {
            return NERTrainingDataRest
                .put({
                    id: this.id,
                    conllstr: _.map(this.tags, function(tag) {
                        return tag.token && tag.token + ' ' + tag.pos + ' ' + tag.iob;
                    }).join('\n')
                });
        };

        return NERTrainingData;
    }]);
