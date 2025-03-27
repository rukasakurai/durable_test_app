import azure.functions as func
import azure.durable_functions as df

async def main(req: func.HttpRequest, instanceId: str, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)

    # Extract X-Forwarded-Host and X-Forwarded-Proto headers
    forwarded_host = req.headers.get("X-Forwarded-Host")
    forwarded_proto = req.headers.get("X-Forwarded-Proto")

    # Get status response
    status_response = await client.get_status(instanceId)

    # Use custom domain for status URL
    if forwarded_host and forwarded_proto:
        status_url = status_response.headers["Location"]
        status_url = status_url.replace(req.url, f"{forwarded_proto}://{forwarded_host}")
        status_response.headers["Location"] = status_url

    return func.HttpResponse(status_response)
