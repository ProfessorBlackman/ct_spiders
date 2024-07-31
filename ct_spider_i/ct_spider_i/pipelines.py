import uuid

import boto3
from io import BytesIO
from PIL import Image
import requests
from botocore.exceptions import NoCredentialsError
from decouple import config
from requests_aws4auth import AWS4Auth
import os
from algoliasearch.search_client import SearchClient

from ct_spider_i.kafka import send_to_kafka
from ct_spider_i.kafka.producer import ImageData


class S3Pipeline:
    def __init__(self):
        # AWS S3 setup
        self.s3_bucket_name = config('AWS_S3_BUCKET_NAME')
        self.s3 = boto3.client('s3', region_name=config('AWS_REGION'))

        self.region = config('AWS_REGION')
        self.aws_auth = AWS4Auth(config('AWS_ACCESS_KEY'), config('AWS_SECRET_KEY'), self.region, 'es')

    def process_item(self, item, spider):
        try:
            for image_link in item['image_links']:
                # Download the image
                response = requests.get(image_link)
                image = Image.open(BytesIO(response.content))
                image_format = image.format.lower()

                # Generate a unique filename
                filename = f"{os.path.basename(image_link)}"

                # Upload to S3
                self.s3.upload_fileobj(
                    BytesIO(response.content),
                    self.s3_bucket_name,
                    filename,
                    ExtraArgs={'ContentType': f'image/{image_format}'}
                )

        except NoCredentialsError:
            spider.logger.error("Credentials not available")
        except Exception as e:
            spider.logger.error(f"Error uploading image to S3 or storing metadata: {str(e)}")

        return item


class AlgoliaPipeline:
    def __init__(self):
        # Initialize the Algolia client
        self.client = SearchClient.create(
            config('ALGOLIA_APP_ID'),
            config('ALGOLIA_SEARCH_KEY')
        )
        self.index = self.client.init_index(config('SEARCH_INDEX'))

    def process_item(self, item, spider):
        # Prepare the data to be sent to Algolia
        record = {
            'image_id': uuid.uuid5(uuid.NAMESPACE_DNS, item['post_headlines'][0]),
            'image_links': item['image_links'],
            'post_links': item['post_links'],
            'image_source_alt': item['image_source_alt'],
            'post_headlines': item['post_headlines'],
            'source': item['source'],
            'append_source': item['append_source']
        }

        send_to_kafka('ct_spider_i', ImageData(**record))

        # Add the record to the Algolia index
        self.index.save_object(record)

        return item
