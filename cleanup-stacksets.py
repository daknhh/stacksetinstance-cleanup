import boto3
import datetime
import argparse
import time
from tqdm import tqdm

def delete_stack_set_instances(accountid,client,retain):
    allStack_sets = client.list_stack_sets(
        Status='ACTIVE'
    )
    if retain == 'yes':
        RetainStacks = True
    else:
        RetainStacks = False


    for stackset in tqdm(allStack_sets['Summaries'],desc="Progress"):
        instances = client.list_stack_instances(
        StackSetName=stackset['StackSetName'],
        StackInstanceAccount=accountid)
        
        if instances['Summaries'] != []:
            print(f"\n\nDeleting StackSetInstances {stackset['StackSetName']}")
            for instance in instances['Summaries']:
                print(f"🌍 {instance['Region']}")
                response = client.delete_stack_instances(
                StackSetName=stackset['StackSetName'],
                Accounts=[
                    accountid,
                ],
                Regions=[
                    instance['Region'],
                ],
                RetainStacks=RetainStacks
                )
                operationid = response['OperationId']
                finished = False
                while not finished:
                    time.sleep(5)
                    status = client.describe_stack_set_operation(StackSetName=stackset['StackSetName'], OperationId=operationid)["StackSetOperation"]["Status"]
                    if status in 'RUNNING':
                        finished = False
                    else:
                        finished = True
                if status not in 'SUCCEEDED':
                    print(f"💀 StackSet Operation failed with Status: {status}")         
                print(f"✅ - All StackSet Instances for {stackset['StackSetName']} has been deleted.") 

parser = argparse.ArgumentParser()
parser.add_argument('--account', help='--account define target accountid')
parser.add_argument('--profile', help='--profile enter valid AWSPROFILE')
parser.add_argument('--retain', help='--retain choose if you want to retain the stack or not yes / no')
args = parser.parse_args()
session = boto3.Session(profile_name=args.profile)
cloudformation_client = session.client('cloudformation')
print(f'\n\n💣 Delete StackSet Instances for one AWS Account 💀\n')
print(f'👨🏻‍💻 - linkedin.com/in/daknhh 🔀 daknhh\n\n ')
print(f"""⚙️  SETTINGS: \n Profile: {args.profile} \n Account: {args.account} \n Retain: {args.retain} \n""")
delete_stack_set_instances(args.account,cloudformation_client, args.retain)

generationTime = datetime.datetime.now()
print(f"""\n🗓: {generationTime}""")

