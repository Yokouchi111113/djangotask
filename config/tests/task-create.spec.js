import { test, expect } from '@playwright/test';
import { signup, signin, DEFAULT_PASSWORD } from "./auth";
import { createTask } from "./task";


const title = `Task ${Date.now()}`;


test('認証済みユーザーがタスクを作成できる', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await createTask(page, title);
  await expect(page.getByText(title)).toBeVisible();
});