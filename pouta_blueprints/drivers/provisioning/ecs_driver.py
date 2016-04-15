import boto3

from pouta_blueprints.drivers.provisioning import base_driver


class ECSDriver(base_driver.ProvisioningDriverBase):
    def get_configuration(self):
        from pouta_blueprints.drivers.provisioning.ecs_driver_config import CONFIG
        return CONFIG

    def do_update_connectivity(self, token, instance_id):
        pass

    def do_provision(self, token, instance_id):
        self.logger.debug("do_provision %s" % instance_id)
        client = boto3.client('ecs')

        log_uploader = self.create_prov_log_uploader(token, instance_id, log_type='provisioning')
        log_uploader.info("Provisioning Docker based instance (%s)\n" % instance_id)

        pbclient = ap.get_pb_client(token, self.config['INTERNAL_API_BASE_URL'], ssl_verify=False)

        log_uploader = self.create_prov_log_uploader(token, instance_id, log_type='provisioning')

        instance = pbclient.get_instance_description(instance_id)

        # fetch config
        blueprint = pbclient.get_blueprint_description(instance['blueprint_id'])
        blueprint_config = blueprint['config']

        response = client.run_task(
            cluster='default',
            taskDefinition='taskDefinition:revision',
            count=1,
            startedBy=instance_id
        )

        tasks = response.get('tasks', [])
        if not tasks:
            raise RuntimeError('No containers started for the task')
        elif len(tasks) > 1:
            raise RuntimeError('More than one container started for the task')

        task = tasks[0]

        host_port = task.get('containers', {}).get('networkBindings', {}).get('hostPort')
        if not host_port:
            raise RuntimeError('Unable to get host port')
        container_instance_arn = task.get('containerInstanceArn')

        instance_data = {
            'name': 'raw',
            'access': '%s:%s' % (self.config['PUBLIC_IPV4'], host_port),
            'ecs_host_arn': container_instance_arn
        }


    def do_deprovision(self, token, instance_id):
        pass

    def do_housekeep(self, token):
        pass
