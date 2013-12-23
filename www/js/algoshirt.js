angular.module('algoshirt', [
	'ngResource',
	'ui.bootstrap',
	'angularMoment'
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
})

.factory('RenderResource', function ($resource) {
	var RenderResource = $resource(
		'/api/renders/:id',
		{ id: '@id' },
		{
			'new': { method:'POST' }
		}
	);

	return RenderResource;
})

.factory('OrderResource', function ($resource) {
	var OrderResource = $resource(
		'/api/orders/:id',
		{ id: '@id' },
		{
			'quote': { method: 'POST', params: { action: 'quote' }},
			'place': { method: 'POST', params: { action: 'place' }}
		}
	);

	return OrderResource;
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

function OrderCtrl($scope, $location, $http, RenderResource, OrderResource) {

	$scope.refresh = function() {
		$scope.renders = RenderResource.query(
			function(o) {},
			function(e) {
				console.log(e);
			}
		);

		$scope.orders = OrderResource.query(
			function(o) {},
			function(e) {
				console.log(e);
			}
		);
	};

	$scope.render = function() {
		RenderResource.new({},
			function(res) {
				$scope.refresh();
			},
			function(e) {
				console.log(e);
			}
		);
	};

	$scope.buildOrder = function(render) {
		if (render.status != "done") {
			console.log("Render not complete yet, cannot order");
		} else {
			OrderResource.save({"render_id": render.id},
				function(result) {
					$scope.refresh();
				},
				function(e) {
					console.log(e);
				}
			);
		}
	};

	$scope.quoteOrder = function(order) {
		if (order.status != "noquote") {
			console.log("Already have quote");
		} else {
			OrderResource.quote({'id': order.id},
				function(result) {
					$scope.refresh();
				},
				function(e) {
					console.log(e);
				}
			);
		}
	};

	$scope.placeOrder = function(order) {
		if (order.status != "quote") {
			console.log("Need quote to order");
		} else {
			OrderResource.place({'id': order.id},
				function(result) {
					$scope.refresh();
				},
				function(e) {
					console.log(e);
				}
			);
		}
	};

	$scope.deleteRender = function(render) {
		RenderResource.delete({'id': render.id}, //Dunno why I can't just put render here? Something with Cherrypy and DELETE
			function() {
				$scope.refresh();
			},
			function(e) {
				console.log(e);
			}
		);
	};

	$scope.deleteOrder = function(order) {
		OrderResource.delete({'id': order.id}, //Dunno why I can't just put render here? Something with Cherrypy and DELETE
			function() {
				$scope.refresh();
			},
			function(e) {
				console.log(e);
			}
		);
	};

	$scope.alerts = [];

	$scope.addAlert = function() {
		$scope.alerts.push({msg: "Another alert!"});
	};

	$scope.closeAlert = function(index) {
		$scope.alerts.splice(index, 1);
	};

	$scope.refresh();
}

