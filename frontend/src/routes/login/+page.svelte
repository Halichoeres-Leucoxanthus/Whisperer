<script>
import {goto} from "$app/navigation";
import { onMount, setContext } from 'svelte';
import Header from '../../components/Header.svelte';

let username = '';
let email = '';
let password = '';
let errors = {};
let isAuthenticated = false;

onMount(async () => {
    try {
        const response = await fetch('http://localhost:8000/check-login/', {
            credentials: 'include'
        });
        const data = await response.json();
        isAuthenticated = data.message === 'User is logged in';

        // Redirect if user is authenticated
        if (isAuthenticated) {
            await goto('/'); // Redirect to the dashboard or any other page
        }
    } catch (error) {
        console.error('Error checking login status:', error);
    }
});
let handleSubmit = async () => {
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

            // Set the session ID in the context
            setContext('sessionId', data.sessionId);

            await goto('/');
        } else {
            errors = data.body;
            console.log(data);
        }
    } catch (error) {
        console.error('Error:', error);
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
                {#if errors.username}
                    <div class="invalid-feedback">Invalid username</div>
                {/if}
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" bind:value={email} id="email" required>
                {#if errors.email}
                    <div class="invalid-feedback">Invalid email</div>
                {/if}
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" bind:value={password} id="password" required>
                {#if errors.password}
                    <div class="invalid-feedback">Invalid password</div>
                {/if}
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</div>