
function Hero() {
  return (
    <section id="home" className="hero">
      <div>
        <p className="section-label">HELLO, I'M</p>
        <h1>Your Name</h1>
        <h2>Software Engineering Student</h2>

        <p>
          I build websites and applications using
          JavaScript, React, and other technologies.
        </p>

        <div className="hero-buttons">
          <a href="#projects" className="button primary">
            My Projects
          </a>

          <a href="#contact" className="button secondary">
            Contact Me
          </a>
        </div>
      </div>

      <div className="profile-placeholder">
        YN
      </div>
    </section>
  );
}

export default Hero;
