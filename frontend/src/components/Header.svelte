<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';

    let isAuthenticated = false;
    let userProfile = null;
    let currentPage = '';

    onMount(async () => {
        try {
            const response = await fetch('http://localhost:8000/check-login/', {
                credentials: 'include'
            });
            const data = await response.json();
            isAuthenticated = data.message === 'User is logged in';

            if (isAuthenticated) {
                const profileResponse = await fetch('http://localhost:8000/user-profile/', {
                    credentials: 'include'
                });
                userProfile = await profileResponse.json();
            }
        } catch (error) {
            console.error('Error checking login status:', error);
        }
    });

    $: {
        currentPage = $page.url.pathname;
    }

    async function navigateToHome() {
        await goto('/');
    }

    async function navigateToRegister() {
        await goto('/register');
    }

    async function navigateToLogin() {
        await goto('/login');
    }

    async function navigateToProfile() {
        await goto('/profile');
    }

    async function getCsrfToken() {
        const response = await fetch('http://localhost:8000/get-csrf-token/', {
            credentials: 'include'
        });
        const { csrfToken } = await response.json();
        return csrfToken;
    }

    async function logout() {
        try {
            const csrfToken = await getCsrfToken();
            const response = await fetch('http://localhost:8000/logout/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                credentials: 'include'
            });

            if (response.ok) {
                document.cookie = 'csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                isAuthenticated = false;
                userProfile = null;
                await goto('/');
            } else {
                console.error('Error logging out:', response.status);
            }
        } catch (error) {
            console.error('Error during logout:', error);
        }
    }
</script>
<style>
    @import "../../static/whisperer.css";
</style>
<header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark navbar-vertical">
        <ul class="navbar-nav">
            {#if isAuthenticated && userProfile}
                {#if currentPage !== '/profile'}
                    <li class="nav-item">
                        <button class="btn btn-link nav-link" on:click={navigateToProfile}>
                            {userProfile.username}
                        </button>
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-link nav-link" on:click={logout}>Logout</button>
                    </li>
                {:else}
                    <li class="nav-item">
                        <button class="btn btn-link nav-link" on:click={navigateToHome}>Home</button>
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-link nav-link" on:click={logout}>Logout</button>
                    </li>
                {/if}
            {:else}
                {#if currentPage === '/register'}
                    <li class="nav-item">
                        <button class="btn btn-link nav-link" on:click={navigateToHome}>Home</button>
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-link nav-link" on:click={navigateToLogin}>Login</button>
                    </li>
                {:else if currentPage === '/login'}
                    <li class="nav-item">
                        <button class="btn btn-link nav-link" on:click={navigateToHome}>Home</button>
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-link nav-link" on:click={navigateToRegister}>Register</button>
                    </li>
                {:else}
                    <li class="nav-item">
                        <button class="btn btn-link nav-link" on:click={navigateToRegister}>Register</button>
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-link nav-link" on:click={navigateToLogin}>Login</button>
                    </li>
                {/if}
            {/if}
        </ul>
    </nav>
</header>