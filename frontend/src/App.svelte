<script>
  import ReferenceLog from './lib/reference/ReferenceLog.svelte';
</script>

<main class="container">
  <header style="margin-bottom: 2rem;">
    <hgroup>
      <h1>Lost & Found</h1>
      <p>University Database Project Starter Template</p>
    </hgroup>
    <nav>
      <ul>
        <li><strong>Status:</strong> Architecture Skeleton Ready</li>
      </ul>
      <ul>
        <li><a href="#reference-section">Jump to Reference Example</a></li>
      </ul>
    </nav>
  </header>

  <section>
    <article>
      <h2>Project Architecture Guidelines</h2>
      <p>
        Welcome to the starter template. Here is how your team should organize the database project:
      </p>
      <ul>
        <li><strong>Backend:</strong> FastAPI with raw <code>pymssql</code> driver and pure JSON responses.</li>
        <li><strong>Database Layer:</strong> All table definitions (DDL) and queries (DML) MUST use explicit, raw T-SQL strings connected to Microsoft SQL Server. No ORMs (like SQLAlchemy or SQLModel).</li>
        <li><strong>Pydantic:</strong> Used strictly for parsing incoming JSON request bodies (DTOs) and passing parameters safely into raw SQL statements.</li>
        <li><strong>Frontend:</strong> Decoupled Svelte SPA styled entirely with semantic Pico.css elements.</li>
      </ul>
    </article>
  </section>

  <section id="reference-section" style="margin-top: 2rem;">
    <!-- Isolated Reference Example Component -->
    <ReferenceLog />
  </section>
</main>

<style>
  main {
    padding-top: 2rem;
    padding-bottom: 4rem;
  }
</style>
