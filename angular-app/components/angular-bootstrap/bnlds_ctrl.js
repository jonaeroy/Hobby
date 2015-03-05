angular.module('app.controllers').controller('newBnldsRequestCtrl', function($scope, $location, $modal, $log, BnldsSvc){
    "use.strict"

    $scope.bnlds={};
    $scope.items = ["dsd"];

    //list pagination variables
    $scope.max_size = 5;
    $scope.total_items = 0;
    $scope.current_page = 1;
    $scope.items_per_page = 8;
    
    
    //view

    $scope.view = function(key, size){
	var modalInstance = $modal.open({
	    templateUrl: '/ng/templates/bnlds/view.html',
	    controller: 'BnldDetailsCtrl',
	    size: size,
	    resolve: {
		key: function () {
		    return key;
		}
	    }
	});

	modalInstance.result.then(function (bnlds_list) {
	}, function () {
	    $log.info('Modal dismissed at: ' + new Date());
	});
    };

    //list
    $scope.bnlds_list = [];
    $scope.sliced_bnlds_list
    $scope.list_all = function(){
	$scope.loading =  true;
	BnldsSvc.list_all()
	    .success(function(data, status){
		$scope.loading = false;
		$scope.bnlds_list = data.items;
		$scope.total_items = data.items.length;
		$scope.pageChange();
		console.log($scope.total_items);
	    })
	    .error(function(data, status){
		alert('Error Accessing BNLDS Request Lists!');
	    });
    };

    //edit
    $scope.edit = function(key){
	var modalInstance = $modal.open({
	    templateUrl: '/ng/templates/bnlds/bnldform.html',
	    controller: 'BnldEditCtrl',
	    size: 'md',
	    resolve: {
		key: function () {
		    return key;
		}
	    }
	});

	modalInstance.result.then(function (bnlds_list) {
	    $scope.bnlds_list = bnlds_list;
	    $scope.list_all();
	}, function () {
	    $log.info('Modal dismissed at: ' + new Date());
	    $scope.list_all();
	});

    };

    //delete
    $scope.delete = function(key){
	BnldsSvc.delete(key)
	    .success(function(data, status){
		if(status==200){
		    alert('Request was succesfully deleted!');
		}
		$scope.list_all();
	    })
	    .error(function(data, status){
		
	    });
    };

    //request list pagination 
    $scope.pageChange = function(){
	var start = ($scope.current_page-1)*$scope.items_per_page;
	var end = start + $scope.items_per_page;
	$scope.sliced_bnlds_list = $scope.bnlds_list.slice(start, end);
	$log.log(start + " : " + end);
    };

    /*create request form modal*/
    $scope.open = function (size) {
	var modalInstance = $modal.open({
	    templateUrl: '/ng/templates/bnlds/bnldform.html',
	    controller: 'BnldFormCtrl',
	    size: size,
	    resolve: {
		items: function () {
		    return $scope.items;
		}
	    }
	});

	modalInstance.result.then(function (bnlds_list) {
	    $scope.bnlds_list = bnlds_list;
	    $scope.list_all();
	}, function () {
	    $log.info('Modal dismissed at: ' + new Date());
	    $scope.list_all();
	});
    };

    //ngfilereder sample here

});


angular.module('app.controllers').controller('BnldFormCtrl', function ($scope, $modalInstance, $log, $upload, items, BnldsSvc) {

    $scope.bnlds = {};
    $scope.choices=["Yes","No","N/A"];
    $scope.bnlds_list = [];
    $scope.mode = 'add';
    //ng file reader variables
    $scope.bnld_file = {};
    $scope.blob_key = null;
    $scope.file_name = "";

    /*******upload file *******/
    $scope.$watch('files', function () {
        $scope.upload($scope.files);
    });

    $scope.upload = function (files) {
        if (files && files.length) {
	    $scope.bnld_file = files[0];
	    /*
              for (var i = 0; i < files.length; i++) {
              var file = files[i];
              $upload.upload({
              url: 'https://angular-file-upload-cors-srv.appspot.com/upload',
              file: file
              }).progress(function (evt) {
              var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
              console.log('progress: ' + progressPercentage + '% ' +
              evt.config.file.name);
              }).success(function (data, status, headers, config) {
	      $log.log(data);
	      $scope.bnld_file = JSON.stringify(data);
	      $scope.file_name = config.file.name;
              /*console.log('file ' + config.file.name + 'uploaded. Response: ' +
              JSON.stringify(data));
              });
              }*/
        }
    };

    /*********end of upload function************/

    /***get currently logged in user****/
    BnldsSvc.get_user()
	.success(function(data, status){
	    $scope.bnlds['Buyer_or_BAA_Name'] = data;
	    $log.log(data);
	})
	.error(function(data, status){
	});

    BnldsSvc.get_uploadurl()
	.success(function(data, status){
	    $scope.upload_url = data;
	})
	.error(function(){
	});


    //click ok event
    $scope.ok = function () {
	//do create new request service here
	//$scope.bnlds['Please_attach_the_New_Line_Submission_Sheet_to_this_Form_Below'] = $scope.files;
	BnldsSvc.get_uploadurl()
	    .success(function(url, status){
		BnldsSvc.upload_file(url, $scope.bnld_file)
		    .success(function(blobkey){
			$log.log('blobkey: ' + blobkey);
			$scope.bnlds['Please_attach_the_New_Line_Submission_Sheet_to_this_Form_Below'] = blobkey;
		    })
		    .error();
	    })
	    .error(function(data, status){
		
	    });

	
	BnldsSvc.create($scope.bnlds)
            .success(function(data, status){
                console.log(data);
            })
            .error(function(data,status){

            });

	BnldsSvc.list_all()
	    .success(function(data, status){
		$scope.bnlds_list = data.items;
		console.log(data.items);
	    })
	    .error(function(data, status){
		alert('Error Accessing BNLDS Request Lists!');
	    });
	
	$modalInstance.close($scope.bnlds_list);
    };

    $scope.cancel = function () {
	$modalInstance.dismiss('cancel');
    };
});


angular.module('app.controllers').controller('BnldDetailsCtrl', function ($scope, $modalInstance, key, BnldsSvc) {
    $scope.bnld_details = {};

    BnldsSvc.get(key)
        .success(function(data, status){
	    $scope.bnlds_details = data;
            console.log(data);
        })
        .error(function(data,status){

        });

    
    
    $scope.cancel = function () {
	$modalInstance.dismiss('cancel');
    };
});


angular.module('app.controllers').controller('BnldEditCtrl', function ($scope, $modalInstance, $log, key, BnldsSvc) {
    $scope.bnlds = {};
    $scope.choices = ["Yes","No","N/A"];
    $scope.bnlds_list = [];
    $scope.mode = 'edit';
    
    BnldsSvc.get(key)
        .success(function(data, status){
	    $scope.bnlds = data;
            console.log(data);
        })
        .error(function(data,status){

        });
    
    $scope.ok = function () {
	$log.log($scope.bnlds);
	BnldsSvc.update($scope.bnlds)
	    .success(function(data,status){
		
	    })
	    .error(function(data, status){

	    });

	BnldsSvc.list_all()
	    .success(function(data, status){
		$scope.bnlds_list = data.items;
		console.log(data.items);
	    })
	    .error(function(data, status){
		alert('Error Accessing BNLDS Request Lists!');
	    });

	$modalInstance.close(key);
    };

    $scope.cancel = function () {
	$modalInstance.dismiss('cancel');
    };
});
