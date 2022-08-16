import boto3


startup_script = '''#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd
cd /var/www/html
rm index.html
wget https://cs351-assignment2.s3.amazonaws.com/index.html
'''


def createInstance() -> str:
    try:
        print('creating instance')
        ec2 = boto3.resource('ec2')
        #print("hello")
        response = ec2.create_instances(
            ImageId='ami-0c2b8ca1dad447f8a',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='cs351key',
            SecurityGroupIds=['sg-01f0d539aca59ca98'],
            UserData=startup_script)
        instance = response[0]
        print('Instance created.. waiting to be in running state')
        instance.wait_until_running()
        print('Instance in running.')
        instance.load()
        print('public dns address: ', get_name(instance))
    except Exception as e:
        print(e)


def get_name(inst):
    client = boto3.client('ec2')
    response = client.describe_instances(InstanceIds=[inst.instance_id])
    dns_address = response['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicDnsName']
    return dns_address


createInstance()
