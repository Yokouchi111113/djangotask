import { expect } from "@playwright/test";


export const DEFAULT_PASSWORD = "password123";

export async function signup(page, email, password) {
    await page.goto('http://127.0.0.1:8000/signup/');
    await page.locator('#signup-email').fill(email);
    await page.locator('#signup-display-name').fill('159963');
    await page.locator('#signup-password1').fill(password);
    await page.locator('#signup-password2').fill(password);
    await page.getByRole('button', { name: '登録' }).click();
    await expect(page).toHaveURL('http://127.0.0.1:8000/signin/');
}


export async function signin(page, email, password) {
    await page.goto("http://127.0.0.1:8000/signin/");
    await page.locator('#signin-email').fill(email);
    await page.locator('#signin-password').fill(password);
    await page.getByRole('button', { name: 'サインイン' }).click();
}

