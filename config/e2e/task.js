import { expect } from "@playwright/test";


export async function createTask(page, title, due_date = "2026-07-31") {
    await page.getByRole('textbox', { name: 'タイトル' }).fill(title);
    await page.getByRole('textbox', { name: '詳細を記載してください' }).fill('create');
    await page.locator('#due_date').fill(due_date);
    await page.getByRole('button', { name: '作成' }).click();
}