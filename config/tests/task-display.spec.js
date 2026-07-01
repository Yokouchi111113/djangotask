import { test, expect } from '@playwright/test';
import { signup, signin, DEFAULT_PASSWORD } from "./auth";
import { createTask } from "./task";
import { getTask, formatDate } from "./helpers";



const now = Date.now();
const title = `Play A ${now}`;
const titleB = `Django B ${now}`;

test('期限付きタスクは残り日数が表示される', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await createTask(page, title, formatDate(1));
  const task = getTask(page, title);
  await expect(task).toContainText("残り 1 日");
});


test('期限が今日のタスクは今日までと表示される', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await createTask(page, title, formatDate(0));
  const task = getTask(page, title);
  await expect(task).toContainText("今日まで");
});

