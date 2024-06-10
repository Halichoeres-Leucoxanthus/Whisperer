<script>
    import { goto } from "$app/navigation";
    import Header from '../../components/Header.svelte';
    import { onMount } from 'svelte';

    let username = '';
    let password = '';
    let first_name = '';
    let last_name = '';
    let email = '';
    let errors = {};
    let passwordSuccess = false;
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
        const endpoint = 'http://localhost:8000/register/';
        const requestOptions = {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username, password: password, first_name: first_name, last_name: last_name, email: email })
        }

        try {
            const response = await fetch(endpoint, requestOptions);
            const data = await response.json();

            if (response.status === 201) {
                await goto('/login/');
            } else {
                errors = data.body;
                console.log(data);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    let validatePassword = () => {
        if (password.length < 8) {
            errors.password = 'Password must be at least 8 characters';
            passwordSuccess = false;
        } else if (!password.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$%*#?&.,_])[A-Za-z\d@$#%*?&.,_]{8,}$/)) {
            errors.password = 'Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character';
            passwordSuccess = false;
        } else {
            delete errors.password;
            passwordSuccess = true;
        }
    }
</script>

<Header />

<div class="container">
    <div class="row">
        <h2 class="my-4">Register</h2>
        <form on:submit|preventDefault={handleSubmit}>
            <div class="form-row">
                <div class="form-group col-md-6">
                    <label for="name">Name:</label>
                    <input class="form-control mb-3" type="text" placeholder="Name" bind:value={first_name}>
                    {#if errors && errors.name}
                        <p class="text-danger">{errors.name}</p>
                    {/if}
                </div>
                <div class="form-group col-md-6">
                    <label for="surname">Surname:</label>
                    <input class="form-control mb-3" type="text" placeholder="Surname" bind:value={last_name}>
                    {#if errors && errors.surname}
                        <p class="text-danger">{errors.surname}</p>
                    {/if}
                </div>
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <input class="form-control mb-3" type="email" placeholder="Email" bind:value={email}>
                {#if errors && errors.email}
                    <p class="text-danger">{errors.email}</p>
                {/if}
            </div>
            <div class="form-group">
                <label for="username">Username:</label>
                <input class="form-control mb-3" type="text" placeholder="Username" bind:value={username}>
                {#if errors && errors.username}
                    <p class="text-danger">{errors.username}</p>
                {/if}
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input class="form-control mb-3" type="password" placeholder="Password" bind:value={password}
                       on:input={validatePassword}>
                {#if errors && errors.password}
                    <p class="text-danger">{errors.password}</p>
                {:else if passwordSuccess}
                    <p class="text-success">Password is strong!</p>
                {/if}
            </div>
            <button class="btn btn-primary" type="submit">Register</button>
        </form>
    </div>
</div>