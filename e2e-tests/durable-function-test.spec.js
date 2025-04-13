const { test, expect } = require('@playwright/test');

test('should verify local HTTP endpoint is available', async ({ request }) => {
  // Get the status URL directly from the API endpoint
  const response = await request.post('http://localhost:7071/api/orchestrators/HelloOrchestrator', {
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
  
  // Click the "Start Orchestration" button
  await page.click('button:has-text("Start Orchestration")');
  console.log('Clicked Start Orchestration button');
  
  // Wait for the status URL to appear
  console.log('Waiting for status URL to appear...');
  try {
    const statusUrlElement = await page.waitForSelector('p:has-text("Status URL:") code', { timeout: 30000 });
    const statusUrl = await statusUrlElement.textContent();
    console.log('Status URL found:', statusUrl);
  } catch (error) {
    console.error('Failed to find status URL element:', error);
    // Capture the page's current state for debugging
    await page.screenshot({ path: 'error-screenshot.png' });
    const html = await page.content();
    console.log('Page HTML at time of error:', html);
    throw error; // Re-throw to fail the test
  }
  
  // Verify that it's a valid URI
  expect(statusUrl).toBeTruthy();
  expect(statusUrl).toContain('http');
  
  // Wait a moment for the orchestration to complete
  // This is necessary because Durable Functions take some time to complete
  await page.waitForTimeout(3000);
  
  // Click the "Check Status" button
  await page.click('button:has-text("Check Status")');
  console.log('Clicked Check Status button');
  
  // Wait for the status text to appear
  const statusText = await page.waitForSelector('p:has-text("Status:")', { timeout: 30000 });
  const status = await statusText.textContent();
  console.log('Status found:', status);
  
  // Verify that the status shows "Completed"
  expect(status).toContain('Completed');
  console.log('Successfully verified status is Completed');
});