const { test, expect } = require('@playwright/test');

test('should verify local HTTP endpoint is available', async ({ request }) => {
  // Get the status URL directly from the API endpoint
  const response = await request.post('http://localhost:7071/api/orchestrators/hello_orchestrator', {
    timeout: 60000
  });
  
  console.log('Response status:', response.status());
  
  // Verify that we get a successful response code (2xx)
  expect(response.status()).toBeLessThan(300);
  expect(response.status()).toBeGreaterThanOrEqual(200);
  
  const responseBody = await response.json();
  console.log('Response body:', JSON.stringify(responseBody, null, 2));
  
  // Verify that the response contains a statusQueryGetUri
  expect(responseBody.statusQueryGetUri).toBeTruthy();
  console.log('StatusQueryGetUri:', responseBody.statusQueryGetUri);
});

test('should complete the full user journey - start orchestration, check status, and verify completion', async ({ page }) => {
  // Navigate to the React app
  await page.goto('http://localhost:3000');
  console.log('Navigated to frontend app');
  
  // Click the "Start Orchestration" button using data-testid
  await page.getByTestId('start-button').click();
  console.log('Clicked Start Orchestration button');
  
  // Wait for the status URL to appear using data-testid
  console.log('Waiting for status URL to appear...');
  try {
    await page.getByTestId('status-url').waitFor({ timeout: 30000 });
    const statusUrl = await page.getByTestId('status-url').innerText();
    console.log('Status URL found:', statusUrl);
    
    // Verify that it's a valid URI
    expect(statusUrl).toBeTruthy();
    expect(statusUrl).toContain('http');
  } catch (error) {
    console.error('Failed to find status URL element:', error);
    // Capture the page's current state for debugging
    await page.screenshot({ path: 'error-screenshot.png' });
    const html = await page.content();
    console.log('Page HTML at time of error:', html);
    throw error; // Re-throw to fail the test
  }
  
  // Wait longer for the orchestration to complete (increase from 3s to 10s)
  await page.waitForTimeout(10000);
  
  // Click the "Check Status" button using data-testid
  await page.getByTestId('check-status-button').click();
  console.log('Clicked Check Status button');
  
  // Poll for "Completed" status with multiple retries
  let status = '';
  let retries = 5;  // Number of attempts to check for completion
  const retryInterval = 3000;  // 3 seconds between retries
  
  while (retries > 0) {
    // Wait for the status text to appear using data-testid
    await page.getByTestId('status-display').waitFor({ timeout: 10000 });
    status = await page.getByTestId('status-display').innerText();
    console.log(`Status found (${retries} retries left):`, status);
    
    if (status.includes('Completed')) {
      break;  // Exit the loop if we found the Completed status
    }
    
    // If not complete yet, wait and check status again
    await page.waitForTimeout(retryInterval);
    if (retries > 1) {  // Don't click the button on the last iteration
      await page.getByTestId('check-status-button').click();
      console.log('Clicked Check Status button again');
    }
    
    retries--;
  }
  
  // Verify that the status shows "Completed"
  expect(status).toContain('Completed');
  console.log('Successfully verified status is Completed');
});