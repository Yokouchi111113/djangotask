import { test, expect } from '@playwright/test';
import { signup, signin, DEFAULT_PASSWORD } from "./auth";



test('ユーザーがサインアップ、サインイン・サインアウトができる', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await expect(page.getByRole('link', { name: 'signout' })).toBeVisible();
  await page.getByRole('link', { name: 'signout' }).click();
  await expect(page).toHaveURL('http://127.0.0.1:8000/signin/');
  await expect(page.getByRole('button', { name: 'サインイン' })).toBeVisible();
});



// negative
test('パスワード不一致でサインアップできない', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await page.goto('http://127.0.0.1:8000/signup/');
  await page.locator('#signup-email').fill(email);
  await page.locator('#signup-display-name').fill('159963');
  await page.locator('#signup-password1').fill('password123');
  await page.locator('#signup-password2').fill('password951');
  await page.getByRole('button', { name: '登録' }).click();
  await expect(page).toHaveURL('http://127.0.0.1:8000/signup/');
  await expect(page.getByText("パスワードが一致しません")).toBeVisible();
});

test('重複メールアドレスでサインアップできない', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await page.goto('http://127.0.0.1:8000/signup/');
  await page.locator('#signup-email').fill(email);
  await page.locator('#signup-password1').fill('password123');
  await page.locator('#signup-password2').fill('password123');
  await page.getByRole('button', { name: '登録' }).click();
  await expect(page).toHaveURL('http://127.0.0.1:8000/signup/');
  await expect(page.getByText("この メールアドレス を持った ユーザー が既に存在します")).toBeVisible();
});

test('サインアップ画面でメールアドレス未入力', async ({ page }) => {
  await page.goto('http://127.0.0.1:8000/signup/');
  await page.locator('#signup-email').fill('');
  await page.locator('#signup-password1').fill('password123');
  await page.locator('#signup-password2').fill('password123');
  await page.getByRole('button', { name: '登録' }).click();
  await expect(page).toHaveURL('http://127.0.0.1:8000/signup/');
  const valid = await page.locator("#signup-email").evaluate(
  el => el.checkValidity()
  );
  expect(valid).toBe(false);
});

test('サインアップ画面でパスワード(確認用)未入力', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await page.goto('http://127.0.0.1:8000/signup/');
  await page.locator('#signup-email').fill(email);
  await page.locator('#signup-password1').fill('password123');
  await page.locator('#signup-password2').fill('');
  await page.getByRole('button', { name: '登録' }).click();
  await expect(page).toHaveURL('http://127.0.0.1:8000/signup/');
  const valid = await page.locator("#signup-password2").evaluate(
  el => el.checkValidity()
  );
  expect(valid).toBe(false);
});



test('誤ったパスワードでサインインできない', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, 'pass852');
  await expect(page).toHaveURL('http://127.0.0.1:8000/signin/');
  await expect(page.getByText("メールアドレスまたはパスワードが違います")).toBeVisible();
});

test('パスワード未入力でサインインできない', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, '');
  await expect(page).toHaveURL('http://127.0.0.1:8000/signin/');
  const valid = await page.locator("#signin-password").evaluate(
  el => el.checkValidity()
  );
  expect(valid).toBe(false);
});

test('誤ったメールアドレスでサインインできない', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, 'test@example963.com', DEFAULT_PASSWORD);
  await expect(page).toHaveURL('http://127.0.0.1:8000/signin/');
  await expect(page.getByText("メールアドレスまたはパスワードが違います")).toBeVisible();
});

test('メールアドレス未入力でサインインできない', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, '', DEFAULT_PASSWORD);
  await expect(page).toHaveURL('http://127.0.0.1:8000/signin/');
  const valid = await page.locator("#signin-email").evaluate(
  el => el.checkValidity()
  );
  expect(valid).toBe(false);
});