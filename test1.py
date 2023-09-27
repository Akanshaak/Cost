import boto3
import datetime

def get_rds_info():
    session = boto3.Session(profile_name='default')
    rds_client = session.client('rds',region_name='us-east-1')
    ec2_client = session.client('ec2', region_name='us-east-1') 
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    rds_info = []
    start_date = datetime.date.today() - datetime.timedelta(days=40) 
    end_date = datetime.date.today()
    cost_explorer_client = session.client('ce', region_name='us-east-1')  

    for region in regions:
        rds_client = session.client('rds', region_name=region)
        response = rds_client.describe_db_instances()
        # print(response)
        for instance in response['DBInstances']:
            instance_id = instance['DBInstanceIdentifier']
            instance_status = instance['DBInstanceStatus']
            instance_class = instance['DBInstanceClass']
            endpoint = instance['Endpoint']['Address']
            allocated_storage = instance['AllocatedStorage']
            cost_response = cost_explorer_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d'),
                },
                Granularity='DAILY',
                Metrics=['UnblendedCost'],
            )
            cost_amount = cost_response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
            rds_info.append({
                'Region': region,
                'InstanceID': instance_id,
                'Status': instance_status,
                'InstanceClass': instance_class,
                'Endpoint': endpoint,
                'AllocatedStorage': allocated_storage,
                'Cost': cost_amount,
            })

    return rds_info

if __name__ == '__main__':
    rds_info = get_rds_info()
    for instance in rds_info:
        print(f"Region: {instance['Region']}")
        print(f"Instance ID: {instance['InstanceID']}")
        print(f"Status: {instance['Status']}")
        print(f"Instance Class: {instance['InstanceClass']}")
        print(f"Endpoint: {instance['Endpoint']}")
        print(f"Allocated Storage: {instance['AllocatedStorage']} GB")
        print(f"Cost: ${instance['Cost']}")
        print()

# import boto3
# import datetime
# import concurrent.futures

# def get_cost_for_region(region, start_date, end_date, cost_explorer_client):
#     cost_response = cost_explorer_client.get_cost_and_usage(
#         TimePeriod={
#             'Start': start_date.strftime('%Y-%m-%d'),
#             'End': end_date.strftime('%Y-%m-%d'),
#         },
#         Granularity='DAILY',
#         Metrics=['UnblendedCost'],
#     )
#     return region, cost_response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']

# def get_rds_info():
#     session = boto3.Session(profile_name='default')
#     ec2_client = session.client('ec2', region_name='us-east-1')
#     regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
#     start_date = datetime.date.today() - datetime.timedelta(days=40)
#     end_date = datetime.date.today()
#     cost_explorer_client = session.client('ce', region_name='us-east-1')

#     def get_rds_info_for_region(region):
#         rds_client = session.client('rds', region_name=region)
#         response = rds_client.describe_db_instances()
#         cost_amount = get_cost_for_region(region, start_date, end_date, cost_explorer_client)[1]

#         rds_info = []
#         for instance in response.get('DBInstances', []):
#             rds_info.append({
#                 'Region': region,
#                 'InstanceID': instance['DBInstanceIdentifier'],
#                 'Status': instance['DBInstanceStatus'],
#                 'InstanceClass': instance['DBInstanceClass'],
#                 'Endpoint': instance['Endpoint']['Address'],
#                 'AllocatedStorage': instance['AllocatedStorage'],
#                 'Cost': cost_amount,
#             })
#         return rds_info

#     with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#         rds_info = executor.map(get_rds_info_for_region, regions)

#     rds_info = [info for sublist in rds_info for info in sublist]

#     return rds_info

# if __name__ == '__main__':
#     rds_info = get_rds_info()
#     for instance in rds_info:
#         print(f"Region: {instance['Region']}")
#         print(f"Instance ID: {instance['InstanceID']}")
#         print(f"Status: {instance['Status']}")
#         print(f"Instance Class: {instance['InstanceClass']}")
#         print(f"Endpoint: {instance['Endpoint']}")
#         print(f"Allocated Storage: {instance['AllocatedStorage']} GB")
#         print(f"Cost: ${instance['Cost']}")
#         print()
