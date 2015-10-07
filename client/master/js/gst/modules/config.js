/**=========================================================
 * Module: config.js
 * App routes and resources configuration
 =========================================================*/

GST.config(['$stateProvider', '$locationProvider', '$urlRouterProvider', 'RouteHelpersProvider',
    function ($stateProvider, $locationProvider, $urlRouterProvider, helper) {
        'use strict';

        // default route
        $urlRouterProvider.otherwise('/app/singleview');

        //
        // Application Routes
        // -----------------------------------
        $stateProvider
            //
            // Account Routes
            // -----------------------------------
            .state('account', {
                url: '/account',
                templateUrl: 'app/pages/page.html',
                resolve: helper.resolveFor('modernizr', 'icons'),
                controller: ["$rootScope", function ($rootScope) {
                    $rootScope.app.layout.isBoxed = false;
                }]
            })
            .state('account.login', {
                url: '^/login',
                title: "Login",
                templateUrl: 'app/pages/login.html'
            })
            .state('account.register', {
                url: '^/register',
                title: "Register",
                templateUrl: 'app/pages/register.html'
            })
            .state('page.lock', {
                url: '/lock',
                title: "Lock",
                templateUrl: 'app/pages/lock.html'
            })
            //
            // Game Management Routes
            // -----------------------------------
            .state('game', {
                url: '/game',
                abstract: true,
                templateUrl: helper.basepath('app.html'),
                controller: 'AppController',
                resolve: helper.resolveFor('modernizr', 'icons')
            })
            .state('game.role', {
                url: '/role',
                title: 'Role Data View',
                templateUrl: helper.basepath('game-role.html')
            })
            .state('game.mail', {
                url: '/mail',
                title: 'Send Mail View',
                templateUrl: helper.basepath('game-mail.html')
            })
            //
            // Single Page Routes
            // -----------------------------------
            .state('page', {
                url: '/page',
                templateUrl: 'app/pages/page.html',
                resolve: helper.resolveFor('modernizr', 'icons'),
                controller: ["$rootScope", function ($rootScope) {
                    $rootScope.app.layout.isBoxed = false;
                }]
            })
            .state('page.recover', {
                url: '/recover',
                title: "Recover",
                templateUrl: 'app/pages/recover.html'
            })
            .state('page.404', {
                url: '/404',
                title: "Not Found",
                templateUrl: 'app/pages/404.html'
            })
            //
            // CUSTOM RESOLVES
            //   Add your own resolves properties
            //   following this object extend
            //   method
            // -----------------------------------
            // .state('app.someroute', {
            //   url: '/some_url',
            //   templateUrl: 'path_to_template.html',
            //   controller: 'someController',
            //   resolve: angular.extend(
            //     helper.resolveFor(), {
            //     // YOUR RESOLVES GO HERE
            //     }
            //   )
            // })
        ;


    }])
;
