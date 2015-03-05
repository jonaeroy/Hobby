angular.module('app.controllers').controller('phonebookNewCtrl',function($scope,$location,$modal,$log,PhonebookSvc){
    "use strict"

    $scope.phonebooks={};
    

    // $scope.create = function(){
    // 	PhonebookSvc.create($scope.phonebooks)
    // 	    .success(function(data, status){
    // 		console.log(dat.items);
    // 	    })
    // 	    .error(function(data,status){
		
    // 	    })
    // };

    //pagination starts here:

    $scope.max_size = 5;
    $scope.total_items = 0;
    $scope.current_page = 1;
    $scope.items_per_page = 8;

    //view
    $scope.view = function(key,size){
	var modalInstance = $modal.open({
	    templateUrl: 'ng/templates/bnlds/view.html',
	    controller: 'PhonebookDetailsCtrl',
	    size: size,
	    resolve: {
	    key: function (){
		return key;
	    }
	    }
	});
	modalInstance.result.then(function (bnlds_list){
	}, function () {
	    $log.info('modal dismissed at: ' + new Date());
	});	
    };

    //list
    
    $scope.phonebooks_list = [];
    $scope.sliced_phonebooks_list
    $scope.list_all = function (){
	$scope.loading = true;
	PhonebookSvc.list_all()
	.success(function (data){
	    $scope.loading = false;
	    $scope.phonebooks_list = data.items;
	    $scope.total_items = data.items.length;
	    
	})
    }
    







});

// angular.module('app.controllers').controller('phonebookCtrl', function($scope,PhonebookSvc){

//     $scope.phonebooks_items = [];
//     PhonebookSvc.list()
//     .success(function(data, status){
// 	$scope.phonebooks_items = data.items;
//     })
//     .error(function(data, status)){
// 	alert("Error Occured!");
//     }
// });


