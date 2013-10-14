angular.module('algoshirt', [
	'ngResource'
])

.config(function($routeProvider, $locationProvider) {
	$routeProvider.when('/', {
		templateUrl: '/templates/subscribe.html',
		controller: SubscribeCtrl
	});

	$routeProvider.when('/subscribe', {
		templateUrl: '/templates/subscribe.html',
		controller: SubscribeCtrl
	});

	$routeProvider.when('/subscribers', {
		templateUrl: '/templates/subscriber.html',
		controller: SubscriberCtrl
	});

	$routeProvider.when('/subscribers/:id', {
		templateUrl: '/templates/subscriber.html',
		controller: SubscriberCtrl
	});

	$routeProvider.when('/order', {
		templateUrl: '/templates/order.html',
		controller: OrderCtrl
	});

	// configure html5 to get links working on jsfiddle
	// $locationProvider.html5Mode(true);
})

.factory('SubscriberResource', function ($resource) {
	var SubscriberResource = $resource(
		'api/subscribers/:id',
		{ id: '@id' },
		{}
	);

	return SubscriberResource;
});

function SubscribeCtrl($scope, $location, SubscriberResource) {

	$scope.subscriber = {}

	$scope.subscribe = function() {
		SubscriberResource.save($scope.subscriber,
			function(result) {
				$location.path('/subscribers');
			},
			function(e) {
				console.log(e);
			}
		);
	}

}

function SubscriberCtrl($scope, $location, $routeParams, SubscriberResource) {

	$scope.refresh = function() {
		if ('id' in $routeParams) {
			console.log("yup");
			$scope.subscribers = [SubscriberResource.get(
				{'id' : $routeParams.id},
				function(result) {},
				function(e) {
					console.log(e);
				}
			)];
		} else {
			$scope.subscribers = SubscriberResource.query(
				function(subs) {},
				function(e) {
					console.log(e);
				}
			);
		}
	};

	$scope.delete = function(sub) {
		SubscriberResource.delete({'id': sub.id} ,
			function() {
				if ('id' in $routeParams) $location.path('/subscribers');
				$scope.refresh();
			},
			function(e) {
				console.log(e);
			}
		);
	};

	$scope.refresh();
}

function OrderCtrl($scope, $location) {

}

