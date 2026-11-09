
import Link from "next/link";

const technologies = [
  "Python",
  "Apache Airflow",
  "PostgreSQL",
  "ClickHouse",
  "Docker",
  "Pandas",
  "FastAPI",
  "SQLAlchemy",
  "Pytest",
];

const pipelineTasks = [
  {
    number: "01",
    name: "Start audit",
    detail: "Create an execution record in PostgreSQL.",
  },
  {
    number: "02",
    name: "Extract",
    detail: "Read customer records from the CSV source.",
  },
  {
    number: "03",
    name: "Validate",
    detail: "Check required fields, duplicates, emails and dates.",
  },
  {
    number: "04",
    name: "Load PostgreSQL",
    detail: "Detect and apply new or modified customer records.",
  },
  {
    number: "05",
    name: "Sync ClickHouse",
    detail: "Replicate changed records into analytical storage.",
  },
  {
    number: "06",
    name: "Verify PostgreSQL",
    detail: "Verify source records using their expected hashes.",
  },
  {
    number: "07",
    name: "Verify ClickHouse",
    detail: "Compare analytical records with PostgreSQL.",
  },
  {
    number: "08",
    name: "Complete audit",
    detail: "Store execution status and synchronization metrics.",
  },
];

const capabilities = [
  {
    title: "Incremental ingestion",
    description:
      "SHA-256 record hashes identify new, changed and unchanged customers. Unchanged records are skipped.",
  },
  {
    title: "Idempotent synchronization",
    description:
      "Repeated processing of the same dataset does not cause unnecessary updates or duplicate logical customer records.",
  },
  {
    title: "Execution audit",
    description:
      "Each Airflow run records its status, source record count, insertions, updates and unchanged record counts.",
  },
  {
    title: "Cross-database verification",
    description:
      "Record-level verification checks expected hashes in both PostgreSQL and ClickHouse.",
  },
];

export default function EnterpriseDataPlatformPage() {
  return (
    <main className="min-h-screen bg-[#090d12] text-white">
      {/* Navigation */}
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-7">
        <Link href="/" className="text-xl font-bold tracking-tight">
          ABDULLA<span className="text-emerald-400">.</span>
        </Link>

        <div className="flex items-center gap-6 text-sm text-gray-400">
          <Link href="/#projects" className="hidden hover:text-white sm:block">
            Projects
          </Link>
          <Link href="/#about" className="hidden hover:text-white sm:block">
            About
          </Link>
          <a
            href="https://github.com/abdullachowdry750/abdulla-portfolio/tree/main/projects/enterprise-data-platform"
            target="_blank"
            rel="noreferrer"
            className="hover:text-emerald-400"
          >
            Source code ↗
          </a>
        </div>
      </nav>

      {/* Hero */}
      <section className="border-b border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <Link
            href="/#projects"
            className="text-sm text-gray-500 transition hover:text-emerald-400"
          >
            ← Back to projects
          </Link>

          <div className="mt-12 flex flex-wrap items-center gap-3">
            <span className="rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-2 text-xs text-emerald-400">
              DATA ENGINEERING
            </span>
            <span className="rounded-full border border-gray-700 px-4 py-2 text-xs text-gray-400">
              Working local implementation
            </span>
          </div>

          <h1 className="mt-8 max-w-4xl text-4xl font-semibold leading-tight tracking-tight md:text-6xl">
            Enterprise Data
            <span className="text-emerald-400"> Platform.</span>
          </h1>

          <p className="mt-8 max-w-3xl text-lg leading-8 text-gray-400">
            A containerized data ingestion and analytics platform that
            orchestrates incremental customer data synchronization across
            PostgreSQL and ClickHouse using Apache Airflow.
          </p>

          <div className="mt-10 flex flex-wrap gap-4">
            <a
              href="https://github.com/abdullachowdry750/abdulla-portfolio/tree/main/projects/enterprise-data-platform"
              target="_blank"
              rel="noreferrer"
              className="rounded-full bg-emerald-400 px-7 py-3 font-medium text-black transition hover:bg-emerald-300"
            >
              View source code ↗
            </a>

            <a
              href="#architecture"
              className="rounded-full border border-gray-700 px-7 py-3 text-gray-300 transition hover:border-white hover:text-white"
            >
              Explore architecture ↓
            </a>
          </div>

          {/* Project metrics */}
          <div className="mt-20 grid gap-4 border-t border-gray-800 pt-8 sm:grid-cols-2 lg:grid-cols-4">
            {[
              { value: "8", label: "Airflow pipeline tasks" },
              { value: "2", label: "Database systems" },
              { value: "SHA-256", label: "Change detection" },
              { value: "5", label: "Synthetic test records" },
            ].map((item) => (
              <div key={item.label}>
                <p className="text-2xl font-semibold">{item.value}</p>
                <p className="mt-2 text-sm text-gray-500">{item.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Overview */}
      <section className="border-b border-gray-800">
        <div className="mx-auto grid max-w-6xl gap-12 px-6 py-24 md:grid-cols-[1.2fr_0.8fr]">
          <div>
            <p className="text-sm tracking-widest text-emerald-400">
              01 / OVERVIEW
            </p>

            <h2 className="mt-6 text-3xl font-semibold">
              Reliable ingestion. Consistent data. Analytical access.
            </h2>

            <p className="mt-6 leading-8 text-gray-400">
              The platform ingests customer data from CSV sources, validates
              records, and synchronizes changes into PostgreSQL. It then
              replicates the relevant records into ClickHouse for analytical
              queries.
            </p>

            <p className="mt-5 leading-8 text-gray-400">
              Apache Airflow coordinates the workflow, handles task retries
              and maintains execution history. FastAPI exposes analytical
              results to the portfolio dashboard.
            </p>
          </div>

          <div className="rounded-2xl border border-gray-800 bg-[#101720] p-8">
            <h3 className="text-lg font-semibold">Engineering objectives</h3>

            <div className="mt-7 space-y-5">
              {[
                "Avoid unnecessary database updates.",
                "Make repeated ingestion safe.",
                "Keep analytical data synchronized.",
                "Verify data consistency across systems.",
                "Maintain execution-level audit history.",
              ].map((objective) => (
                <div key={objective} className="flex gap-3">
                  <span className="text-emerald-400">✓</span>
                  <p className="text-sm leading-6 text-gray-400">
                    {objective}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Architecture */}
      <section id="architecture" className="border-b border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm tracking-widest text-emerald-400">
            02 / ARCHITECTURE
          </p>

          <h2 className="mt-6 text-3xl font-semibold md:text-4xl">
            System architecture
          </h2>

          <p className="mt-5 max-w-3xl leading-8 text-gray-400">
            Airflow orchestrates ingestion and synchronization. PostgreSQL
            acts as the operational source of truth, while ClickHouse
            provides the analytical read layer.
          </p>

          <div className="mt-12 rounded-2xl border border-gray-800 bg-[#101720] p-6 md:p-10">
            <div className="mx-auto max-w-2xl space-y-3">
              <div className="rounded-xl border border-gray-700 bg-[#090d12] p-5 text-center">
                <p className="font-semibold">CSV data source</p>
                <p className="mt-1 text-xs text-gray-500">
                  Customer records
                </p>
              </div>

              <div className="text-center text-emerald-400">↓</div>

              <div className="rounded-xl border border-emerald-400/40 bg-emerald-400/5 p-5 text-center">
                <p className="font-semibold">Apache Airflow</p>
                <p className="mt-1 text-xs text-gray-500">
                  Scheduling · Orchestration · Retries · Audit
                </p>
              </div>

              <div className="text-center text-emerald-400">↓</div>

              <div className="rounded-xl border border-gray-700 bg-[#090d12] p-5 text-center">
                <p className="font-semibold">Python + Pandas</p>
                <p className="mt-1 text-xs text-gray-500">
                  Extraction · Validation · SHA-256 hashing
                </p>
              </div>

              <div className="text-center text-emerald-400">↓</div>

              <div className="grid gap-3 sm:grid-cols-2">
                <div className="rounded-xl border border-blue-400/30 bg-blue-400/5 p-5 text-center">
                  <p className="font-semibold">PostgreSQL</p>
                  <p className="mt-2 text-xs text-gray-500">
                    Operational customer data
                  </p>
                  <p className="mt-2 text-xs text-gray-500">
                    Ingestion audit history
                  </p>
                </div>

                <div className="rounded-xl border border-emerald-400/30 bg-emerald-400/5 p-5 text-center">
                  <p className="font-semibold">ClickHouse</p>
                  <p className="mt-2 text-xs text-gray-500">
                    Analytical customer data
                  </p>
                  <p className="mt-2 text-xs text-gray-500">
                    Aggregations and reporting
                  </p>
                </div>
              </div>

              <div className="pt-4 text-center text-gray-500">↓</div>

              <div className="rounded-xl border border-gray-700 bg-[#090d12] p-5 text-center">
                <p className="font-semibold">FastAPI</p>
                <p className="mt-1 text-xs text-gray-500">
                  Read-only customer analytics API
                </p>
              </div>

              <div className="pt-2 text-center text-emerald-400">↓</div>

              <div className="rounded-xl border border-gray-700 bg-[#090d12] p-5 text-center">
                <p className="font-semibold">Next.js portfolio dashboard</p>
                <p className="mt-1 text-xs text-gray-500">
                  Customer metrics and analytical visualizations
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Workflow */}
      <section className="border-b border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm tracking-widest text-emerald-400">
            03 / ORCHESTRATION
          </p>

          <h2 className="mt-6 text-3xl font-semibold md:text-4xl">
            Airflow workflow
          </h2>

          <p className="mt-5 max-w-3xl leading-8 text-gray-400">
            The customer ingestion DAG separates processing into eight
            sequential tasks. Each task has a defined responsibility,
            and retries are configured for execution failures.
          </p>

          <div className="mt-12 grid gap-4 md:grid-cols-2">
            {pipelineTasks.map((task) => (
              <div
                key={task.number}
                className="flex gap-5 rounded-xl border border-gray-800 bg-[#101720] p-6"
              >
                <span className="text-lg font-semibold text-emerald-400">
                  {task.number}
                </span>

                <div>
                  <h3 className="font-semibold">{task.name}</h3>
                  <p className="mt-2 text-sm leading-6 text-gray-400">
                    {task.detail}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Incremental ingestion */}
      <section className="border-b border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm tracking-widest text-emerald-400">
            04 / INCREMENTAL PROCESSING
          </p>

          <h2 className="mt-6 text-3xl font-semibold md:text-4xl">
            Detect changes, not just records
          </h2>

          <p className="mt-5 max-w-3xl leading-8 text-gray-400">
            Each customer record receives a deterministic SHA-256 hash
            calculated from its relevant fields. The hash is compared with
            the previously stored value to determine the required action.
          </p>

          <div className="mt-10 grid gap-4 md:grid-cols-3">
            {[
              {
                title: "New records",
                value: "INSERT",
                description:
                  "Customers not yet present in the target database.",
              },
              {
                title: "Changed records",
                value: "UPDATE",
                description:
                  "Customers whose current record hash differs from the stored hash.",
              },
              {
                title: "Unchanged records",
                value: "SKIP",
                description:
                  "Customers with matching hashes and no required data update.",
              },
            ].map((item) => (
              <div
                key={item.title}
                className="rounded-2xl border border-gray-800 bg-[#101720] p-7"
              >
                <p className="text-sm text-gray-400">{item.title}</p>
                <h3 className="mt-4 text-2xl font-semibold text-emerald-400">
                  {item.value}
                </h3>
                <p className="mt-4 text-sm leading-7 text-gray-500">
                  {item.description}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-8 rounded-xl border border-gray-800 bg-[#101720] p-7">
            <h3 className="font-semibold">ClickHouse versioning</h3>
            <p className="mt-3 leading-7 text-gray-400">
              The analytical table uses ReplacingMergeTree with a version
              column. Queries use FINAL when the latest logical version of
              each customer is required.
            </p>
          </div>
        </div>
      </section>

      {/* Capabilities */}
      <section className="border-b border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm tracking-widest text-emerald-400">
            05 / ENGINEERING
          </p>

          <h2 className="mt-6 text-3xl font-semibold md:text-4xl">
            Engineering capabilities
          </h2>

          <div className="mt-12 grid gap-5 md:grid-cols-2">
            {capabilities.map((capability) => (
              <div
                key={capability.title}
                className="rounded-2xl border border-gray-800 bg-[#101720] p-7"
              >
                <h3 className="text-lg font-semibold">
                  {capability.title}
                </h3>

                <p className="mt-4 leading-7 text-gray-400">
                  {capability.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Validation and analytics */}
      <section className="border-b border-gray-800">
        <div className="mx-auto grid max-w-6xl gap-12 px-6 py-24 md:grid-cols-2">
          <div>
            <p className="text-sm tracking-widest text-emerald-400">
              06 / VALIDATION
            </p>

            <h2 className="mt-6 text-3xl font-semibold">
              Testing and verification
            </h2>

            <p className="mt-5 leading-8 text-gray-400">
              The implementation includes automated tests for customer
              validation, deterministic hashing, incremental database
              operations, record-level verification and audit status
              handling.
            </p>

            <p className="mt-5 leading-8 text-gray-400">
              PostgreSQL and ClickHouse synchronization were tested with
              new, modified, unchanged and repeated customer records.
            </p>
          </div>

          <div>
            <p className="text-sm tracking-widest text-emerald-400">
              07 / ANALYTICS
            </p>

            <h2 className="mt-6 text-3xl font-semibold">
              Analytical access
            </h2>

            <p className="mt-5 leading-8 text-gray-400">
              ClickHouse powers customer summary metrics, city-wise
              distribution and monthly signup aggregations. These results
              are exposed through a FastAPI endpoint and displayed on the
              portfolio homepage.
            </p>

            <Link
              href="/#analytics"
              className="mt-7 inline-block text-sm font-medium text-emerald-400 transition hover:text-emerald-300"
            >
              View live analytics section ↗
            </Link>
          </div>
        </div>
      </section>

      {/* Technology stack */}
      <section className="border-b border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm tracking-widest text-emerald-400">
            08 / TECHNOLOGY
          </p>

          <h2 className="mt-6 text-3xl font-semibold">
            Technology stack
          </h2>

          <div className="mt-10 flex flex-wrap gap-3">
            {technologies.map((technology) => (
              <span
                key={technology}
                className="rounded-lg border border-gray-800 bg-[#101720] px-5 py-3 text-sm text-gray-300"
              >
                {technology}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer>
        <div className="mx-auto flex max-w-6xl flex-col justify-between gap-6 px-6 py-12 md:flex-row md:items-center">
          <div>
            <p className="font-semibold">Enterprise Data Platform</p>
            <p className="mt-2 text-sm text-gray-500">
              Built with Python, Airflow, PostgreSQL and ClickHouse.
            </p>
          </div>

          <div className="flex flex-wrap gap-6 text-sm text-gray-400">
            <Link href="/#projects" className="hover:text-white">
              All projects
            </Link>

            <a
              href="https://github.com/abdullachowdry750/abdulla-portfolio/tree/main/projects/enterprise-data-platform"
              target="_blank"
              rel="noreferrer"
              className="hover:text-emerald-400"
            >
              GitHub ↗
            </a>

            <a
              href="mailto:abdullachowdry@gmail.com"
              className="hover:text-white"
            >
              Contact ↗
            </a>
          </div>
        </div>
      </footer>
    </main>
  );
}