<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import Header from '../../components/Header.svelte';

	let chatroomId = '';
	let chatroomName = '';
	let messages = [];
	let newMessage = '';

	async function getChatroomMessages() {
		const response = await fetch(`http://localhost:8000/chatroom/${chatroomId}/`, {
			credentials: 'include'
		});
		const { messages } = await response.json();
		return messages;
	}

	async function sendMessage() {
		try {
			const response = await fetch(`http://localhost:8000/send_message/${chatroomId}/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					text: newMessage
				}),
				credentials: 'include'
			});
			if (response.ok) {
				// Handle successful message sending
				newMessage = '';
				messages = await getChatroomMessages();
			} else {
				console.error('Error sending message:', response.status);
			}
		} catch (error) {
			console.error('Error sending message:', error);
		}
	}

	onMount(async () => {
		try {
			chatroomId = page.url.pathname.split('/')[2];
			chatroomName = await fetch(`http://localhost:8000/chatroom/${chatroomId}/`).then(response => response.json()).then(data => data.name);
			messages = await getChatroomMessages();
		} catch (error) {
			console.error('Error loading chatroom:', error);
		}
	});
</script>

<Header />

<h2>{chatroomName}</h2>
<ul>
	{#each messages as message}
		<li>
			<p>{message.text}</p>
			<p>by {message.user.username}</p>
		</li>
	{/each}
</ul>

<form on:submit|preventDefault={sendMessage}>
	<input type="text" bind:value={newMessage} placeholder="Type a message...">
	<button type="submit">Send</button>
</form>