angular.module('app.controllers').controller('newBnldsRequestCtrl', function($scope,$location,BlndsSvc){
    "use.strict"

    $scope.bnlds={};
    $scope.choices=["Yes","No","N/A"];
    $scope.create = function(){
        BlndsSvc.create($scope.bnlds)
            .success(function(data, status){
                console.log(data.items);
            })
            .error(function(data,status){

            })

        };

// $scope.loadPage = function(){
//     $location.path("newbnldsrequest");
};

});

angular.module('app.controllers').controller('BnldsListCtrl', function($scope, BnldsSvc){
    $scope.bnlds_items = [];
    BnldsSvc.list()
    .success(function(data, status){
        $scope.bnlds_items = data.items;
    })
    .error(function(data, status)){
        alert("Error Occured!");
    }
});
