import { expect, test } from '@playwright/test';

test('shows the catalog from the API', async ({ page }) => {
  await page.route('**/api/v1/content', (route) =>
    route.fulfill({ json: [{ id: '1', title: 'Movie' }] }),
  );
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Lumia' })).toBeVisible();
  await expect(page.getByText('Movie')).toBeVisible();
});
