import { test, expect } from '@playwright/test';
import { signup, signin, DEFAULT_PASSWORD } from "./auth";
import { createTask } from "./task";
import { getTask } from "./helpers";

const title = `Task ${Date.now()}`;

test('認証済みユーザーがタスクを削除できる', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await createTask(page, title);
  await expect(page.getByText(title)).toBeVisible();
  page.once('dialog', async dialog => {
      expect(dialog.message()).toContain('削除');
      await dialog.accept();
    });
  await page.getByRole('button', { name: '削除' }).click();

  const task = getTask(page, title);

  await expect(task).toHaveCount(0);
});
