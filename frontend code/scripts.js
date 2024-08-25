async function addPassword() {
    const site = document.getElementById('site').value;
    const password = document.getElementById('password').value;

    if (site && password) {
        const response = await fetch('/add_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ site, password }),
        });

        const data = await response.json();
        alert(data.message || data.error);
    } else {
        alert('Please fill out both fields.');
    }
}

async function getPassword() {
    const site = document.getElementById('getSite').value;

    if (site) {
        const response = await fetch(`/get_password?site=${encodeURIComponent(site)}`);
        const data = await response.json();
        document.getElementById('passwordDisplay').innerText = data.password || data.error;
    } else {
        alert('Please enter a site.');
    }
}

async function listPasswords() {
    const response = await fetch('/list_passwords');
    const data = await response.json();
    document.getElementById('passwordsList').innerText = JSON.stringify(data, null, 2);
}
