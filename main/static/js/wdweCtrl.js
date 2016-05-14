var wdweControllers = angular.module('wdweApp.controllers', []);

wdweControllers.controller('HomeCtrl', function HomeCtrl($scope,$http,$interval,Pusher,TagFeed) {

	$scope.message = 'Bon Appetit!';
	$scope.feed = [];
	$scope.instapost = {'init': 'init'};

    Pusher.subscribe('tag_feed', 'feed_update', function (new_media) {
		//A new images was posted -> push it to the feed!
		$scope.feed.unshift(new_media);
    });

    var retrieveFeed = function () {
        TagFeed.query(function (response) {
		    $scope.feed = response;
	    });
    };

    var updateItem = function () {
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

	 $scope.updateInstaPost = function(media){
		 $scope.instapost = media;
		 //console.log($scope.instapost);
	};

	//$interval(updateItem, 15000);

    // load the items
    retrieveFeed();

});