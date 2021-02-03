import praw
import boto3
import datetime

client_ident = '9LjBYEs4MIv0Tw'
client_skey = '2IqklztP5SJCZVcc8wn72hxUMa0'
client_agent = 'scrapetest'

def handler(event, context):
    dynamodb = boto3.client('dynamodb', region_name='us-west-2')

    try:
        latest_submission = dynamodb.query(
            TableName = 'r-aws-scrape',
            IndexName = 'created_unix-index',
            ExpressionAttributeValues = {
                ':sr': {
                    'S': 'aws'
                }
            },
            KeyConditionExpression = 'subreddit = :sr',
            ProjectionExpression = 'created_unix',
            Limit = 1,
            ScanIndexForward = False
        )['Items'][0]['created_unix']['N']
    except Exception:
        latest_submission = '0.0'

    print(f'Latest Post: {latest_submission}')

    reddit = praw.Reddit(
        client_id = client_ident,
        client_secret = client_skey,
        user_agent = client_agent
    )

    aws_subreddit = reddit.subreddit('aws')
    submissions = aws_subreddit.new(limit=None)

    for submission in submissions:
        if submission.created_utc >= float(latest_submission):
            submission_data = {
                'created_unix': {'N': str(submission.created_utc)},
                'created_utc': {'S': str(datetime.datetime.fromtimestamp(submission.created_utc))},
                'id': {'S': submission.id},
                'num_comments': {'N': str(submission.num_comments)},
                'score': {'N': str(submission.score)},
                'title': {'S': submission.title},
                'link': {'S': submission.url},
                'subreddit': {'S': 'aws'}
            }

            try:
                submission_data['author'] = {'S': submission.author.name}
            except Exception:
                submission_data['author'] = {'S': '[deleted]'}

            if len(submission.selftext) > 0:
                submission_data['body'] = {'S': submission.selftext}

            try:
                dynamodb.put_item(
                    TableName = 'r-aws-scrape',
                    Item = submission_data,
                )
            except Exception as e:
                print(e)

    return