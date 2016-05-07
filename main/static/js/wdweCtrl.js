var wdweControllers = angular.module('wdweApp.controllers', []);

wdweControllers.controller('HomeCtrl', function HomeCtrl($scope,Pusher,TagFeed) {

	$scope.message = 'Hello Angular !';

    $scope.items = [];

    Pusher.subscribe('items', 'updated', function (item) {
        // an item was updated. find it in our list and update it.
        for (var i = 0; i < $scope.items.length; i++) {
            if ($scope.items[i].id === item.id) {
                $scope.items[i] = item;
                break;
            }
        }
    });

    var retrieveItems = function () {
        // get a list of items from the api located at '/api/items'
        console.log('getting items');
        TagFeed.query(function (response) {
		    $scope.items = response;
	    });
    };

    $scope.updateItem = function (item) {
        console.log('updating item');
        /*$scope.items.$update(
			{ id:$scope.items.pk }, $scope.items
		);*/
    };

    // load the items
    retrieveItems();

});