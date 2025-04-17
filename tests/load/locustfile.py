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
        start_url = self.orchestrator_path
        
        with self.client.post(start_url, 
                             name="Start Orchestration", 
                             catch_response=True) as response:
            if response.status_code == 202:  # Accepted
                # Extract statusQueryGetUri from the response body (JSON)
                data = response.json()
                status_url = data.get('statusQueryGetUri')
                print(f"Received status URL: {status_url}")
                
                # Poll the status URL (once, or until completed with timeout)
                max_wait = 10  # seconds
                poll_interval = 3  # seconds
                waited = 0
                while waited < max_wait:
                    with self.client.get(status_url, name="Check Status", catch_response=True) as status_resp:
                        if status_resp.status_code == 200:
                            try:
                                status_data = status_resp.json()
                                runtime_status = status_data.get('runtimeStatus')
                                print(f"Polled status: runtimeStatus={runtime_status}, full response={status_data}")
                                if runtime_status == 'Completed':
                                    status_resp.success()
                                    break
                                else:
                                    status_resp.success()
                            except Exception as e:
                                status_resp.failure(f"Failed to parse status response: {e}")
                                break
                        elif status_resp.status_code == 202:
                            # 202 means still running, treat as success and continue polling
                            status_resp.success()
                            print("Orchestration still running, will poll again.")
                        else:
                            status_resp.failure(f"Failed to get status: {status_resp.status_code}")
                            break
                    time.sleep(poll_interval)
                    waited += poll_interval
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