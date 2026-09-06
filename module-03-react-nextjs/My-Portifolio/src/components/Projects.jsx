
const projects = [
  {
    id: 1,
    title: "Portfolio Website",
    description: "A personal website built with React.",
    technology: "React, CSS",
  },
  {
    id: 2,
    title: "Farmer Marketplace",
    description: "A platform connecting farmers with buyers.",
    technology: "Flutter, Firebase",
  },
  {
    id: 3,
    title: "Task Manager",
    description: "An app for managing daily tasks.",
    technology: "JavaScript, HTML, CSS",
  },
];

function Projects() {
  return (
    <section id="projects" className="section projects">
      <p className="section-label">MY WORK</p>
      <h2>My Projects</h2>

      <div className="project-grid">
        {projects.map((project) => (
          <article className="project-card" key={project.id}>
            <h3>{project.title}</h3>
            <p>{project.description}</p>
            <span className="tech-stack">
              {project.technology}
            </span>
          </article>
        ))}
      </div>
    </section>
  );
}

export default Projects;
