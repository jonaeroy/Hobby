angular.module('app.services').
    service('BnldsSvc', function($http) {

	this.list_all = function(){
            return $http.get('/api/bnlds');
	}

	this.create = function(params){
            return $http.post('/api/bnlds', params);
	}

	this.get = function(key){
            return $http.get('/api/bnlds:' + key);
	}

	this.update = function(params){
            return $http.post('/api/bnlds/:' + params.key.urlsafe, params);
	}

	this.delete = function(key){
            return $http.delete('/api/bnlds/:' + key);
	}
	this.get_user = function(){
	    return $http.get('/api/get_user');
	}

	this.get_uploadurl = function(){
	    return $http.get('/api/get_uploadurl');
	}

	this.upload_file = function(url, file){
	    console.log(file);
	    var fd = new FormData();
	    if(file) fd.append('file', file);
	    console.log(fd);


	    return $http.post(url, fd,{
 	        transformRequest: angular.identity,
		headers: {'Content-Type': undefined}
	    });
	}

    });
