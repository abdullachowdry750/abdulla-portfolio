import {
  getProfile,
  getProjects,
  getCustomerAnalytics,
} from "@/lib/api";
import Link from "next/link";
import Image from "next/image";

const skills = [
  "Python", "FastAPI", "Apache Airflow", "PostgreSQL",
  "ClickHouse", "Kafka", "GCP", "Docker",
  "LLMs", "RAG", "MLflow", "System Design",
];

export default async function Home() {
  const profile = await getProfile();
  const projectData = await getProjects();
  const analytics = await getCustomerAnalytics();

  const formatDate = (value: string | null) =>
  value
    ? new Date(`${value}T00:00:00Z`).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
        timeZone: "UTC",
      })
    : "—";

  const maxCityCount = Math.max(
    ...analytics.city_distribution.map((item) => item.customer_count),
    1
  );

  const projects = projectData.projects;
  return (
    <main className="min-h-screen bg-[#090d12] text-white">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-7">
        <a href="/" className="flex items-center gap-3">
          <Image
            src="/logo.svg"
            alt=""
            width={38}
            height={38}
            priority
          />
          <span className="text-lg font-bold tracking-tight">
            ABDULLA CHOWDRY<span className="text-emerald-400">.</span>
          </span>
        </a>
          <div className="hidden gap-8 text-sm text-gray-400 md:flex">
            <a href="#about" className="hover:text-white">About</a>
            <a href="#expertise" className="hover:text-white">Expertise</a>
            <a href="#projects" className="hover:text-white">Projects</a>
            <a href="#analytics" className="hover:text-white">Analytics</a>
            <a href="#experience" className="hover:text-white">Experience</a>
            <a href="#resume" className="hover:text-white">Resume</a>
          </div>
        <a
          href="mailto:abdullachowdry@gmail.com"
          className="rounded-full border border-gray-700 px-5 py-2 text-sm hover:border-emerald-400"
        >
          Contact ↗
        </a>
      </nav>

  <section className="mx-auto grid min-h-[650px] max-w-6xl grid-cols-1 items-center gap-14 px-6 py-20 lg:grid-cols-[minmax(0,1.35fr)_minmax(320px,0.8fr)] lg:gap-16">

    {/* Introduction */}
    <div className="max-w-3xl">
      <p className="mb-6 text-sm font-medium tracking-[0.25em] text-emerald-400">
        AI ENGINEERING · DATA PLATFORMS · CLOUD
      </p>

      <h1 className="text-5xl font-semibold leading-tight tracking-tight md:text-6xl">
        Engineering intelligent systems
        <span className="text-emerald-400"> at scale.</span>
      </h1>

      <p className="mt-8 max-w-2xl text-lg leading-8 text-gray-400">
        I'm Abdulla Chowdry, an AI and Data Engineer focused on
        designing scalable data platforms, production-ready AI
        systems and reliable engineering infrastructure.
      </p>

      <p className="mt-4 text-sm text-gray-500">
        Data Science Lead · Impact Big Data Analytics · Bengaluru, India
      </p>
      <p className="mt-2 text-sm text-gray-500">
        Open to opportunities in India and internationally.
      </p>

      <div className="mt-10 flex flex-wrap gap-4">
        <a href="#projects"
          className="rounded-full bg-emerald-400 px-7 py-3 font-medium text-black hover:bg-emerald-300">
          Explore my work ↗
        </a>

        <a href="#about"
          className="rounded-full border border-gray-700 px-7 py-3 hover:border-white">
          More about me
        </a>

        <a
          href="/resume.pdf"
          download="Abdulla_Chowdry_Resume.pdf"
          className="rounded-full border border-emerald-400/40 px-7 py-3 text-emerald-400 hover:bg-emerald-400/10"
        >
          Download Resume ↓
        </a>
      </div>

      <div className="mt-6 flex flex-wrap gap-6 text-sm text-gray-400">
        <a
          href="https://www.linkedin.com/in/chowdry-abdulla-178484156/"
          target="_blank"
          rel="noopener noreferrer"
          className="transition hover:text-emerald-400"
        >
          LinkedIn ↗
        </a>
        <a
          href="https://github.com/abdullachowdry750"
          target="_blank"
          rel="noopener noreferrer"
          className="transition hover:text-emerald-400"
        >
          GitHub ↗
        </a>
        <a
          href="mailto:abdullachowdry@gmail.com"
          className="transition hover:text-emerald-400"
        >
          Email ↗
        </a>
      </div>

      <div className="mt-16 grid max-w-2xl grid-cols-2 gap-8 border-t border-gray-800 pt-8 md:grid-cols-3">
        <div>
          <p className="text-3xl font-semibold">5+</p>
          <p className="mt-2 text-sm text-gray-500">Years in engineering</p>
        </div>
        <div>
          <p className="text-3xl font-semibold">AI + Data</p>
          <p className="mt-2 text-sm text-gray-500">Core specialization</p>
        </div>
        <div>
          <p className="text-3xl font-semibold">GCP</p>
          <p className="mt-2 text-sm text-gray-500">Cloud ecosystem</p>
        </div>
      </div>
    </div>

    {/* Profile photograph */}
    <div className="relative mx-auto w-full max-w-[460px] lg:max-w-none">
      <Image
        src="/images/profile.webp"
        alt="Abdulla Chowdry - AI and Data Engineer"
        width={900}
        height={900}
        priority
        sizes="(max-width: 1024px) 85vw, 460px"
        className="aspect-[4/5] w-full rounded-2xl object-cover object-[center_28%]"
      />
    </div>

  </section>

      <section id="about" className="border-t border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm tracking-widest text-emerald-400">01 / ABOUT</p>
          <h2 className="mt-6 max-w-3xl text-3xl font-semibold md:text-4xl">
            Building the infrastructure behind intelligent applications.
          </h2>
          <p className="mt-8 max-w-3xl leading-8 text-gray-400">
            My engineering interests span data infrastructure,
            distributed systems, machine learning operations and
            applied AI. I enjoy solving complex engineering problems
            and turning ideas into reliable production systems.
          </p>
        </div>
      </section>

      <section id="expertise" className="border-t border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm tracking-widest text-emerald-400">02 / EXPERTISE</p>
          <h2 className="mt-6 text-3xl font-semibold">Technology & tools</h2>
          <div className="mt-10 flex flex-wrap gap-3">
            {skills.map((skill) => (
              <span key={skill}
                className="rounded-lg border border-gray-800 bg-[#101720] px-5 py-3 text-sm text-gray-300">
                {skill}
              </span>
            ))}
          </div>
        </div>
      </section>

      <section id="projects" className="border-t border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm tracking-widest text-emerald-400">03 / SELECTED WORK</p>
          <h2 className="mt-6 text-3xl font-semibold md:text-4xl">
            Engineering projects
          </h2>
          <div className="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {projects.map((project) => (
              <article
                key={project.id}
                className="flex h-full flex-col rounded-2xl border border-gray-800 bg-[#101720] p-7 transition duration-300 hover:-translate-y-1 hover:border-emerald-400/50"
              >
                <p className="text-sm text-emerald-400">
                  {String(project.id).padStart(2, "0")} / {project.category}
                </p>

                <h3 className="mt-8 text-2xl font-semibold">
                  {project.name}
                </h3>

                <p className="mt-4 leading-7 text-gray-400">
                  {project.description}
                </p>

                <div className="mt-8 flex flex-wrap gap-2">
                  {project.stack.map((item) => (
                    <span
                      key={item}
                      className="rounded-full bg-gray-800 px-3 py-1 text-xs text-gray-300"
                    >
                      {item}
                    </span>
                  ))}
                </div>
                <div className="mt-auto pt-8">
                  <p className="text-sm text-gray-500">
                    {project.status}
                  </p>

                  {project.id === 1 && (
                    <Link
                      href="/projects/enterprise-data-platform"
                      className="mt-5 inline-flex items-center gap-2 text-sm font-medium text-emerald-400 transition hover:text-emerald-300"
                    >
                      Explore case study <span>↗</span>
                    </Link>
                  )}
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="analytics" className="border-t border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm tracking-widest text-emerald-400">
            04 / LIVE DATA PLATFORM
          </p>

          <div className="mt-6 flex flex-col justify-between gap-4 md:flex-row md:items-end">
            <div>
              <h2 className="text-3xl font-semibold md:text-4xl">
                Customer Analytics
              </h2>
              <p className="mt-3 text-gray-400">
                Analytical insights powered by PostgreSQL, ClickHouse and FastAPI.
              </p>
            </div>

            <span className="w-fit rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-2 text-xs text-emerald-400">
              ● Analytics API Connected
            </span>
          </div>

          {/* Summary metrics */}
          <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {[
              {
                label: "Total customers",
                value: analytics.summary.total_customers,
              },
              {
                label: "Unique cities",
                value: analytics.summary.unique_cities,
              },
              {
                label: "First signup",
                value: formatDate(analytics.summary.first_signup),
              },
              {
                label: "Latest signup",
                value: formatDate(analytics.summary.latest_signup),
              },
            ].map((metric) => (
              <div
                key={metric.label}
                className="rounded-2xl border border-gray-800 bg-[#101720] p-6"
              >
                <p className="text-sm text-gray-500">{metric.label}</p>
                <p className="mt-4 text-2xl font-semibold text-white">
                  {metric.value}
                </p>
              </div>
            ))}
          </div>

          {/* City distribution */}
          <div className="mt-8 grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-gray-800 bg-[#101720] p-8">
              <h3 className="text-xl font-semibold">
                Customers by city
              </h3>

              <p className="mt-2 text-sm text-gray-500">
                Geographic distribution of customers
              </p>

              <div className="mt-8 space-y-6">
                {analytics.city_distribution.map((item) => (
                  <div key={item.city}>
                    <div className="mb-2 flex justify-between text-sm">
                      <span className="text-gray-300">{item.city}</span>
                        <span className="text-gray-400">
                          {item.customer_count} (
                          {Math.round(
                            (item.customer_count /
                              Math.max(analytics.summary.total_customers, 1)) * 100
                          )}%)
                        </span>
                    </div>

                    <div className="h-2 overflow-hidden rounded-full bg-gray-800">
                      <div
                        className="h-full rounded-full bg-emerald-400"
                        style={{
                          width: `${(item.customer_count / Math.max(analytics.summary.total_customers, 1)) * 100}%`,
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Monthly signups */}
            <div className="rounded-2xl border border-gray-800 bg-[#101720] p-8">
              <h3 className="text-xl font-semibold">
                Monthly signups
              </h3>

              <p className="mt-2 text-sm text-gray-500">
                Customer acquisition over time
              </p>

              <div className="mt-8 space-y-6">
                {analytics.monthly_signups.map((item) => (
                  <div key={item.signup_month}>
                    <div className="mb-2 flex justify-between text-sm">
                      <span className="text-gray-300">
                        {new Date(item.signup_month).toLocaleDateString(
                          "en-US",
                          { month: "short", year: "numeric", timeZone: "UTC" }
                        )}
                      </span>

                      <span className="text-gray-400">
                        {item.new_customers} customers
                      </span>
                    </div>

                    <div className="h-2 overflow-hidden rounded-full bg-gray-800">
                      <div
                        className="h-full rounded-full bg-emerald-400"
                        style={{
                          width: `${
                            (item.new_customers /
                              Math.max(
                                ...analytics.monthly_signups.map(
                                  (entry) => entry.new_customers
                                ),
                                1
                              )) * 100
                          }%`,
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <p className="mt-6 text-xs text-gray-600">
            Demonstration dataset · Analytics queried from ClickHouse through FastAPI.
          </p>
        </div>
      </section>

      <section id="experience" className="border-t border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm tracking-widest text-emerald-400">05 / EXPERIENCE</p>
          <h2 className="mt-6 text-3xl font-semibold">Professional journey</h2>
          <div className="mt-10 border-l border-gray-700 pl-6">
            <p className="text-xl font-semibold">Data Science Lead</p>
            <p className="mt-2 text-gray-400">Impact Big Data Analytics</p>
            <p className="mt-2 text-sm text-gray-500">June 2024 — Present</p>
          </div>
          <div className="mt-10 border-l border-gray-700 pl-6">
            <p className="text-xl font-semibold">Senior Data Scientist</p>
            <p className="mt-2 text-gray-400">Impact Big Data Analytics</p>
            <p className="mt-2 text-sm text-gray-500">September 2023 — June 2024</p>
          </div>
          <div className="mt-10 border-l border-gray-700 pl-6">
            <p className="text-xl font-semibold">Data Scientist</p>
            <p className="mt-2 text-gray-400">Impact Big Data Analytics</p>
            <p className="mt-2 text-sm text-gray-500">February 2021 — August 2022</p>
          </div>
        </div>
      </section>


      <section id="resume" className="border-t border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm tracking-widest text-emerald-400">
            06 / RESUME
          </p>

          <div className="mt-8 grid items-center gap-10 lg:grid-cols-[1fr_auto]">
            <div>
              <h2 className="max-w-2xl text-3xl font-semibold md:text-4xl">
                A closer look at my engineering journey.
              </h2>

              <p className="mt-6 max-w-2xl leading-8 text-gray-400">
                Explore my professional experience across AI engineering,
                agentic AI, enterprise data platforms, machine learning
                systems and cloud architecture.
              </p>

              <p className="mt-5 text-sm text-gray-500">
                Abdulla Chowdry · AI + Data Engineer · 5+ Years Experience
              </p>
            </div>

            <div className="flex flex-wrap gap-4 lg:flex-col">
              <a
                href="/resume.pdf"
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-full border border-gray-700 px-7 py-3 text-center text-white transition hover:border-emerald-400"
              >
                View Resume ↗
              </a>

              <a
                href="/resume.pdf"
                download="Abdulla_Chowdry_Resume.pdf"
                className="rounded-full bg-emerald-400 px-7 py-3 text-center font-medium text-black transition hover:bg-emerald-300"
              >
                Download PDF ↓
              </a>
            </div>
          </div>
        </div>
      </section>

      <footer className="border-t border-gray-800">
        <div className="mx-auto flex max-w-6xl flex-col justify-between gap-6 px-6 py-10 md:flex-row">
          <div>
            <p className="font-semibold">CHOWDRY MOHAMMED ABDULLA</p>
            <p className="mt-2 text-sm text-gray-500">
              Building intelligent systems at scale.
            </p>
          </div>
          <div className="flex gap-6 text-sm text-gray-400">
            <a href="https://github.com/abdullachowdry750" target="_blank" rel="noreferrer">GitHub ↗</a>
            <a
  href="https://www.linkedin.com/in/chowdry-abdulla-178484156/"
  target="_blank"
  rel="noopener noreferrer"
>
  LinkedIn ↗
</a>
            <a href="mailto:abdullachowdry@gmail.com">Email ↗</a>
          </div>
        </div>
      </footer>
    </main>
  );
}