<script>
	import { onMount } from 'svelte';
	import Header from '../../components/Header.svelte';

	let chatroomId = '';
	let chatroomName = '';
	let messages = [];
	let newMessage = '';

	async function getChatroomMessages() {
		const response = await fetch(`/chatroom/${chatroomId}/messages/`, {
			credentials: 'include'
		});
		const data = await response.json();
		return data.messages;
	}

	async function sendMessage() {
		try {
			const response = await fetch(`/chatroom/${chatroomId}/send_message/`, {
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
			chatroomId = window.chatroomId;
			chatroomName = window.chatroomName;
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