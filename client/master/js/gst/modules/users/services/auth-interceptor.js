

GST.factory('authInterceptor', ['$rootScope', '$q', '$window', function($rootScope, $q, $window){
    return {
        request: function(request) {
            request.headers = request.headers || {};
            if($window.sessionStorage.token){
                request.headers.Authorization = 'Bearer' + $window.sessionStorage.token;
            }
            return request;
        },
        response: function(response) {
            if(response.status == 401 || response.status == 403) {
                $location.path('/login');
            }
            return $q.reject(response)
        }
    };
}]);

//GST.config(['$httpProvider', function($httpProvider){
//    $httpProvider.interceptors.push('authInterceptor');
//}]);