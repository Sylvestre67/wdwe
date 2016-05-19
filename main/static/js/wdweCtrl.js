var wdweControllers = angular.module('wdweApp.controllers', []);

wdweControllers.controller('HomeCtrl', function HomeCtrl($scope,$http,$interval,Pusher,TagFeed) {

	$scope.message = 'Bon Appetit!';
	$scope.feed = [];
	$scope.instapost = {};

    Pusher.subscribe('tag_feed', 'feed_update', function (new_media) {
		//A new images was posted -> push it to the feed!
		$scope.feed.unshift(new_media);

    });

    var retrieveFeed = function () {
        TagFeed.query(function (response) {
		    $scope.feed = response;
			console.log($scope.feed);
			$scope.instapost = response[0];
	    });
    };

	//Select randomly on of the picture on the feed.
	var randomPost = function(){
		var index = Math.floor(Math.random() * ( $scope.feed.length - 0) + 0);

		console.log($scope.feed[index]);

		$scope.instapost = $scope.feed[index];

		return $scope.feed[index];
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
	};

	$interval(updateItem, 15000);

	$interval(randomPost,5000);

    // load the items
    retrieveFeed();

});