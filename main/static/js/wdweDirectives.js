/**
 * Created by gugs on 5/5/16.
 */
var wdweDirectives = angular.module('wdweApp.directives', []);

wdweDirectives.directive('instaPostDetails', function() {
  return {
	  restrict: 'E',
	  templateUrl: 'static/views/directives/insta-post-details.html',
	  scope: {
		  instapost: '=dataset',
	  },
	  /*link: function(scope,element,attrs){

		  console.log(scope.instapost);

	  }*/
  };
});