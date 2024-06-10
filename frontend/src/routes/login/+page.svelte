<script>
    import { goto } from "$app/navigation";
    import Header from '../../components/Header.svelte';
    import { onMount } from 'svelte';

    let username = '';
    let password = '';
    let email = '';
    let errors = {};

    onMount(async () => {
        try {
            const response = await fetch('http://localhost:8000/check-login/', {
                credentials: 'include'
            });
            const data = await response.json();
            const isAuthenticated = data.message === 'User is logged in';

            // Redirect if user is authenticated
            if (isAuthenticated) {
                await goto('/'); // Redirect to the dashboard or any other page
            }
        } catch (error) {
            console.error('Error checking login status:', error);
        }
    });

    let handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const endpoint = 'http://localhost:8000/login/';
            const requestOptions = {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username: username, email: email, password: password })
            };

            const response = await fetch(endpoint, requestOptions);
            const data = await response.json();

            if (response.status === 200) {
                // Set the CSRF token and session ID in the cookies
                document.cookie = `csrftoken=${data.csrfToken}; path=/`;
                document.cookie = `sessionid=${data.sessionId}; path=/`;

                // Update session ID context
                // updateSessionId(data.sessionId);

                await goto('/');
            } else {
                const errorElement = document.getElementById('error-message');
                if (data.body.username) {
                    errorElement.innerHTML += `<p>Username is incorrect.</p>`;
                }
                if (data.body.email) {
                    errorElement.innerHTML += `<p>Email is incorrect.</p>`;
                }
                if (data.body.password) {
                    errorElement.innerHTML += `<p>Password is incorrect.</p>`;
                }
            }
        } catch (error) {
            // Display error message using JavaScript alert
            alert('An error occurred while logging in. Please try again.');
            console.error('Error:', error);
            // Refresh the page to handle the error
            location.reload();
        }
    };
</script>

<Header />

<div class="container">
    <div class="row">
        <h2 class="my-4">Whisperer Login</h2>
        <form on:submit|preventDefault={handleSubmit}>
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" bind:value={username} id="username" required>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" bind:value={email} id="email" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" bind:value={password} id="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</div>