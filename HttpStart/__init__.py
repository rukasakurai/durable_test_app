import os
import azure.functions as func
import azure.durable_functions as df

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    instance_id = await client.start_new("HelloOrchestrator")
    
    custom_domain = os.getenv("CUSTOM_DOMAIN")
    status_response = client.create_check_status_response(req, instance_id)
    
    if custom_domain:
        status_response.headers["Location"] = status_response.headers["Location"].replace("*.azurewebsites.net", custom_domain)
        status_response.headers["Retry-After"] = status_response.headers["Retry-After"].replace("*.azurewebsites.net", custom_domain)
        status_response.headers["StatusQueryGetUri"] = status_response.headers["StatusQueryGetUri"].replace("*.azurewebsites.net", custom_domain)
        status_response.headers["SendEventPostUri"] = status_response.headers["SendEventPostUri"].replace("*.azurewebsites.net", custom_domain)
        status_response.headers["TerminatePostUri"] = status_response.headers["TerminatePostUri"].replace("*.azurewebsites.net", custom_domain)
        status_response.headers["PurgeHistoryDeleteUri"] = status_response.headers["PurgeHistoryDeleteUri"].replace("*.azurewebsites.net", custom_domain)
    
    return status_response
