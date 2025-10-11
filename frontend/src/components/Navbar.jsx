export default function Navbar() {
  return (
    <header className="fixed top-0 inset-x-0 z-10">
      <div className="mx-auto max-w-5xl px-4 py-4 flex items-center justify-between">
        <a href="/" className="font-semibold tracking-tight text-white/90">
          birdal<span className="text-blue-400">.dev</span>
        </a>
        <nav className="text-sm text-white/70 space-x-5">
          <a href="#" className="hover:text-white/100 transition-colors">
            Resume
          </a>
          <a href="#" className="hover:text-white/100 transition-colors">
            Projects
          </a>
          <a href="#" className="hover:text-white/100 transition-colors">
            Contact
          </a>
        </nav>
      </div>
    </header>
  );
}
