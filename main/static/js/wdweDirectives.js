/**
 * Created by gugs on 5/5/16.
 */
var wdweDirectives = angular.module('wdweApp.directives', []);

wdweDirectives.directive('instaPostDetails', ['InstaPost', function(InstaPost) {
  return {
	  restrict: 'E',
	  templateUrl: 'static/views/directives/insta-post-details.html',
	  scope: {
		  instapost: '=dataset',
	  },
	  link: function(scope,element,attrs){

		  scope.insta_post_info = {};

		  scope.$watch('instapost', function(newValue,oldValue){
			  newValue.id ?
				  InstaPost.get({postId:newValue.id},function(post_data){
					  scope.insta_post_info = post_data;
				  })
				  : scope.insta_post_info = {status : 'no_data'};
		  })

	  }
  };
}]
);