import { test, expect } from '@playwright/test';
import { signup, signin, DEFAULT_PASSWORD } from "./auth";
import { createTask } from "./task";


const title = `Task ${Date.now()}`;


test('認証済みユーザーがタスクを作成できる', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await expect(page).toHaveURL(/\/tasks\/$/);
  await createTask(page, title);
  await expect(page.getByText(title)).toBeVisible();
});

test('タイトルが100文字でもタスクを作成できる', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await expect(page).toHaveURL(/\/tasks\/$/);
  const longTitle = "a".repeat(100);
  await createTask(page, longTitle);
  await expect(page.getByText(longTitle)).toBeVisible();
});


test('タイトル未入力ではタスクを作成できない', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await expect(page).toHaveURL(/\/tasks\/$/);
  await createTask(page, '');
  const valid = await page.locator("#title").evaluate(
  el => el.checkValidity()
  );
  expect(valid).toBe(false);
});

test('タイトルは2文字以下では作成できない', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await expect(page).toHaveURL(/\/tasks\/$/);
  await createTask(page, '12');
  await expect(page.getByText('この項目は少なくとも3文字以上にしてください')).toBeVisible();
});

test('過去の日付ではタスクを作成できない', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await expect(page).toHaveURL(/\/tasks\/$/);
  await createTask(page, title, "2026-06-11");
  await expect(page.getByText('過去の日付は設定できません')).toBeVisible();
});


test('タイトルが100文字を超えるとタスクを作成できない', async ({ page }, testInfo) => {
  const email = `test-${testInfo.project.name}-${Date.now()}@example.com`;
  await signup(page, email, DEFAULT_PASSWORD);
  await signin(page, email, DEFAULT_PASSWORD);
  await expect(page).toHaveURL(/\/tasks\/$/);
  const longTitle = "a".repeat(101);
  await createTask(page, longTitle);
  await expect(page.getByText('この項目が100文字より長くならないようにしてください')).toBeVisible();
});