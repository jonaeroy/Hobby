angular.module('app.controllers').controller('phonebookCtrl',function($scope,PhonebookSvc){
    "use strict"

    $scope.phonebooks={};
    $scope.create = function(){
	PhonebookSvc.create($scope.phonebooks)
	    .success(function(data, status){
		console.log(dat.items);
	    })
	    .error(function(data,status){
		
	    })
    };


});

angular.module('app.controllers').controller('phonebookCtrl', function($scope,PhonebookSvc){

    $scope.phonebooks_items = [];
    PhonebookSvc.list()
    .success(function(data, status){
	$scope.phonebooks_items = data.items;
    })
    .error(function(data, status)){
	alert("Error Occured!");
    }
});
