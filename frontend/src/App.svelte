<script lang="ts">
  import { onMount } from 'svelte'

  type HealthResponse = {
    status: string
  }

  const backendBaseUrl = import.meta.env.VITE_BACKEND_URL ?? 'http://localhost:8000'

  let loading = true
  let health: HealthResponse | null = null
  let errorMessage = ''

  async function loadHealthStatus() {
    loading = true
    errorMessage = ''

    try {
      const response = await fetch(`${backendBaseUrl}/health`)

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }

      health = (await response.json()) as HealthResponse
    } catch (error) {
      health = null
      errorMessage = error instanceof Error ? error.message : 'Unknown error'
    } finally {
      loading = false
    }
  }

  onMount(() => {
    void loadHealthStatus()
  })
</script>

<main class="min-h-screen bg-base-200 p-6">
  <section class="mx-auto max-w-2xl space-y-6">
    <div class="card bg-base-100 shadow-md">
      <div class="card-body gap-4">
        <h1 class="card-title text-3xl">Lost and Found Starter</h1>
        <p>
          Minimal monorepo starter for the university database project. The ERD, schema, and lost-and-found
          features will be designed by the team later.
        </p>
      </div>
    </div>

    <div class="card bg-base-100 shadow-md">
      <div class="card-body gap-4">
        <h2 class="card-title text-xl">Backend health check</h2>
        <p class="text-sm">Endpoint: {backendBaseUrl}/health</p>

        {#if loading}
          <span class="loading loading-spinner loading-md" aria-label="Loading health status"></span>
        {:else if errorMessage}
          <div class="alert alert-error" role="alert">
            <span>Could not reach backend: {errorMessage}</span>
          </div>
        {:else if health}
          <div class="alert alert-success" role="status">
            <span>Backend is running (status: {health.status}).</span>
          </div>
        {/if}

        <div>
          <button class="btn btn-outline btn-sm" on:click={loadHealthStatus} type="button">Refresh status</button>
        </div>
      </div>
    </div>
  </section>
</main>
