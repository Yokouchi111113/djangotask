document
    .getElementById("signup-form")
    .addEventListener("submit", signup);

async function signup(e) {
    e.preventDefault();

    const email = document.getElementById(
        "signup-email"
    ).value;
    const displayName = document.getElementById(
        "signup-display-name"
    ).value;
    const password1 = document.getElementById(
        "signup-password1"
    ).value;
    const password2 = document.getElementById(
        "signup-password2"
    ).value;

    const message = document.getElementById("message");

    try{
        const res = await fetch("/api/signup/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: email,
                display_name: displayName,
                password1: password1,
                password2: password2,
            }),
        });

        if (!res.ok) {
            const data = await res.json();
            message.textContent = 
                Object.values(data).flat().join(" ");
            return;
        }

        message.textContent = "登録成功しました";

        setTimeout(() => {
            location.href = "/signin/";
        }, 1000);
    } catch (error) {
        console.error(error);

        message.textContent =
            "通信エラーが発生しました";
    }
}