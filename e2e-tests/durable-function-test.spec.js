const { test, expect } = require('@playwright/test');

test('should start orchestration and verify statusQueryGetUri', async ({ page }) => {
  // Navigate to the React app
  await page.goto('http://localhost:3000');
  
  // Click the "Start Orchestration" button
  await page.click('text=Start Orchestration');
  
  // Wait for the status URL to appear
  const statusUrlElement = await page.waitForSelector('code', { timeout: 30000 });
  const statusUrl = await statusUrlElement.innerText();
  
  // Log and verify the statusQueryGetUri
  console.log('StatusQueryGetUri:', statusUrl);
  
  // Check that it's a valid URI
  expect(statusUrl).toBeTruthy();
  expect(statusUrl).toContain('http');
  
  // Parse the URL to verify it's valid
  expect(() => new URL(statusUrl)).not.toThrow();
  
  // Additional check that the URL contains expected elements for a Durable Functions status URL
  expect(statusUrl).toMatch(/\/runtime\/webhooks\/durabletask/);
});