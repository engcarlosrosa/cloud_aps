import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')
desc_key_pair_Json = ec2.describe_key_pairs()
key_pair_name = "Carlos"
desc_vpcs = ec2.describe_vpcs()
security_group = "APS"
ec2_ = boto3.resource('ec2', region_name="us-east-1")
ip_publico_dict = {}

for instance in ec2_.instances.all():
	if instance.tags is None:
		continue
	for tag in instance.tags:
		if tag['Key'] == 'Owner' and tag['Value']=='Carlos' and instance.state['Name']=='running':
			instance.terminate()
			print('instances terminated')
			ip_publico_dict[instance.instance_id]=instance.public_ip_address
			print(ip_publico_dict[instance.instance_id])
			instance.wait_until_terminated()

for i in range(len(desc_key_pair_Json['KeyPairs'])):
	if key_pair_name in desc_key_pair_Json['KeyPairs'][i]['KeyName']:
		ec2.delete_key_pair(KeyName=key_pair_name)
		print('keypair deletada')
		key_pair = ec2.create_key_pair(KeyName=key_pair_name)
		print('keypair criada')

vpc_id = desc_vpcs.get('Vpcs', [{}])[0].get('VpcId', '')
try:
	sec_groups = ec2.describe_security_groups()
	for j in range(len(sec_groups['SecurityGroups'])):
		if security_group in sec_groups['SecurityGroups'][j]['GroupName']:
			sec_group_id = sec_groups['SecurityGroups'][j]['GroupId']

			ec2.delete_security_group(GroupId=sec_group_id)
			print('Security Group deletado')
			desc_vpcs = ec2.create_security_group(GroupName=security_group,
										  Description='APS',
										  VpcId=vpc_id)
			security_group_id = desc_vpcs['GroupId']

			data = ec2.authorize_security_group_ingress(
			GroupId=security_group_id,
			IpPermissions=[
			{'IpProtocol': 'tcp',
			 'FromPort': 5000,
			 'ToPort': 5000,
			 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
			{'IpProtocol': 'tcp',
			 'FromPort': 22,
			 'ToPort': 22,
			 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
			 {'IpProtocol': 'tcp',
			 'FromPort': 80,
			 'ToPort':80,
			 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
		])
		else:
			desc_vpcs = ec2.create_security_group(GroupName=security_group,
										  Description='APS',
										  VpcId=vpc_id)
			security_group_id = desc_vpcs['GroupId']

			data = ec2.authorize_security_group_ingress(
			GroupId=security_group_id,
			IpPermissions=[
			{'IpProtocol': 'tcp',
			 'FromPort': 5000,
			 'ToPort': 5000,
			 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
			{'IpProtocol': 'tcp',
			 'FromPort': 22,
			 'ToPort': 22,
			 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
		])

except ClientError as e:
	print(e)

output_file = open('Carlos.pem','w')
output_key_pair = str(key_pair['KeyMaterial'])
output_file.write(output_key_pair)
print('key_pair Carlos.pem saved')

instances = ec2_.create_instances(
	ImageId='ami-0ac019f4fcb7cb7e6', 
	MinCount=1, 
	MaxCount=3,
	KeyName=key_pair_name,
	InstanceType="t2.micro",
	SecurityGroups=[security_group] ,
	UserData='''#!/bin/sh/

				git clone https://github.com/engcarlosrosa/cloud_aps
				sudo apt-get update
				sudo apt install python3-pip
				pip3 install flask
				cd /cloud_aps
				python3 webserver.py ''',
	TagSpecifications=[
		{
			'ResourceType': 'instance',
			'Tags': [
				{
					'Key': 'Owner',
					'Value': 'Carlos'
				},
			]
		},
	],
)

