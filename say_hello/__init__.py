import logging

def main(input: dict) -> str:
    name = input.get("name", "")
    instance_id = input.get("instance_id", "unknown")
    try:
        logging.info(f"Activity started. Instance ID: {instance_id}, Name: {name}")
        return f"Hello, {name}!"
    except Exception as e:
        logging.error(f"Exception in activity. Instance ID: {instance_id}. Error: {e}")
        raise
