param location string = resourceGroup().location
// As of April 13, 2025, Azure Static Web Apps are not available in Japan East
// Using East Asia as it's the closest available region to Japan East for Static Web Apps
param staticWebAppLocation string = 'eastasia'
param functionAppName string
param storageAccountName string
param appServicePlanName string
param appInsightsName string
param staticWebAppName string

var functionWorkerRuntime = 'python'
var functionAppVersion = '~4'
var linuxFxVersion = 'Python|3.11'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    supportsHttpsTrafficOnly: true
    defaultToOAuthAuthentication: true
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2024-04-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'EP1'
    tier: 'Premium'
  }
  properties: {
    reserved: true // Required for Linux
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    Request_Source: 'rest'
  }
}

resource functionApp 'Microsoft.Web/sites@2024-04-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp,linux'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: linuxFxVersion
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: toLower(functionAppName)
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: functionAppVersion
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: functionWorkerRuntime
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
      ]
      cors: {
        allowedOrigins: [
          'http://localhost:3000'
          'https://localhost:3000'
        ]
      }
    }
    httpsOnly: true
  }
}

resource staticWebApp 'Microsoft.Web/staticSites@2024-04-01' = {
  name: staticWebAppName
  // Using different location for Static Web App due to service availability constraints
  location: staticWebAppLocation
  sku: {
    name: 'Free' // Valid options: 'Free', 'Standard', or 'Dedicated'
    tier: 'Free'
  }
  properties: {
    branch: 'main'
    repositoryUrl: 'https://github.com/rukasakurai/durable_test_app'
    buildProperties: {
      appLocation: 'frontend'
      outputLocation: 'build'
      apiLocation: 'http_start' // Points to the directory containing the main Azure Function app
    }
  }
}

output functionAppName string = functionApp.name
output functionAppUrl string = 'https://${functionApp.properties.defaultHostName}'
output staticWebAppUrl string = 'https://${staticWebApp.properties.defaultHostname}'
