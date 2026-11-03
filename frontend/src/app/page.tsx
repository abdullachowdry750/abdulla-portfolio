import { getProfile, getProjects } from "@/lib/api";
const skills = [
  "Python", "FastAPI", "Apache Airflow", "PostgreSQL",
  "ClickHouse", "Kafka", "GCP", "Docker",
  "LLMs", "RAG", "MLflow", "System Design",
];

export default async function Home() {
  const profile = await getProfile();
  const projectData = await getProjects();

  const projects = projectData.projects;
  return (
    <main className="min-h-screen bg-[#090d12] text-white">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-7">
        <a href="#" className="text-xl font-bold tracking-tight">
          ABDULLA<span className="text-emerald-400">.</span>
        </a>
        <div className="hidden gap-8 text-sm text-gray-400 md:flex">
          <a href="#about" className="hover:text-white">About</a>
          <a href="#expertise" className="hover:text-white">Expertise</a>
          <a href="#projects" className="hover:text-white">Projects</a>
          <a href="#experience" className="hover:text-white">Experience</a>
        </div>
        <a
          href="mailto:abdullachowdry@gmail.com"
          className="rounded-full border border-gray-700 px-5 py-2 text-sm hover:border-emerald-400"
        >
          Contact ↗
        </a>
      </nav>

      <section className="mx-auto flex min-h-[650px] max-w-6xl flex-col justify-center px-6 py-24">
        <p className="mb-6 text-sm font-medium tracking-[0.25em] text-emerald-400">
          AI ENGINEERING · DATA PLATFORMS · CLOUD
        </p>

        <h1 className="max-w-4xl text-5xl font-semibold leading-tight tracking-tight md:text-7xl">
          Engineering intelligent systems
          <span className="text-emerald-400"> at scale.</span>
        </h1>

        <p className="mt-8 max-w-2xl text-lg leading-8 text-gray-400">
          I'm Abdulla Chowdry, an AI and Data Engineer focused on
          designing scalable data platforms, production-ready AI
          systems and reliable engineering infrastructure.
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
        </div>

        <div className="mt-20 grid max-w-2xl grid-cols-2 gap-8 border-t border-gray-800 pt-8 md:grid-cols-3">
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
          <div className="mt-12 grid gap-6 md:grid-cols-2">
            {projects.map((project) => (
              <article
                key={project.id}
                className="rounded-2xl border border-gray-800 bg-[#101720] p-8 transition hover:border-emerald-400/50"
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

                <p className="mt-8 text-sm text-gray-500">
                  {project.status}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="experience" className="border-t border-gray-800">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <p className="text-sm tracking-widest text-emerald-400">04 / EXPERIENCE</p>
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

      <footer className="border-t border-gray-800">
        <div className="mx-auto flex max-w-6xl flex-col justify-between gap-6 px-6 py-10 md:flex-row">
          <div>
            <p className="font-semibold">ABDULLA.</p>
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