const token = localStorage.getItem("access");

const signinLink = document.getElementById("signin-link");
const signoutLink = document.getElementById("signout-link");

if (token) {
    signinLink.style.display = "none";
} else {
    signoutLink.style.display = "none";
}

signoutLink?.addEventListener("click", (e) => {
    e.preventDefault();

    localStorage.removeItem("access");
    localStorage.removeItem("refresh");

    location.href = "/signin/";
});