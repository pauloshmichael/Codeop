
function Navbar() {
  return (
    <header className="navbar">
      <a href="#home" className="logo">
        MyPortfolio<span>.</span>
      </a>

      <nav>
        <a href="#home">Home</a>
        <a href="#about">About</a>
        <a href="#skills">Skills</a>
        <a href="#projects">Projects</a>
        <a href="#contact">Contact</a>
      </nav>
    </header>
  );
}

export default Navbar;
