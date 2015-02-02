app.controller('DashboardController', ['$q', '$scope', '$interval', 'AuthService', 'Restangular',
                              function ($q,   $scope,   $interval,   AuthService,   Restangular) {

        Restangular.setDefaultHeaders({token: AuthService.getToken()});

        var resources = Restangular.all('resources');
        resources.getList().then(function (response) {
            $scope.services = response;
        });

        var provisionedResources = Restangular.all('provisioned_resources');
        provisionedResources.getList().then(function (response) {
            $scope.instances = response;
        });

        $scope.provision = function (resource) {
            resource.post().then(function (response) {
                    provisionedResources.getList().then(function (response) {
                            $scope.instances = response;
                        }
                    )
                }
            )
            ;
        }

        $scope.deprovision = function (provisionedResource) {

//            provisionedResource.remove().then(function () {
//                var index = $scope.instances.indexOf(provisionedResource);
//                if (index > -1) $scope.instances.splice(index, 1);
//            });
            provisionedResource.patch({state:'deleting'}).then(function () {
                var index = $scope.instances.indexOf(provisionedResource);
                if (index > -1) $scope.instances[index].state='deleting';
            });
        }

        $interval(function () {
            var provisionedResources = Restangular.all('provisioned_resources');
            provisionedResources.getList().then(function (response) {
                $scope.instances = response;
            });
        }, 60000);
    }]);
