import boto3
import time

ebsClient = boto3.client('elasticbeanstalk')

version_label = 'v2'
application_name = 'testing'
environment_name = 'testingEnv'

print("Hello")


def createNewVersion():
    try:
        ebsClient.create_application_version(
            ApplicationName=application_name,
            VersionLabel='v2',
            Description='testing',
            SourceBundle={
                'S3Bucket': 'cs351-assignment2',
                'S3Key': 'app.zip'
            },
            AutoCreateApplication=True,
            Process=False
        )
        print('application Created')
    except Exception as e:
        print('some error has occured: ', e)


def createEnvironment():
    try:
        ebsClient.create_environment(
            ApplicationName=application_name,
            EnvironmentName=environment_name,
            Description='testing',
            CNAMEPrefix='testing',
            Tier={
                'Name': 'WebServer',
                'Type': 'Standard',
            },
            VersionLabel='v2',
            SolutionStackName='64bit Amazon Linux 2 v3.3.5 running PHP 8.0',
            OptionSettings=[
                {
                    'Namespace': 'aws:autoscaling:launchconfiguration',
                    'OptionName': 'IamInstanceProfile',
                    'Value': 'aws-elasticbeanstalk-ec2-role'
                },
            ],
        )
        print('Environment Created')
    except Exception as e:
        print('some error has occured: ', e)


createNewVersion()
time.sleep(20)
createEnvironment()
