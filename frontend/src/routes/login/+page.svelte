<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">

<script>
    import { goto } from "$app/navigation";

    let username = '';
    let password = '';
    let errors = {};

    let handleSubmit = () => {
        const endpoint = 'http://localhost:8000/login/';
        const requestOptions = {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username, password: password })
        }

        fetch(endpoint, requestOptions)
            .then(response => response.json().then(data => ({ status: response.status, body: data })))
            .then(data => {
                if (data.status === 200) {
                    goto('/login/home/');
                } else {
                    errors = data.body;
                    console.log(data);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
</script>

<div class="container">
    <div class="row">
        <div class="col-12 col-md-4">
            <h2 class="my-4">Login</h2>
            <form on:submit|preventDefault={handleSubmit} class="needs-validation" novalidate>
                <div class="form-group">
                    <label for="username">Username</label>
                    <input class="form-control mb-3 {errors.username ? 'is-invalid' : ''}" type="text"
                           bind:value={username} id="username" required>
                    {#if errors.username}
                        <div class="invalid-feedback">Invalid username</div>
                    {/if}
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input class="form-control mb-3 {errors.password ? 'is-invalid' : ''}" type="password"
                           bind:value={password} id="password" required>
                    {#if errors.password}
                        <div class="invalid-feedback">Invalid password</div>
                    {/if}
                </div>
                <button class="btn btn-primary" type="submit">Login</button>
            </form>
        </div>
    </div>
</div>