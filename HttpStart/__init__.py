import azure.functions as func
import azure.durable_functions as df

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new("HelloOrchestrator")
    # Extract the correct domain using X-Forwarded-Host and X-Forwarded-Proto headers
    host = req.headers.get("X-Forwarded-Host", req.host)
    proto = req.headers.get("X-Forwarded-Proto", "http")
    base_url = f"{proto}://{host}"
    
    # Generate consistent management URLs using the extracted domain
    status_url = f"{base_url}/api/status/{instance_id}"
    terminate_url = f"{base_url}/api/terminate/{instance_id}"
    raise_event_url = f"{base_url}/api/raiseevent/{instance_id}"
    
    return func.HttpResponse(
        body={
            "id": instance_id,
            "statusQueryGetUri": status_url,
            "sendEventPostUri": raise_event_url,
            "terminatePostUri": terminate_url
        },
        status_code=200
    )
