async function authFetch(url, options = {}) {
    const token = localStorage.getItem("access");

    return fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
            ...options.headers,
        },
    });
}