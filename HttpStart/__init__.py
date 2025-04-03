import azure.functions as func
import azure.durable_functions as df
import logging
import json

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    logging.info("HttpStart function received a request")
    logging.info(f"Request URL: {req.url}")
    logging.info(f"Request method: {req.method}")
    logging.info(f"Request headers: {dict(req.headers)}")
    
    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new("HelloOrchestrator")
    logging.info(f"Started orchestration with ID: {instance_id}")
    
    # Get the forwarded host and protocol if available
    forwarded_host = req.headers.get('X-Forwarded-Host')
    forwarded_host = "example.com"
    logging.info(f"X-Forwarded-Host header: {forwarded_host}")
    
    forwarded_proto = req.headers.get('X-Forwarded-Proto', 'https')
    logging.info(f"X-Forwarded-Proto header: {forwarded_proto}")
    
    # If Forwarded header exists (RFC 7239), parse it to get the host
    forwarded_header = req.headers.get('Forwarded')
    logging.info(f"Forwarded header: {forwarded_header}")
    
    if forwarded_header and not forwarded_host:
        logging.info("Parsing Forwarded header to extract host")
        for part in forwarded_header.split(';'):
            logging.info(f"Processing Forwarded header part: {part}")
            if part.strip().lower().startswith('host='):
                # Extract host from format like 'host=example.com'
                forwarded_host = part.strip()[5:].strip('"')
                logging.info(f"Extracted host from Forwarded header: {forwarded_host}")
                break
    
    # Create management payload dictionary
    management_payload = client.create_http_management_payload(instance_id)
    logging.info(f"Original management payload: {management_payload}")
    
    # If forwarded headers exist, modify the management URLs
    if forwarded_host:
        base_url = f"{forwarded_proto}://{forwarded_host}"
        logging.info(f"Using custom base URL: {base_url}")
        
        # Replace the host portion in each URL with our custom base URL
        modified_payload = {}
        for key, url in management_payload.items():
            # Find the position after the scheme and authority in the URL
            # This is typically after the third slash in http://authority/path
            path_start = url.find('/', url.find('//') + 2)
            if path_start != -1:
                modified_url = base_url + url[path_start:]
                modified_payload[key] = modified_url
            else:
                modified_payload[key] = url  # Keep original if we can't parse it
        
        logging.info(f"Modified management payload: {modified_payload}")
        
        # Return HTTP response with the modified payload
        return func.HttpResponse(
            body=json.dumps(modified_payload),
            headers={"Content-Type": "application/json"},
            status_code=202
        )
    else:
        # Use standard response with default URLs
        logging.info("No forwarding headers found, using default URLs")
        return client.create_check_status_response(req, instance_id)
