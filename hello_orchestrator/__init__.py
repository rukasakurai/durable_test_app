import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    yield context.call_activity("say_hello", "Durable Functions")
    return "Done"

main = df.Orchestrator.create(orchestrator_function)
