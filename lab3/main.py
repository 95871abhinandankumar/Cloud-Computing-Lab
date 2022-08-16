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


print("Connecting to Autoscalling Service")

client = boto3.client('autoscaling')

print("Creating launch configuration")

response = client.create_launch_configuration(
    LaunchConfigurationName='MY-Launch-Config',
    ImageId='ami-0c2b8ca1dad447f8a',
    InstanceType='t2.micro',
    KeyName='cs351key',
    SecurityGroups=[
        'sg-01f0d539aca59ca98',
    ],
    UserData=startup_script)

print("Creating auto-scaling group")

response = client.create_auto_scaling_group(
    AutoScalingGroupName='My-Auto-Scaling-Group',
    LaunchConfigurationName='MY-Launch-Config',
    AvailabilityZones=['us-east-1a', 'us-east-1b','us-east-1c', 'us-east-1d', 'us-east-1e', 'us-east-1f'],
    MinSize=1,
    MaxSize=2)

print("Creating auto-scaling policies")

scale_up_policy= client.put_scaling_policy(
    AutoScalingGroupName='My-Auto-Scaling-Group',
    PolicyName='scale_up',
    AdjustmentType='ChangeInCapacity',
    ScalingAdjustment=1,
    Cooldown=180)


scale_down_policy = client.put_scaling_policy(
    AutoScalingGroupName='My-Auto-Scaling-Group',
    PolicyName='scale_down',
    AdjustmentType='ChangeInCapacity',
    ScalingAdjustment=-1,
    Cooldown=180)

print("Connecting to CloudWatch")

cloudwatch = boto3.client('cloudwatch')

#alarm_dimensions = "AutoScalingGroupName": 'My-Auto-Scaling-Group'

print("Creating scale-up alarm")

response = cloudwatch.put_metric_alarm(
    AlarmName='up_alarm',
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Statistic='Average',
    ComparisonOperator='GreaterThanThreshold',
    Threshold=70,
    Period=60,
    EvaluationPeriods=2,
    AlarmActions=[scale_up_policy['PolicyARN']])

print("Creating scale-down alarm")

response = cloudwatch.put_metric_alarm(
    AlarmName='down_alarm',
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Statistic='Average',
    ComparisonOperator='LessThanThreshold',
    Threshold=40,
    Period=60,
    EvaluationPeriods=2,
    AlarmActions=[scale_down_policy['PolicyARN']])

print("Done")
