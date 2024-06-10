<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';

    let isAuthenticated = false;
    let userProfile = null;
    let currentPage = '';
    let chatrooms = [];
    let newChatroomName = '';
    let newChatroomDescription = '';
    let newChatroomType = 'private';
    let newChatroomUsers = [];

    async function getAvailableUsers() {
        const response = await fetch('http://localhost:8000/get-available-users/', {
            credentials: 'include'
        });
        const { users } = await response.json();
        return users;
    }

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

                // Fetch chatrooms for the user
                const chatroomsResponse = await fetch('http://localhost:8000/chatroom_list/', {
                    credentials: 'include'
                });
                const chatroomsData = await chatroomsResponse.json();
                chatrooms = chatroomsData.chatrooms;

                if (newChatroomType === 'private') {
                    const availableUsers = await getAvailableUsers();
                    newChatroomUsers = availableUsers.filter(user => user.id !== userProfile.id);
                }
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

    async function createChatroom() {
        try {
            const csrfToken = await getCsrfToken();
            const response = await fetch('http://localhost:8000/create_chatroom/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    name: newChatroomName,
                    description: newChatroomDescription,
                    type: newChatroomType,
                    users: newChatroomUsers
                }),
                credentials: 'include'
            });
            if (response.ok) {
                // Handle successful creation of chatroom
                newChatroomName = '';
                newChatroomDescription = '';
                newChatroomType = 'private';
                newChatroomUsers = [];
            } else {
                console.error('Error creating chatroom:', response.status);
            }
        } catch (error) {
            console.error('Error creating chatroom:', error);
        }
    }

    async function deleteChatroom(chatroomId) {
        try {
            const csrfToken = await getCsrfToken();
            const response = await fetch(`http://localhost:8000/delete_chatroom/${chatroomId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                credentials: 'include'
            });
            if (response.ok) {
                // Handle successful deletion of chatroom
                console.log('Chatroom deleted successfully');
                // You may want to update the chatrooms list here
            } else {
                console.error('Error deleting chatroom:', response.status);
            }
        } catch (error) {
            console.error('Error deleting chatroom:', error);
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

{#if isAuthenticated}
    <div class="chatrooms-container">
        <h2>Create Chatroom</h2>
        <form on:submit|preventDefault={createChatroom}>
            <div class="mb-3">
                <label for="chatroom-name" class="form-label">Chatroom Name:</label>
                <input type="text" class="form-control" id="chatroom-name" bind:value={newChatroomName} required>
            </div>
            <div class="mb-3">
                <label for="chatroom-description" class="form-label">Chatroom Description:</label>
                <textarea class="form-control" id="chatroom-description" bind:value={newChatroomDescription} required></textarea>
            </div>
            {#if newChatroomType === 'private'}
                <div class="mb-3">
                    <label for="selected-users" class="form-label">Select Users:</label>
                    <select class="form-control" id="selected-users" multiple bind:value={newChatroomUsers} required>
                        {#each newChatroomUsers as user}
                            <option value={user.id}>{user.username}</option>
                        {/each}
                    </select>
                </div>
            {/if}
            <div class="mb-3">
                <label for="chatroom-type" class="form-label">Chatroom Type:</label>
                <select class="form-control" id="chatroom-type" bind:value={newChatroomType} required>
                    <option value="private">Private</option>
                    <option value="global">Global</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">Create Chatroom</button>
        </form>
        <h2>Your Chatrooms</h2>
        <ul>
            {#each chatrooms as chatroom}
                {#if chatroom.type === 'global' || (chatroom.type === 'private' && chatroom.creator_id === userProfile.id) || (chatroom.type === 'private' && chatroom.users || [])}
                    <li>
												<a href="/chatroom/{chatroom.id}">{chatroom.name}</a>
                            <button on:click={() => deleteChatroom(chatroom.id)}>Delete Chatroom</button>
                    </li>
                {/if}
            {/each}
        </ul>
    </div>
{/if}