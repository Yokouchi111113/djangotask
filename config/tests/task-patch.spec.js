import { test, expect } from '@playwright/test';
import { signup, signin, DEFAULT_PASSWORD } from "./auth";
import { createTask } from "./task";

const title = `Task ${Date.now()}`;
const updatedTitle = `Updated Task ${Date.now()}`;
const updatedDueDate = '2027-08-15';


test('認証済みユーザーがタスクを編集できる', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await expect(page.getByRole('link', { name: 'signout' })).toBeVisible();
  await createTask(page, title);
  await expect(page.getByText(title)).toBeVisible();
  await page.getByRole('button', { name: '編集' }).click();
  await page.getByRole('textbox', { name: 'タイトル' }).fill(updatedTitle);
  await page.getByRole('textbox', { name: '詳細を記載してください' }).fill('update');
  await page.locator('#status').selectOption('done');
  await page.locator('#due_date').fill(updatedDueDate);
  await page.getByRole('button', { name: '更新' }).click();

  const task = page.locator('.task').filter({
      has: page.getByText(updatedTitle),
  });

  await expect(task.locator('.task-title')).toHaveText(updatedTitle);
  await expect(task.locator('.task-description')).toHaveText('update');
  await expect(task.getByText('完了')).toBeVisible();
  await expect(task.getByText(updatedDueDate)).toBeVisible();
});