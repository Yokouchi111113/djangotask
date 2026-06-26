document
    .getElementById("signin-form")
    .addEventListener("submit", signin);

async function signin(e) {
    e.preventDefault();

    const email = 
        document.getElementById("signin-email").value;
    
    const password = 
        document.getElementById("signin-password").value;

    const message = document.getElementById("message");

    try{
        const res = await fetch("/api/signin/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: email,
                password: password,
            }),
        });


        if (!res.ok) {
            message.textContent = "メールアドレスまたはパスワードが違います";
            return;
        }

        const data = await res.json();

        localStorage.setItem(
            "access", 
            data.access
        );
        localStorage.setItem(
            "refresh", 
            data.refresh
        );

        location.href = "/tasks/";

    } catch (error) {
        console.error(error);

        message.textContent =
            "通信エラーが発生しました";
    }
}