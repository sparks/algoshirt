angular.module('algoshirt', [
	'ngResource',
])

.config(function($routeProvider, $locationProvider) {
	$routeProvider.when('/', {
		templateUrl: '/templates/subscriber-form.html',
		controller: SubscriberFormCtrl
	});

	$routeProvider.when('/subscribers/new', {
		templateUrl: '/templates/subscriber-form.html',
		controller: SubscriberFormCtrl
	});

	$routeProvider.when('/subscribers/:id/edit', {
		templateUrl: '/templates/subscriber-form.html',
		controller: SubscriberCtrl
	});

	$routeProvider.when('/subscribers/:id', {
		templateUrl: '/templates/subscriber.html',
		controller: SubscriberCtrl
	});

	$routeProvider.when('/subscribers', {
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
		'/api/subscribers/:id',
		{ id: '@id' },
		{}
	);

	return SubscriberResource;
});

function SubscriberFormCtrl($scope, $location, $routeParams, SubscriberResource) {

	if ('id' in $routeParams) {
		$scope.subscriber = SubscriberResource.get(
			{'id' : $routeParams.id},
			function(result) {},
			function(e) {
				console.log(e);
			}
		);
		$scope.action = "Save";
	} else {
		$scope.subscriber = {}
		$scope.action = "Subscribe";
	}

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

	$scope.edit = function(sub) {
		$location.path('/subscribers/'+sub.id+'/edit');
	}

	$scope.refresh();
}

function OrderCtrl($scope, $location, $http) {

	$scope.noQuote = true;

	$scope.prepare = function() {
		$http.post('/api/order', {"action": "prepare"}).
		success(function(data) {
			$scope.prepareResp = data;
		}).
		error(function(e) {
			console.log(e);
		});
	};

	$scope.quote = function() {
		$http.post('/api/order', {"action": "quote"}).
		success(function(data) {
			$scope.quoteResp = data;
			$scope.noQuote = false;
		}).
		error(function(e) {
			$scope.noQuote = true;
			console.log(e);
		});
	};

	$scope.place = function() {
		$http.post('/api/order', {"action": "place", "args": $scope.quoteResp}).
		success(function(data) {
			$scope.placeResp = data;
		}).
		error(function(e) {
			$scope.response = e;
		});
	};

}

