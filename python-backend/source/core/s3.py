import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from source.core.config import config
import logging
import io

logger = logging.getLogger(__name__)


client = boto3.client(
    "s3",
    region_name=config.default_region,
    aws_access_key_id=config.aws_access_key_id,
    aws_secret_access_key=config.aws_secret_access_key
)

def generate_presigned_url(client_method:str, method_parameters:dict, expires_in:int
    ) -> str:
    """
    Generate a presigned Amazon S3 URL that can be used to perform an action.
    :param client_method: The name of the client method that the URL performs.
    :param method_parameters: The parameters of the specified client method.
    :param expires_in: The number of seconds the presigned URL is valid for.
    :return: The presigned URL.
    """
    try:
        url = client.generate_presigned_url(
            ClientMethod=client_method,
            Params=method_parameters,
            ExpiresIn=expires_in
        )
        logger.info("Got presigned URL: %s", url)
    except ClientError:
        logger.exception(
            "Couldn't get a presigned URL for client method '%s'.", client_method)
        raise
    return url


def upload_image(pil_image, bucket, key, FORMAT='PNG'):
    in_mem_file = io.BytesIO()
    pil_image.save(in_mem_file, format=FORMAT)
    in_mem_file.seek(0)

    try:
        client.upload_fileobj(
            in_mem_file,  # This is what i am trying to upload
            bucket,
            key,
            ExtraArgs={"ACL": "public-read"},
        )
    except ClientError:
        logger.exception(
            f"Couldn't get a presigned URL for client method")
        raise