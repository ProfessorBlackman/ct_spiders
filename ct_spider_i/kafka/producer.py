from decouple import config
from kafka import KafkaProducer
import json


# Define a class to store image data
class ImageData:
    def __init__(self, image_id: str, image_links: list, post_links: list, image_source_alt: list, post_headlines: list,
                 append_source: bool, source: str):
        self.image_id = image_id
        self.image_links = image_links
        self.post_links = post_links
        self.image_source_alt = image_source_alt
        self.post_headlines = post_headlines
        self.append_source = append_source
        self.source = source

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(data: dict):
        image_id = data['image_id']
        image_links = data['image_links']
        post_links = data['post_links']
        image_source_alt = data['image_source_alt']
        post_headlines = data['post_headlines']
        append_source = data['append_source']
        source = data['source']
        return ImageData(image_id, image_links, post_links, image_source_alt, post_headlines, append_source, source)


# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[config("KAFKA_BOOTSTRAP_SERVER")],  # Replace with your Kafka broker address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize data to JSON
)


# Define a function to send data to Kafka
def send_to_kafka(topic, data: ImageData):
    producer.send(topic, data.to_json())
    producer.flush()  # Ensure all messages are sent
