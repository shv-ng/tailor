<script lang="ts">
  import { goto } from '$app/navigation';
  import { PUBLIC_API_BASE_URL } from '$env/static/public';
  import { Button } from '$lib/components/ui/button';
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';
  import { Tabs, TabsContent, TabsList, TabsTrigger } from '$lib/components/ui/tabs';

  let username = $state('');
  let password = $state('');
  let confirmPassword = $state('');
  let error = $state('');
  let isLoading = $state(false);

  $effect(() => {
    if (localStorage.getItem('access')) {
      goto('/home');
    }
  });

  async function handleSubmit(type: 'login' | 'register') {
    error = '';
    isLoading = true;

    if (type === 'register' && password !== confirmPassword) {
      error = 'Passwords do not match';
      isLoading = false;
      return;
    }

    try {
      const url = `${PUBLIC_API_BASE_URL}${type === 'login' ? '/api/auth/token/' : '/api/auth/register/'}`;
      const body = { username, password };

      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      if (!response.ok) throw new Error(type === 'login' ? 'Invalid credentials' : 'Registration failed');

      if (type === 'login') {
        const data = await response.json();
        localStorage.setItem('access', data.access);
        localStorage.setItem('refresh', data.refresh);
        localStorage.setItem('user_email', username); // Store username as user_email
        goto('/home');
      } else {
        alert('Registered successfully. Please login.');
      }
    } catch (e: any) {
      error = e.message;
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="flex min-h-screen items-center justify-center p-4">
  <Card class="w-full max-w-sm bg-zinc-900 border-zinc-800">
    <CardHeader>
      <CardTitle>Welcome</CardTitle>
      <CardDescription>Authenticate to access your workspace.</CardDescription>
    </CardHeader>
    <CardContent>
      <Tabs defaultValue="login" class="w-full">
        <TabsList class="grid w-full grid-cols-2">
          <TabsTrigger value="login">Login</TabsTrigger>
          <TabsTrigger value="register">Register</TabsTrigger>
        </TabsList>
        <TabsContent value="login" class="space-y-4 pt-4">
          <form onsubmit={(e) => { e.preventDefault(); handleSubmit('login'); }} class="space-y-4">
            <div class="space-y-2">
              <Label for="username">Username</Label>
              <Input id="username" bind:value={username} required />
            </div>
            <div class="space-y-2">
              <Label for="password">Password</Label>
              <Input id="password" type="password" bind:value={password} required />
            </div>
            {#if error} <p class="text-sm text-destructive">{error}</p> {/if}
            <Button type="submit" class="w-full" disabled={isLoading}>
              {isLoading ? 'Processing...' : 'Login'}
            </Button>
          </form>
        </TabsContent>
        <TabsContent value="register" class="space-y-4 pt-4">
          <form onsubmit={(e) => { e.preventDefault(); handleSubmit('register'); }} class="space-y-4">
            <div class="space-y-2">
              <Label for="reg-username">Username</Label>
              <Input id="reg-username" bind:value={username} required />
            </div>
            <div class="space-y-2">
              <Label for="reg-password">Password</Label>
              <Input id="reg-password" type="password" bind:value={password} required />
            </div>
            <div class="space-y-2">
              <Label for="reg-confirm">Confirm Password</Label>
              <Input id="reg-confirm" type="password" bind:value={confirmPassword} required />
            </div>
            {#if error} <p class="text-sm text-destructive">{error}</p> {/if}
            <Button type="submit" class="w-full" disabled={isLoading}>
              {isLoading ? 'Processing...' : 'Register'}
            </Button>
          </form>
        </TabsContent>
      </Tabs>
    </CardContent>
  </Card>
</div>
