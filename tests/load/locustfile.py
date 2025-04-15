import json
import time
from locust import HttpUser, task, between, events


class DurableFunctionUser(HttpUser):
    wait_time = between(1, 3)  # Wait between 1 and 3 seconds between tasks

    @task
    def test_durable_function(self):
        # Step 1: Start the orchestration
        with self.client.post("/api/orchestrators/hello_orchestrator", 
                             name="Start Orchestration", 
                             catch_response=True) as response:
            if response.status_code == 202:  # Accepted
                # Extract the statusQueryGetUri for polling from the response headers
                status_url = response.headers.get('Location')
                if not status_url:
                    response.failure("No status URL returned in the Location header")
                    return

                # Store the status URL for this user's session
                self.status_url = status_url
            else:
                response.failure(f"Failed to start orchestration: {response.status_code}")
                return

        # Step 2: Poll the status URL until the orchestration completes or times out
        max_polls = 10
        polls = 0
        while polls < max_polls:
            polls += 1
            time.sleep(1)  # Wait before polling again
            
            # Extract just the path part of the URL for the client
            path_only = self.status_url.split('/api')[1] if '/api' in self.status_url else self.status_url
            
            with self.client.get(path_only, 
                                name="Poll Orchestration Status", 
                                catch_response=True) as status_response:
                if status_response.status_code != 200:
                    status_response.failure(f"Failed to poll status: {status_response.status_code}")
                    break
                
                try:
                    status_data = json.loads(status_response.text)
                    
                    # Check if orchestration is completed
                    if status_data.get('runtimeStatus') == 'Completed':
                        status_response.success()
                        # Verify the output if needed
                        if 'output' in status_data:
                            output = status_data['output']
                            if isinstance(output, str) and 'Hello' in output:
                                status_response.success()
                            else:
                                status_response.failure(f"Unexpected output: {output}")
                        break
                    
                    # Continue polling if still running
                    if status_data.get('runtimeStatus') in ['Running', 'Pending']:
                        status_response.success()
                        continue
                    
                    # Handle failed or other states
                    if status_data.get('runtimeStatus') in ['Failed', 'Terminated', 'Canceled']:
                        status_response.failure(f"Orchestration failed: {status_data}")
                        break
                        
                except json.JSONDecodeError:
                    status_response.failure("Invalid JSON response")
                    break
                    
        # If we exhausted our polls, mark as failure
        if polls >= max_polls:
            events.request.fire(
                request_type="GET",
                name="Poll Orchestration Status - Timeout",
                response_time=polls * 1000,  # Approximate total polling time in ms
                response_length=0,
                exception=Exception("Orchestration polling timed out"),
            )


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("Load test is starting!")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Load test has completed!")