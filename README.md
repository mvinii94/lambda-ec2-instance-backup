# Lambda EC2 Instance backup

A serverless solution to backup your EC2 Instances regestering automated AMIs.

## Getting Started

This project contains two files:

CloudFormation SAM template (template.yaml)

Lambda Function (index.py)

The Lambda function will register Amazon Machine Images (AMI) from all EC2 instances in running state AND with the tag "backup" set as "yes" each hour. If you want to change the period of backup generation you can change the lines:

```yaml
Events:
  Cron:
    Type: Schedule
    Properties:
      Schedule: rate(1 day)
```

Available Rate Expressions: [ScheduleEvents](http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#RateExpressions)

### Prerequisites

* **S3 Bucket** - *To upload the index.py file zipped.* 

* **AWS CLI Installed** - *To deploy the SAM CloudFormation template.* - [How to Install AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)

### Deploying the lambda serverless application

* Clone this repository;

* Upload the lambda code zipped to an S3 Bucket of your preference in the desired region (should be the same where you are going to deploy the serverless solution);

* Run the following command providing the bucket name and the S3 key name toof your file:

```
aws cloudformation deploy --template-file template.yaml --stack-name lambda-ec2-instance-backup --region us-east-1 --capabilities CAPABILITY_NAMED_IAM --parameter-overrides Bucket=<MyBucketName> FileKey=lambda-ec2-instance-backup.zip
```

## Managing

IMPORTANT: This Serverless solution creates AMIs on your beahlf, if you want to control the AMIs rentention created by this solution, please see the solution [lambda-ec2-deregister-amis](https://github.com/mvinii94/lambda-ec2-deregister-old-amis)

## Authors

* **Marcus Ramos** - [GitHub](https://github.com/mvinii94/)
