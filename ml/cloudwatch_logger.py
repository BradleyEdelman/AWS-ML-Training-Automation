import logging
import os
import sys
import time

import boto3
import watchtower
import yaml  # type: ignore

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

AWS_REGION = config["aws"]["region"]
PROJECT = config.get("project", "default-project")
MODEL = config["training"]["model"]
LOG_GROUP = "/aws/ml-training"
TIMESTAMP = int(time.time())
STREAM_NAME = f"{PROJECT}_{MODEL}_{TIMESTAMP}"


def setup_logger():
    logger_obj = logging.getLogger("CloudWatchLogger")
    logger_obj.setLevel(logging.INFO)

    if not logger_obj.handlers:
        cw_handler = watchtower.CloudWatchLogHandler(
            log_group=LOG_GROUP,
            stream_name=STREAM_NAME,
            boto3_session=boto3.Session(region_name=AWS_REGION),
        )
        logger_obj.addHandler(cw_handler)

    # Write metadata for export script
    os.makedirs("runtime_spot/logs", exist_ok=True)
    with open("runtime_spot/logs/last_log_info.txt", "w") as f:
        f.write(f"{LOG_GROUP}\n{STREAM_NAME}\n{PROJECT}\n")

    def logger_fn(msg):
        logger_obj.info(msg)

    return logger_fn


# Redirect stdout and stderr to CloudWatch, and also print to console (real-time checking and later debugging)
def redirect_stdout_to_logger(logger_fn):
    original_stdout_write = sys.stdout.write
    original_stderr_write = sys.stderr.write

    def tee_stdout(text):
        original_stdout_write(text)
        text = text.strip()
        if text:
            logger_fn(text)

    def tee_stderr(text):
        original_stderr_write(text)
        text = text.strip()
        if text:
            logger_fn(text)

    sys.stdout.write = tee_stdout
    sys.stderr.write = tee_stderr
