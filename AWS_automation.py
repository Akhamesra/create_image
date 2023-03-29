import boto3
import datetime
import os
ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

def get_ami(key,value):
  mod_key = 'tag:'+key
  filters =[{'Name':mod_key ,'Values':[value]}]
  info = ec2_client.describe_instances(Filters=filters)
  print(info['Reservations'][0]['Instances'][0]['ImageId'])

def check_ref_id(refid):
  if refid.startswith('INFRA-'):
    return True
  elif refid.startswith('DEVOPS-'):
    return True
  else:
    return False
  
def create_ami(key,value):
  # image_name = input('Enter Name to give to AMI : ')
  # refid = input('Enter REF_ID : ')
  image_name =  os.getenv("Image_name")
  refid = os.getenv("REF_ID")

  if not check_ref_id(refid):
    print('REF_ID format is incorrect')
    return
  
  mod_key = 'tag:'+key
  filters =[{'Name':mod_key,'Values':[value]}]
  instances = ec2_resource.instances.filter(Filters=filters)

  for instance in instances:
    instance_id = instance.id
  
  date = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M")
  
  response = ec2_client.create_image(InstanceId=instance_id,
                                     Name = image_name,
                                     NoReboot =  True,
                                     TagSpecifications=[{
                                          'ResourceType' : 'image',
                                          'Tags': [
                                              {
                                                  'Key': 'Name',
                                                  'Value': image_name
                                              },
                                              {
                                                  'Key': 'Instance_name',
                                                  'Value': value
                                              },
                                              {
                                                  'Key': 'Date',
                                                  'Value': str(date)
                                              },                                              
                                              {
                                                  'Key': 'REF_ID',
                                                  'Value': refid
                                              },
                                          ]
                                      },
                                  ])
  print('Image created')


# get_ami('Name','web2')
create_ami('Name',os.getenv("EC2_Name"))
