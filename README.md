# Durable Functions Test App

This repository contains an Azure Durable Functions application with a React frontend.

## Prerequisites

Before running this application locally, make sure you have the following installed:

- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js 16+](https://nodejs.org/)
- [Azure Functions Core Tools v4](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python#install-the-azure-functions-core-tools)
- [Visual Studio Code](https://code.visualstudio.com/) (recommended)
- [Azure Functions extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) (optional)

## Setup Instructions

### Setting Up the Backend (Azure Functions)

1. Open a command prompt or PowerShell terminal
2. Navigate to the project root directory:
   ```
   cd c:\Users\rusakura\code\github.com\rukasakurai\durable_test_app
   ```
3. Create a Python virtual environment:
   ```
   python -m venv .venv
   ```
4. Activate the virtual environment:
   ```
   .venv\Scripts\activate
   ```
5. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

### Setting Up the Frontend (React)

1. Open a new command prompt or PowerShell terminal
2. Navigate to the frontend directory:
   ```
   cd c:\Users\rusakura\code\github.com\rukasakurai\durable_test_app\frontend
   ```
3. Install the required npm packages:
   ```
   npm install
   ```

## Running the Application Locally

### Starting the Azure Functions Backend

1. Ensure your virtual environment is activated:
   ```
   .venv\Scripts\activate
   ```
   (If you're in the same terminal session from the setup steps, it should already be activated)

2. In the project root directory, start the Azure Functions host:
   ```
   func start
   ```
   This will start the Azure Functions runtime locally, hosting your durable functions.

3. Note the URL where your HTTP trigger function is running (typically http://localhost:7071/api/HttpStart)

### Starting the React Frontend

1. In a separate terminal, navigate to the frontend directory:
   ```
   cd c:\Users\rusakura\code\github.com\rukasakurai\durable_test_app\frontend
   ```

2. Start the React development server:
   ```
   npm start
   ```

3. Your default browser should automatically open to http://localhost:3000, showing the frontend application

## Testing the Application

Once both the backend and frontend are running:

1. Use the frontend interface to interact with the Durable Functions app
2. Alternatively, you can test the backend directly by sending HTTP requests to the HttpStart endpoint:
   ```
   http://localhost:7071/api/HttpStart
   ```

## Troubleshooting

- **Port conflicts**: If another application is using port 7071 or 3000, you may need to configure different ports
- **CORS issues**: If you encounter CORS errors, check the Azure Functions local.settings.json file to ensure it has proper CORS settings
- **Python/Node version incompatibilities**: Ensure you're using compatible versions of Python and Node as listed in prerequisites

## Application Structure

- `host.json`: Configuration for the Azure Functions host
- `requirements.txt`: Python dependencies
- `frontend/`: Contains the React frontend application
- `HelloOrchestrator/`: The durable orchestrator function
- `HttpStart/`: HTTP trigger function to start the orchestration
- `SayHello/`: Activity function called by the orchestrator