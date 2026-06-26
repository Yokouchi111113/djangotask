import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('http://127.0.0.1:8000/signup/');
  await page.locator('#signup-email').click();
  await page.locator('#signup-email').fill('test@example111.com');
  await page.locator('#signup-display-name').click();
  await page.locator('#signup-display-name').fill('159963');
  await page.locator('#signup-password1').click();
  await page.locator('#signup-password1').fill('password123');
  await page.locator('#signup-password2').click();
  await page.locator('#signup-password2').fill('password123');
  await page.getByRole('button', { name: '登録' }).click();
  await page.locator('#signin-email').click();
  await page.locator('#signin-email').fill('test@example111.com');
  await page.locator('#signin-password').click();
  await page.locator('#signin-password').fill('password123');
  await page.getByRole('button', { name: 'サインイン' }).click();
  await page.getByRole('textbox', { name: 'タイトル' }).click();
  await page.getByRole('textbox', { name: 'タイトル' }).fill('task');
  await page.getByRole('textbox', { name: '詳細を記載してください' }).click();
  await page.getByRole('textbox', { name: '詳細を記載してください' }).fill('create');
  await page.locator('#due_date').fill('2026-07-31');
  await page.getByRole('button', { name: '作成' }).click();
  await page.getByRole('button', { name: '編集' }).click();
  await page.getByRole('textbox', { name: '詳細を記載してください' }).click();
  await page.getByRole('textbox', { name: '詳細を記載してください' }).fill('create update');
  await page.getByRole('button', { name: '更新' }).click();
  page.once('dialog', dialog => {
    console.log(`Dialog message: ${dialog.message()}`);
    dialog.dismiss().catch(() => {});
  });
  await page.getByRole('button', { name: '削除' }).click();
  await page.getByRole('link', { name: 'signout' }).click();
});