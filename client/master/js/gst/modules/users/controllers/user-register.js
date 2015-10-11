/**=========================================================
 * Module: user-register.js
 * GST for register account api
 =========================================================*/

GST.controller('RegisterFormController', ['$scope', '$http', '$state', 'Auth', function($scope, $http, $state, Auth) {

    // bind here all data from the form
    $scope.account = {};
    // place the message if something goes wrong
    $scope.authMsg = '';

    $scope.register = function() {
        $scope.authMsg = '';

        if($scope.registerForm.$valid) {

            Auth
                .register(
                $scope.account.email,
                $scope.register.password,
                $scope.register.account_password_confirm)
                .then(function(response) {
                    // assumes if ok, response is an object with some data, if not, a string with error
                    // customize according to your api
                    if ( !response.account ) {
                        $scope.authMsg = response;
                    }else{
                        $state.go('app.dashboard');
                    }
                }, function(x) {
                    $scope.authMsg = 'Server Request Error';
                });
        }
        else {
            // set as dirty if the user click directly to login so we show the validation messages
            $scope.registerForm.account_email.$dirty = true;
            $scope.registerForm.account_password.$dirty = true;
            $scope.registerForm.account_agreed.$dirty = true;

        }
    };

}]);
