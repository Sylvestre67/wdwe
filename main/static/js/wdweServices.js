/**
 * Created by gugs on 5/5/16.
 */

angular.module('wdweApp.services', ['ngResource'])
	.factory('InstaPost',function($resource){
		return $resource('/api/insta_post_information/:postId/')
	})
	.factory('TagFeed', function($resource) {
		return $resource('/api/tag_feed/:id/',null,
			{
				'update' : {method:'PATCH'}
			}
		)
	});