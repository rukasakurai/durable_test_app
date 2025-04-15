import json
import time
import os
from urllib.parse import urlparse, urljoin
from locust import HttpUser, task, between, events


class DurableFunctionUser(HttpUser):
    wait_time = between(0.5, 1)  # Wait between 0.5 and 1 second between tasks

    def on_start(self):
        # Initialize the orchestrator endpoint path
        self.orchestrator_path = "/api/orchestrators/hello_orchestrator"
        
        # Log if we're using environment variable for host URL
        host_url_env = os.environ.get("HOST_URL")
        if host_url_env and not self.host:
            print(f"Using HOST_URL environment variable: {host_url_env}")
            self.host = host_url_env

    @task
    def test_durable_function(self):
        # Step 1: Start the orchestration
        start_url = self.orchestrator_path
        
        with self.client.post(start_url, 
                             name="Start Orchestration", 
                             catch_response=True) as response:
            if response.status_code == 202:  # Accepted
                # Extract the statusQueryGetUri for polling from the response headers
                status_url = response.headers.get('Location')
                if not status_url:
                    response.failure("No status URL returned in the Location header")
                    return
                
                # Just log the status URL, but don't poll it
                print(f"Received status URL: {status_url}")
                response.success()
            else:
                response.failure(f"Failed to start orchestration: {response.status_code}")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("Load test is starting!")
    print(f"Target host: {environment.host}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Load test has completed!")