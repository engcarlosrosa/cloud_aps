import boto3
from botocore.exceptions import ClientError
from flask import Flask, Response, request, render_template, jsonify
import requests
from flask_restful import Api
import time
import threading


ec2 = boto3.client('ec2')
keypairJson = ec2.describe_key_pairs()
key_pair_name = "Carlos"
response = ec2.describe_vpcs()
security_group = "APS"
ec2_2 = boto3.resource('ec2', region_name="us-east-1")

app = Flask(__name__, static_url_path="")
api = Api(app)

ip_list = []
for instance in ec2_2.instances.all():
	if instance.tags is None:
		continue
	for tag in instance.tags:
		if tag['Key'] == 'Owner' and tag['Value']=='Carlos' and instance.state['Name']=='running':
			ip_list.append(instance.public_ip_address)

	



#print('http://'+str(ip_list[1])+':5000/healthcheck/')
def request_0():
	try:
		while (True):
			r = requests.get('http://'+str(ip_list[0])+':5000/healthcheck/')
			print('http://'+str(ip_list[0])+':5000/healthcheck/')
			print(r.text)
			
	except:
		instances = ec2_2.create_instances(
			ImageId='ami-0ac019f4fcb7cb7e6', 
			MinCount=1, 
			MaxCount=3,
			KeyName=key_pair_name,
			InstanceType="t2.micro",
			SecurityGroups=[security_group] ,
			UserData='''#!/bin/sh
						git clone https://github.com/engcarlosrosa/cloud_aps
						sudo apt install python3-pip
						pip3 install flask
						
						cd cloud_aps
						python webserver.py ''',
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
	

def request_1():
		try:
			while (True):
				r = requests.get('http://'+str(ip_list[1])+':5000/healthcheck/')
				print('http://'+str(ip_list[1])+':5000/healthcheck/')
				print(r.text)
				
		except:
			instances = ec2_2.create_instances(
				ImageId='ami-0ac019f4fcb7cb7e6', 
				MinCount=1, 
				MaxCount=3,
				KeyName=key_pair_name,
				InstanceType="t2.micro",
				SecurityGroups=[security_group] ,
				UserData='''#!/bin/sh
							git clone https://github.com/engcarlosrosa/cloud_aps
							sudo apt install python3-pip
							pip3 install flask
							
							cd cloud_aps
							python webserver.py ''',
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

def request_2():
		try:
			while (True):
				r = requests.get('http://'+str(ip_list[2])+':5000/healthcheck/')
				print('http://'+str(ip_list[2])+':5000/healthcheck/')
				print(r.text)
				
		except:
			instances = ec2_2.create_instances(
				ImageId='ami-0ac019f4fcb7cb7e6', 
				MinCount=1, 
				MaxCount=3,
				KeyName=key_pair_name,
				InstanceType="t2.micro",
				SecurityGroups=[security_group] ,
				UserData='''#!/bin/sh
							git clone https://github.com/engcarlosrosa/cloud_aps
							sudo apt install python3-pip
							pip3 install flask
							
							cd cloud_aps
							python webserver.py ''',
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





#thread_0 = threading.Timer(0,0, request_0)
#thread_1 = threading.Timer(0,0, request_1)
#thread_2 = threading.Timer(0,0, request_2)

#thread_0.start()
#thread_1.start()
#thread_2.start()
request_0()
request_1()
request_2()


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

    