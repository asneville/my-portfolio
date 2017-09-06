
import boto3
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')
    try:
        topic = sns.Topic('arn:aws:sns:eu-west-2:848101116957:deplotPortfolioTopic')
        portfolio_bucket = s3.Bucket('asneville.virtualise-me.com')
        build_bucket = s3.Bucket('asneville-portfolio-build')

        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

        with zipfile.ZipFile(portfolio_zip) as myzip:
         for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj,nm,
              ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
        print "Deploy Complete!"
        topic.publish(Subject="Portfolio deployment", Message="Portfolio deployment for asneville complete")
    except:
        topic.publish(Subject="Portfolio deployment failed", Message="Portfolio deployment for asneville failed")
        raise
    return "done"
