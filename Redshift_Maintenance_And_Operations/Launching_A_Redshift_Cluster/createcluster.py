import boto3

redshift = boto3.client('redshift')

response = redshift.create_cluster(
    ClusterIdentifier = 'boto3-cluster',
    ClusterType = 'single-node',
    NodeType = 'dc2.large',
    MasterUsername = 'john',
    MasterUserPassword = 'Strongpass1'
)

print(response)