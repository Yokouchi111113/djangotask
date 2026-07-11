import { expect } from "@playwright/test";

export function getTask(page, title) {
    return page.locator(".task").filter({
        has: page.getByText(title),
    });
}


export function formatDate(offset = 0) {
  const date = new Date();
  date.setDate(date.getDate() + offset);

  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, "0");
  const dd = String(date.getDate()).padStart(2, "0");

  return `${yyyy}-${mm}-${dd}`;
}