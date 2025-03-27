import azure.functions as func
import azure.durable_functions as df

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new("HelloOrchestrator")

    # Extract X-Forwarded-Host and X-Forwarded-Proto headers
    forwarded_host = req.headers.get("X-Forwarded-Host")
    forwarded_proto = req.headers.get("X-Forwarded-Proto")

    # Modify create_check_status_response to use custom domain
    status_response = client.create_check_status_response(req, instance_id)
    if forwarded_host and forwarded_proto:
        status_url = status_response.headers["Location"]
        status_url = status_url.replace(req.url, f"{forwarded_proto}://{forwarded_host}")
        status_response.headers["Location"] = status_url

    return status_response
