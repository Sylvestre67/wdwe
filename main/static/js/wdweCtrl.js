var wdweControllers = angular.module('wdweApp.controllers', []);

wdweControllers.controller('HomeCtrl', function HomeCtrl($scope,$http,Pusher,TagFeed) {

	$scope.message = 'Hello Angular !';
	$scope.feed = [];
    $scope.items = [];

    Pusher.subscribe('tag_feed', 'feed_update', function (item) {

		console.log(item);
		$scope.items = item;

        // an item was updated. find it in our list and update it.
        /*for (var i = 0; i < $scope.items.length; i++) {
            if ($scope.items[i].id === item.id) {
                $scope.items[i] = item;
                break;
            }
        }*/
    });

    var retrieveItems = function () {
        console.log('getting feed');
        TagFeed.query(function (response) {
		    $scope.feed = response;
	    });
    };

    $scope.updateItem = function () {
        console.log('updating item');
        $http({
			method: 'GET',
			url: '/api/insta_feed_update/'
		}).then(function successCallback(response) {
				// this callback will be called asynchronously
				// when the response is available
			console.log(response);
		}, function errorCallback(response) {
			// called asynchronously if an error occurs
			// or server returns response with an error status.
			console.log(response);
		});
    };

    // load the items
    retrieveItems();

});