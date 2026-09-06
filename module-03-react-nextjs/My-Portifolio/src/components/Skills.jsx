
const skills = [
  "HTML",
  "CSS",
  "JavaScript",
  'Dart',
  'Java',
  "React",
  'Flutter',
  "Git",
  "GitHub",
];

function Skills() {
  return (
    <section id="skills" className="section">
      <p className="section-label">WHAT I KNOW</p>
      <h2>My Skills</h2>

      <div className="skills-list">
        {skills.map((skill) => (
          <div className="skill-card" key={skill}>
            {skill}
          </div>
        ))}
      </div>
    </section>
  );
}

export default Skills;
