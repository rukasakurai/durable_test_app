import azure.functions as func
import azure.durable_functions as df
import os
import urllib.parse

def rewrite_url(url, custom_domain):
    parsed_url = urllib.parse.urlparse(url)
    new_netloc = custom_domain
    new_url = parsed_url._replace(netloc=new_netloc)
    return new_url.geturl()

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new("HelloOrchestrator")
    response = client.create_check_status_response(req, instance_id)

    custom_domain = os.getenv("CUSTOM_DOMAIN")
    if custom_domain:
        response.headers["Location"] = rewrite_url(response.headers["Location"], custom_domain)
        response.headers["Retry-After"] = rewrite_url(response.headers["Retry-After"], custom_domain)
        response.headers["StatusQueryGetUri"] = rewrite_url(response.headers["StatusQueryGetUri"], custom_domain)
        response.headers["SendEventPostUri"] = rewrite_url(response.headers["SendEventPostUri"], custom_domain)
        response.headers["TerminatePostUri"] = rewrite_url(response.headers["TerminatePostUri"], custom_domain)
        response.headers["PurgeHistoryDeleteUri"] = rewrite_url(response.headers["PurgeHistoryDeleteUri"], custom_domain)

    return response
