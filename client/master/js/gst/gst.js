var GST = angular.module('gst', ['angle']);

GST.run(['$log', function ($log) {
    return $log.log('I\'m a line from gst.js');
}]);
