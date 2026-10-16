<script>
  import { onMount } from 'svelte';

  // State management using Svelte 5 runes ($state)
  let logs = $state([]);
  let newMessage = $state('');
  let loading = $state(false);
  let errorMessage = $state('');

  const API_BASE_URL = 'http://localhost:8000';

  // Read: Fetch all logs via GET request
  async function fetchLogs() {
    loading = true;
    errorMessage = '';
    try {
      const response = await fetch(`${API_BASE_URL}/reference/logs/`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      logs = await response.json();
    } catch (err) {
      errorMessage = `Failed to fetch logs: ${err.message}`;
    } finally {
      loading = false;
    }
  }

  // Write: Create a new log via POST request with JSON payload
  async function createLog(event) {
    event.preventDefault();
    if (!newMessage.trim()) return;

    errorMessage = '';
    try {
      const response = await fetch(`${API_BASE_URL}/reference/logs/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: newMessage.trim() }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Reset form input via two-way binding
      newMessage = '';
      // Refresh log list
      await fetchLogs();
    } catch (err) {
      errorMessage = `Failed to create log: ${err.message}`;
    }
  }

  onMount(() => {
    fetchLogs();
  });
</script>

<!--
  Pico.css automatically styles semantic HTML elements (<article>, <form>, <input>, <table>)
  without requiring manual CSS utility classes.
-->
<article>
  <header>
    <h3>System Logs (Isolated Reference Example)</h3>
    <p><small>Demonstrating two-way binding, loops, and async raw SQL backend communication.</small></p>
  </header>

  {#if errorMessage}
    <p style="color: var(--pico-del-color, #c52f2f);">
      <strong>Error:</strong> {errorMessage}
    </p>
  {/if}

  <!-- Form with two-way data binding (bind:value) -->
  <form onsubmit={createLog}>
    <label for="log-input">
      Log Message
      <input
        type="text"
        id="log-input"
        placeholder="Enter a log event (e.g., 'Lost black wallet at library')"
        bind:value={newMessage}
        required
      />
    </label>
    <button type="submit" aria-busy={loading}>Add Log Entry</button>
  </form>

  <hr />

  <h4>Log History</h4>

  {#if loading && logs.length === 0}
    <p aria-busy="true">Loading logs from database...</p>
  {:else if logs.length === 0}
    <p><em>No logs recorded yet in Microsoft SQL Server. Try creating one above!</em></p>
  {:else}
    <!-- Semantic table styled natively by Pico.css -->
    <div class="overflow-auto">
      <table>
        <thead>
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Message</th>
            <th scope="col">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {#each logs as log (log.id)}
            <tr>
              <th scope="row">{log.id}</th>
              <td>{log.message}</td>
              <td><small>{log.timestamp}</small></td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</article>

