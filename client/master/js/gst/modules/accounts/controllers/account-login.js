/**=========================================================
 * Module: account-login.js
 * GST for login api
 =========================================================*/

GST.controller('LoginFormController', ['$scope', '$state', 'Auth', function($scope, $state, Auth) {

    // bind here all data from the form
    $scope.account = {};
    // place the message if something goes wrong
    $scope.authMsg = '';

    $scope.login = function() {
        $scope.authMsg = '';

        if($scope.loginForm.$valid) {

            Auth
                .login($scope.account.email, $scope.account.password)
                .then(function(response) {
                    // assumes if ok, response is an object with some data, if not, a string with error
                    // customize according to your api
                    if ( !response.data.username ) {
                        $scope.authMsg = 'Incorrect credentials.';
                    }else{
                        $state.go('game.role');
                    }
                }, function(error) {
                    $scope.authMsg = error;
                });
        }
        else {
            // set as dirty if the user click directly to login so we show the validation messages
            $scope.loginForm.account_email.$dirty = true;
            $scope.loginForm.account_password.$dirty = true;
        }
    };

}]);
