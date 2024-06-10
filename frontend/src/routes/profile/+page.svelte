<script>
  import { onMount } from 'svelte';
  import Header from '../../components/Header.svelte';

  let userProfile = null;
  let editMode = false;
  let newUsername = '';
  let newEmail = '';
  let newBio = '';
  let newProfilePicture = null;
  let showDeleteConfirmation = false;
  let showPasswordChange = false;
  let currentPassword = '';
  let newPassword = '';
  let newPasswordConfirm = '';
  let passwordChangeError = '';
  let firstName = '';
  let lastName = '';

  onMount(async () => {
    try {
      const response = await fetch('http://localhost:8000/user-profile/', { credentials: 'include' });
      const data = await response.json();
      console.log('Profile Picture URL:', data.profile_picture);
      // Log the profile picture URL
      userProfile = data;
      newUsername = data.username;
      newEmail = data.email;
      newBio = data.bio;
      if (data.profile_picture) {
        const profilePictureResponse = await fetch(`http://localhost:8000${data.profile_picture}`, { credentials: 'include' });
        const profilePicture = await profilePictureResponse.blob();
        userProfile.profile_picture = URL.createObjectURL(profilePicture);
      } else {
        userProfile.profile_picture = 'https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_640.png';
      }
      firstName = data.first_name;
      lastName = data.last_name;
    } catch (error) {
      console.error('Error fetching user profile:', error);
    }
  });

  async function getCsrfToken() {
    const response = await fetch('http://localhost:8000/get-csrf-token/', { credentials: 'include' });
    const { csrfToken } = await response.json();
    return csrfToken;
  }

  async function updateProfile() {
    try {
      const csrfToken = await getCsrfToken();
      const formData = new FormData();
      formData.append('username', newUsername);
      formData.append('email', newEmail);
      formData.append('bio', newBio);
      if (newProfilePicture instanceof File) {
        formData.append('profile_picture', newProfilePicture);
      }
      const response = await fetch('http://localhost:8000/user-profile/', { method: 'PUT', headers: { 'X-CSRFToken': csrfToken }, body: formData, credentials: 'include' });
      if (response.ok) {
        userProfile = await response.json();
        editMode = false;
      } else {
        console.error('Error updating profile:', response.status);
      }
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  }

  async function deleteAccount() {
    try {
      const confirmed = confirm('Are you sure you want to delete your account? This action cannot be undone.');
      if (confirmed) {
        const csrfToken = await getCsrfToken();
        const response = await fetch('http://localhost:8000/delete-account/', { method: 'DELETE', headers: { 'X-CSRFToken': csrfToken }, credentials: 'include' });
        if (response.ok) {
          document.cookie = 'csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
          window.location.href = '/';
        } else {
          console.error('Error deleting account:', response.status);
        }
      }
    } catch (error) {
      console.error('Error deleting account:', error);
    }
  }

  async function changePassword() {
    try {
      if (newPassword !== newPasswordConfirm) {
        passwordChangeError = 'Passwords do not match.';
        return;
      }
      const csrfToken = await getCsrfToken();
      const formData = new FormData();
      formData.append('old_password', currentPassword);
      formData.append('new_password1', newPassword);
      formData.append('new_password2', newPasswordConfirm);
      const response = await fetch('http://localhost:8000/change-password/', { method: 'POST', headers: { 'X-CSRFToken': csrfToken }, body: formData, credentials: 'include' });
      if (response.ok) {
        document.cookie = 'csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        showPasswordChange = false;
        newPassword = '';
        newPasswordConfirm = '';
        passwordChangeError = '';
        window.location.href = '/';
      } else {
        const data = await response.json();
        if (data.new_password2 && data.new_password2.includes('This password is too common.')) {
          passwordChangeError = 'Password should be at least 8 characters long.';
        } else if (data.new_password2 && data.new_password2.includes('The password is too similar to the username.')) {
          passwordChangeError = 'Password is too similar to the username.';
        } else {
          passwordChangeError = 'Error changing password. Please try again.';
          console.error('Error changing password:', response.status);
        }
      }
    } catch (error) {
      passwordChangeError = 'Error changing password. Please try again.';
      console.error('Error changing password:', error);
    }
  }
</script>

<main class="container my-5">
  <Header />
  <h1>User Profile</h1>
  {#if userProfile}
    {#if editMode}
      <form on:submit|preventDefault={updateProfile}>
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" class="form-control" id="username" bind:value={newUsername} required>
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input type="email" class="form-control" id="email" bind:value={newEmail} required>
        </div>
        <div class="mb-3">
          <label for="bio" class="form-label">Bio</label>
          <textarea class="form-control" id="bio" rows="3" bind:value={newBio}></textarea>
        </div>
        <div class="mb-3">
          <label for="profile-picture" class="form-label">Profile Picture</label>
          <input type="file" class="form-control" id="profile-picture" on:change={(e) => newProfilePicture = e.target.files[0]}>
        </div>
        <button type="submit" class="btn btn-primary">Save</button>
        <button type="button" class="btn btn-secondary" on:click={() => editMode = false}>Cancel</button>
      </form>
    {:else}
      <div class="d-flex align-items-center mb-3">
        {#if userProfile.profile_picture}
          <img src={new URL(userProfile.profile_picture, 'http://localhost:8000').href} alt="Profile Picture" class="img-thumbnail me-3" aria-hidden="true" width="100" height="100" style="margin-right: 20px; border-radius: 50%; ">
        {:else}
          <img src="https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_640.png" alt="Default Profile Picture" class="img-thumbnail me-3" aria-hidden="true" width="100" height="100" style="margin-right: 20px; border-radius: 50%;">
        {/if}
        <h2>{userProfile.username}</h2>
      </div>
      <p>First Name: {firstName}</p>
      <p>Last Name: {lastName}</p>
      <p>Email: {userProfile.email}</p>
      <p>Bio: {userProfile.bio}</p>

      <button class="btn btn-primary" on:click={() => editMode = true}>Edit Profile</button>
      <button class="btn btn-danger" on:click={() => showDeleteConfirmation = true}>Delete Account</button>
      <button class="btn btn-secondary" on:click={() => showPasswordChange = true}>Change Password</button>
    {/if}
  {:else}
    <p>Loading profile...</p>
  {/if}

  {#if showDeleteConfirmation}
    <div class="alert alert-danger" role="alert">
      Are you sure you want to delete your account? <button type="button" class="btn btn-danger" on:click={deleteAccount}>Confirm</button>
      <button type="button" class="btn btn-secondary" on:click={() => showDeleteConfirmation = false}>Cancel</button>
    </div>
  {/if}

  {#if showPasswordChange}
    <form on:submit|preventDefault={changePassword}>
      <div class="mb-3">
        <label for="current-password" class="form-label">Current Password</label>
        <input type="password" class="form-control" id="current-password" bind:value={currentPassword} required>
      </div>
      <div class="mb-3">
        <label for="new-password" class="form-label">New Password</label>
        <input type="password" class="form-control" id="new-password" bind:value={newPassword} required>
      </div>
      <div class="mb-3">
        <label for="new-password-confirm" class="form-label">Confirm New Password</label>
        <input type="password" class="form-control" id="new-password-confirm" bind:value={newPasswordConfirm} required>
      </div>
      {#if passwordChangeError}
        <div class="alert alert-danger" role="alert">{passwordChangeError}</div>
      {/if}
      <button type="submit" class="btn btn-primary">Change Password</button>
      <button type="button" class="btn btn-secondary" on:click={() => showPasswordChange = false}>Cancel</button>
    </form>
  {/if}
</main>