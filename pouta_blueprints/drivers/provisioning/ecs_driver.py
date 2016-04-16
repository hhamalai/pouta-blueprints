import boto3
import json
from pouta_blueprints.client import PBClient
from pouta_blueprints.drivers.provisioning import base_driver


class ECSDriver(base_driver.ProvisioningDriverBase):
    def get_configuration(self):
        from pouta_blueprints.drivers.provisioning.ecs_driver_config import CONFIG
        return CONFIG

    def do_update_connectivity(self, token, instance_id):
        pass

    def do_provision(self, token, instance_id):
        self.logger.debug("do_provision %s" % instance_id)
        ecs_client = boto3.client('ecs')
        ec2_client = boto3.client('ec2')

        log_uploader = self.create_prov_log_uploader(token, instance_id, log_type='provisioning')
        log_uploader.info("Provisioning Docker based instance (%s)\n" % instance_id)

        log_uploader = self.create_prov_log_uploader(token, instance_id, log_type='provisioning')

        pbclient = PBClient(token, self.config['INTERNAL_API_BASE_URL'], ssl_verify=False)
        instance = pbclient.get_instance_description(instance_id)

        # fetch config
        blueprint = pbclient.get_blueprint_description(instance['blueprint_id'])
        blueprint_config = blueprint['config']

        response = ecs_client.run_task(
            cluster='default',
            taskDefinition=blueprint_config['task_definition'],
            count=1,
            startedBy=instance_id
        )

        tasks = response.get('tasks', [])
        if not tasks:
            log_uploader.info('No containers started for the instance (%s)\n' % instance_id)
            raise RuntimeError('No containers started for the task')
        elif len(tasks) > 1:
            log_uploader.info('Multiple containers started for the instance (%s)\n' % instance_id)
            raise RuntimeError('More than one container started for the task')

        task = tasks[0]

        host_port = task.get('containers', {}).get('networkBindings', {}).get('hostPort')
        if not host_port:
            log_uploader.info('Task did not return host port')
            raise RuntimeError('Unable to get host port')

        container_instance_arn = task.get('containerInstanceArn')
        container_instances = ecs_client.describe_container_instances(containerInstances=[container_instance_arn]).get('containerInstances')
        if not container_instances:
            log_uploader.info('No containers instances running with arn %s' % container_instance_arn)
            raise RuntimeError('No container instances running')

        container_instance = container_instances[0]
        container_instance_id = container_instance.split('/')[-1]
        instance_response = ec2_client.describe_instances(InstanceIds=[container_instance_id])
        reservations = instance_response.get('Reservations')
        if not reservations:
            log_uploader.info('No instances running with id %s' % container_instance_id)
            raise RuntimeError('No instances running with id %s' % container_instance_id)

        reservation = reservations[0]
        instances = reservation.get('Instances')
        if not instances:
            raise RuntimeError('No instances running with given id %s' % instance_id)
        instance = instances[0]
        instance_private_ip = instance.get('PrivateIpAddress')
        if not instance_private_ip:
            raise RuntimeError('No private IP for the instance with id %s' % instance_id)

        instance_data = {
            'name': 'raw',
            'access': '%s:%s' % (self.config['PUBLIC_IPV4'], host_port),
            'ecs_host_arn': container_instance_arn,
            'ecs_host_ip': instance_private_ip
        }

        pbclient.do_instance_patch(
            instance_id,
            {
                'instance_data': json.dumps(instance_data),
            }
        )

    def do_deprovision(self, token, instance_id):
        pass

    def do_housekeep(self, token):
        pass
