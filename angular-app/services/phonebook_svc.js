angular.module('app.services').
    service('PhonebooksSvc', function($http){
	
    this.list_all=function(){
	return $http.get('/api/phonebooks');
    }
    this.create = function(){
	return $http.post('/api/phonebooks', params);
    }
	

});
