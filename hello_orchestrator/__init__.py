import azure.durable_functions as df
import logging

def orchestrator_function(context: df.DurableOrchestrationContext):
    instance_id = context.instance_id
    logging.info(f"Orchestrator started. Instance ID: {instance_id}")
    try:
        yield context.call_activity("say_hello", "Durable Functions")
        return "Done"
    except Exception as e:
        logging.error(f"Exception in orchestrator. Instance ID: {instance_id}. Error: {e}")
        raise

main = df.Orchestrator.create(orchestrator_function)
