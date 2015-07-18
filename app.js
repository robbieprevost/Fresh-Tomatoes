// set up our app to handle our data and various functions
var myApp = angular.module('myApp', ['ngRoute', 'ngSanitize']).config(function($sceDelegateProvider) {
    $sceDelegateProvider.resourceUrlWhitelist([
        // Allow same origin resource loads.
        'self',
        // Allow loading from our assets domain.  Notice the difference between * and **.
        'https://www.youtube.com/**']);
}).filter('trustAsResourceUrl', ['$sce', function($sce) {
    return function(val) {
        return $sce.trustAsResourceUrl(val);
    };
}]);

// set up our controller for our app
var myController = myApp.controller('myController', function($scope, $rootScope, $http, $sce, $timeout ){
    // store the dat we need for our app to function
    $scope.data = {
        featured: {},
        listNames: ["numbers","A","B","C","D","E","F","G",
                "H","I","J-K","L","M","N-O","P","Q-R",
                "S","T","U-W","X-Z"],
        featureSelected: {},
        listSelected: ['',[],[]],
        selected: '',
        selectedURL : '',
        itemSelected: [],
        selectedTimeout: null,
        loading: false
    };
    // store our functions to do things in our app
    $scope.workers = {
        // initialize our app
        init: function(){
            // get the featured movie lists from the server
            $http.get('/featured')
                .success(function(response) {
                    $scope.data.featured = response.featured;
                    //console.log($scope.data.featured);
                });
        },
        // get a list of movies from the server
        list: function(name){
            var link = '/_' + name;
            $http.get(link)
                .success(function(response) {
                    $scope.data.selected = 'list';
                    $scope.data.listSelected[0] = name;
                    for(var i = 0; i < response[1].length;i++){
                        $scope.data.listSelected[1][i] = {
                            index : i,
                            value : response[1][i]
                        };
                        var value = response[2][i];
                        if(value.indexOf("&amp;") != -1){
                            value = value.replace("&amp;", "&");
                        }
                        if(value.indexOf("&quot;") != -1){
                            value = value.replace('&quot;', '"');
                        }
                        $scope.data.listSelected[2][i] = {
                            index : i,
                            value : value
                        };
                    }
                    //console.log($scope.data.listSelected);
                });
        },
        // handle a click on a featured movie
        featuredClick: function(film){
            $scope.data.selected = 'featured';
            $scope.data.featureSelected = film;
            var index = $scope.data.featureSelected.trailer_youtube_url.indexOf('=') + 1;
            var url = $scope.data.featureSelected.trailer_youtube_url.substring(index);
            $scope.data.featureSelected.trailer_youtube_url = $sce.trustAsHtml('<iframe class="trailer" src="https://www.youtube.com/embed/' + url + '" frameborder="0" allowfullscreen></iframe>');
        },
        // handle a click on an exit button
        exitFeatured: function(){
            $scope.data.selected = '';
            $scope.data.featureSelected = {};
        },
        exitList: function(){
            $scope.data.selected = '';
            $scope.data.listSelected = ['',[],[]];
        },
        exitItem: function(){
            $scope.data.selected = '';
            $scope.data.itemSelected = [];
            $scope.data.loading = false;
        },
        // handle a click on a list item
        listItemClick: function(item){
            $scope.data.itemSelected[0] = $scope.data.listSelected[0];
            $scope.data.itemSelected[1] = item.index;
            $scope.data.itemSelected[2] = $scope.data.listSelected[1][item.index].value;
            $scope.data.itemSelected[3] = $scope.data.listSelected[2][item.index].value;
            //console.log($scope.data.itemSelected);
            $scope.data.selected = 'item';
            $scope.data.listSelected = ['',[],[]];
            // define our query for the list item information
            var url = '/selected?list=' + $scope.data.itemSelected[0] +
                      'QQQindex=' + $scope.data.itemSelected[1] +
                      'QQQurl=' + $scope.data.itemSelected[2] +
                      'QQQtitle=' + $scope.data.itemSelected[3];
            $scope.data.loading = true;
            // send our request to the server
            $http.get(url)
                .success(function(response) {
                    // use the response to structure our request for more data
                    $scope.data.selectedURL = '/' + response + '.json';
                    // set a timeout to allow the server to gather our data
                    $scope.data.selectedTimeout = $timeout(function(){
                        // request our additional data
                        $http.get($scope.data.selectedURL)
                            .success(function(response) {
                                $scope.data.loading = false;
                                //console.log(response);
                                $scope.data.itemSelected[4] = response.image;
                                $scope.data.itemSelected[5] = $sce.trustAsHtml('<iframe class="trailer" src="https://www.youtube.com/embed/' + response.videoLink + '" frameborder="0" allowfullscreen></iframe>');
                            });
                        $scope.data.selectedTimeout = null;
                    },5000);
                });
        }
    }
});