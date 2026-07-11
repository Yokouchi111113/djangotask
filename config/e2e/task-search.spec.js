import { test, expect } from '@playwright/test';
import { signup, signin, DEFAULT_PASSWORD } from "./auth";
import { createTask } from "./task";
import { getTask, formatDate } from "./helpers";


const now = Date.now();
const title = `Play A ${now}`;
const titleB = `Django B ${now}`;


test('認証済みユーザーがタスクを検索できる', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await expect(page.getByRole('link', { name: 'signout' })).toBeVisible();
  await createTask(page, title);
  await expect(page.getByText(title)).toBeVisible();

  const task = getTask(page, title, formatDate(1));

  await createTask(page, titleB, formatDate(0));

  const taskB = getTask(page, titleB);

  await page.getByRole('searchbox', { name: 'タスク検索' }).fill(title);
  await page.getByRole('button', { name: '検索' }).click();
  await expect(page.locator('.task')).toHaveCount(1);
  await expect(page.getByText(title)).toBeVisible();
  await expect(task).toHaveCount(1);
  await expect(taskB).toHaveCount(0);
  await page.getByRole('link', { name: 'タスク管理' }).click();
  await page.getByPlaceholder('期限検索').fill('0');
  await page.getByRole('button', { name: '検索' }).click();
  await expect(task).toHaveCount(0);
  await expect(taskB).toHaveCount(1);
});

test('該当するタスクが存在しない', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await expect(page.getByRole('link', { name: 'signout' })).toBeVisible();
  await createTask(page, title);
  await expect(page.getByText(title)).toBeVisible();
  await createTask(page, titleB);
  await expect(page.getByText(titleB)).toBeVisible();
  await page.getByRole('searchbox', { name: 'タスク検索' }).fill('Java');
  await page.getByRole('button', { name: '検索' }).click();
  await expect(page.locator('.task')).toHaveCount(0);
  await expect(page.getByText('該当するタスクはありません')).toBeVisible();
});


test('空欄で検索すると全件表示される', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await expect(page.getByRole('link', { name: 'signout' })).toBeVisible();
  await createTask(page, title);
  await expect(page.getByText(title)).toBeVisible();
  await createTask(page, titleB);
  await page.getByRole('searchbox', { name: 'タスク検索' }).fill('');
  await page.getByRole('button', { name: '検索' }).click();
  await expect(page.locator('.task')).toHaveCount(2);
});

test('スペースで検索すると全件表示される', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await expect(page.getByRole('link', { name: 'signout' })).toBeVisible();
  await createTask(page, title);
  await expect(page.getByText(title)).toBeVisible();
  await createTask(page, titleB);
  await page.getByRole('searchbox', { name: 'タスク検索' }).fill('  ');
  await page.getByRole('button', { name: '検索' }).click();
  await expect(page.locator('.task')).toHaveCount(2);
});

test('期限検索で該当するタスクがない場合、該当するタスクはありませんが返る', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);

  await createTask(page, title, formatDate(1));

  const task = getTask(page, title);

  await expect(task).toContainText("残り 1 日");
  await page.getByPlaceholder('期限検索').fill('0');
  await page.getByRole('button', { name: '検索' }).click();
  await expect(page.getByText('該当するタスクはありません')).toBeVisible();
});