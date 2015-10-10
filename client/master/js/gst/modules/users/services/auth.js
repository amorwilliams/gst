/**=========================================================
 * Module: auth.js
 * Services to share auth functions
 =========================================================*/

GST.factory('Auth', ['$cookies', '$http', '$state', '$q', 'APP_URLS', function($cookies, $http, $state, $q, urls){
    /**
     * @name Authentication
     * @desc The Factory to be returned
     */
    var Auth = {
        register: register,
        login: login,
        logout: logout,
        getAuthenticatedAccount : getAuthenticatedAccount,
        isAuthenticated: isAuthenticated,
        setAuthenticatedAccount: setAuthenticatedAccount,
        unAuthenticate: unAuthenticate
    };

    return Auth;

    ////////////////////

    /**
     * @name register
     * @desc Try to register a new user
     * @param {string} username The username entered by the user
     * @param {string} password The password entered by the user
     * @param {string} email The email entered by the user
     * @returns {Promise}
     * @memberOf thinkster.authentication.services.Authentication
     */
    function register(email, password, username){
        var def = $q.defer();
        $http
            .post(urls.auth + 'api/v1/users/', {
                username:username,
                password:password,
                email:email
            })
            .then(onRegisterSuccess, onRegisterError);

        return def.promise;

        /**
         * @name onRegisterSuccess
         * @desc Log the new user in
         */
        function onRegisterSuccess(data, status, headers, config) {
            Auth.login(email, password);
            def.resolve(data);
        }

        /**
         * @name onRegisterError
         * @desc Log "Epic failure!" to the console
         */
        function onRegisterError(data, status, headers, config) {
            console.error('Epic failure!');
            def.reject('Server Request Error');
        }
    }

    /**
     * @name login
     * @desc Try to log in with email `email` and password `password`
     * @param {string} email The email entered by the user
     * @param {string} password The password entered by the user
     * @returns {Promise}
     * @memberOf thinkster.authentication.services.Authentication
     */
    function login(email, password) {
        //var def = $q.defer();

        var promise = $http.post(urls.auth + '/api/v1/auth/', {
                email: email,
                password: password
            });

        promise.then(onLoginSuccess, onLoginError);

        return promise;
        //return def.promise;

        /**
         * @name onLoginSuccess
         * @desc Set the authenticated account and redirect to index
         */
        function onLoginSuccess(data, status, headers, config) {
            Auth.setAuthenticatedAccount(data.data);
            //def.resolve(data);
        }

        /**
         * @name onLoginError
         * @desc Log "Epic failure!" to the console
         */
        function onLoginError(data, status, headers, config) {
            console.error('Epic failure!');
            //def.reject('Server Request Error');
        }
    }

    /**
     * @name logout
     * @desc Try to log the user out
     * @returns {Promise}
     * @memberOf thinkster.authentication.services.Authentication
     */
    function logout() {
        return $http
            .post('/api/v1/auth/logout/')
            .then(onLogoutSuccess, onLogoutError);

        /**
         * @name logoutSuccessFn
         * @desc Unauthenticate and redirect to index with page reload
         */
        function onLogoutSuccess(data, status, headers, config) {
            Authentication.unauthenticate();

            window.location = '/';
        }

        /**
         * @name onLogoutError
         * @desc Log "Epic failure!" to the console
         */
        function onLogoutError(data, status, headers, config) {
            console.error('Epic failure!');
        }
    }

    /**
     * @name getAuthenticatedAccount
     * @desc Return the currently authenticated account
     * @returns {object|undefined} Account if authenticated, else `undefined`
     * @memberOf thinkster.authentication.services.Authentication
     */
    function getAuthenticatedAccount() {
        if (!$cookies.getObject('authenticatedAccount')) {
            return;
        }

        return $cookies.getObject('authenticatedAccount');
    }

    /**
     * @name isAuthenticated
     * @desc Check if the current user is authenticated
     * @returns {boolean} True is user is authenticated, else false.
     * @memberOf thinkster.authentication.services.Authentication
     */
    function isAuthenticated() {
        return !!$cookies.getObject('authenticatedAccount');
    }

    /**
     * @name setAuthenticatedAccount
     * @desc Stringify the account object and store it in a cookie
     * @param {Object} user The account object to be stored
     * @returns {undefined}
     * @memberOf thinkster.authentication.services.Authentication
     */
    function setAuthenticatedAccount(account) {
        $cookies.putObject('authenticatedAccount', account);
    }

    /**
     * @name unAuthenticate
     * @desc Delete the cookie where the user object is stored
     * @returns {undefined}
     * @memberOf thinkster.authentication.services.Authentication
     */
    function unAuthenticate() {
        $cookies.remove('authenticatedAccount');
    }
}]);