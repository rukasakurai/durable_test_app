import azure.functions as func
import azure.durable_functions as df
import logging

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new("HelloOrchestrator")
    
    # Get the forwarded host and protocol if available
    forwarded_host = req.headers.get('X-Forwarded-Host')
    forwarded_proto = req.headers.get('X-Forwarded-Proto', 'https')
    
    # If Forwarded header exists (RFC 7239), parse it to get the host
    forwarded_header = req.headers.get('Forwarded')
    if forwarded_header and not forwarded_host:
        for part in forwarded_header.split(';'):
            if part.strip().lower().startswith('host='):
                # Extract host from format like 'host=example.com'
                forwarded_host = part.strip()[5:].strip('"')
                break
    
    # Use the forwarded headers to create a custom base URL if available
    if forwarded_host:
        base_url = f"{forwarded_proto}://{forwarded_host}"
        logging.info(f"Using custom base URL from headers: {base_url}")
        return client.create_check_status_response(req, instance_id, base_url)
    else:
        # Fall back to default behavior
        logging.info("No forwarding headers found, using default URL")
        return client.create_check_status_response(req, instance_id)
