import boto3
import datetime
import os
from flask import *
from flask.cli import AppGroup
import click

app = Flask(__name__)  
ami_cli = AppGroup('ami_cli')
app.cli.add_command(ami_cli)

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

@ami_cli.command('get_ami')
@click.option('-n','--name', prompt = 'Enter Name of EC2 instance')
def get_ami(value):
  # mod_key = 'tag:'+'Name'
  filters =[{'Name':'tag:Name' ,'Values':[value]}]
  info = ec2_client.describe_instances(Filters=filters)
  print(info['Reservations'][0]['Instances'][0]['ImageId'])

def check_ref_id(refid):
  if refid.startswith('INFRA-'):
    return True
  elif refid.startswith('DEVOPS-'):
    return True
  else:
    return False

@ami_cli.command('create_ami')
@click.option('-r', '--refid', prompt = 'Enter REF_ID')
@click.option('-n','--ec2_name')
@click.option('-i', '--ec2_ip')
def create_ami(refid,ec2_name=None,ec2_ip=None):
  # image_name = input('Enter Name to give to AMI : ')
  # refid = input('Enter REF_ID : ')
  # image_name =  os.getenv("Image_name")
  # refid = os.getenv("REF_ID")
  if not check_ref_id(refid):
    print('REF_ID format is incorrect')
    return
  
  # mod_key = 'tag:'+'key'
  if ec2_name:
    filters =[{'Name':'tag:Name','Values':[ec2_name]}]

  elif ec2_ip:
    filters = [{'Name': 'network-interface.addresses.private-ip-address', 'Values': [ec2_ip]}]

  instances = ec2_resource.instances.filter(Filters=filters)

  for instance in instances:
    for tag in instance.tags:
        if tag['Key'] == 'Name':
          instance_name = tag['Value']
    instance_id = instance.id
  
  image_name = instance_name+'-BACKUP'
  date = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M")
  response = ec2_client.create_image(InstanceId=instance_id,
                                     Name = image_name,
                                     NoReboot =  True,
                                     TagSpecifications=[{
                                          'ResourceType' : 'image',
                                          'Tags': [ {'Key': 'Name',         'Value': image_name},
                                                    {'Key': 'Instance_name','Value': instance_name},
                                                    {'Key': 'Date',         'Value': str(date)},                                              
                                                    {'Key': 'REF_ID',       'Value': refid},
                                                  ]
                                      },
                                  ])
  print('Image created')



# get_ami('Name','web2')
# create_ami('Name',os.getenv("EC2_Name"))
