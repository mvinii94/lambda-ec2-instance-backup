import boto3
from botocore.exceptions import ClientError
import datetime
import logging

ec2 = boto3.resource('ec2')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

###
# This function generates an AMI of all instances which is running with the TAG key equals to "backup" and its value as "yes"
###

instance_iterator = ec2.instances.filter(
    Filters=[
        {'Name': 'instance-state-name', 'Values': ['running']},
        {'Name': 'tag:backup', 'Values': ['yes']}
    ]
)

def lambda_handler(event, context):

    for instance in instance_iterator:
        current_datetime = datetime.datetime.now()
        full_date_stamp = current_datetime.strftime("%Y-%m-%d-%Hh%M-%S")
        logger.info('-----------------------------------------------------------')
        logger.info('Registering ' + instance.id + ' AMI')
        try:
            ami_id = instance.create_image(
                Name='{0}-backup-{1}'.format(instance.id,full_date_stamp),
                Description='[DO NOT DEREGISTER] - AMI created by Lambda function as automated backup {0}'.format(instance.id),
                NoReboot=True,
            )
            logger.info('AMI CREATED, ID: %s' % ami_id)
            ami_id.create_tags(
                Tags=[
                    {
                        'Key': 'CreationDate',
                        'Value': '{0}'.format(current_datetime)
                    },
                    {
                        'Key': 'backup',
                        'Value': 'lambda'
                    },
                    {
                        'Key': 'Name',
                        'Value': '[DO NOT DEREGISTER] - {0}-backup-{1}'.format(instance.id,full_date_stamp)
                    },
                ]
            )
            logger.info('-----------------------------------------------------------')
            return True
        except ClientError as e:
            error = e.response['Error']['Code'] == 'EntityAlreadyExists'
            logger.info('Unexpected error: ' + error)
