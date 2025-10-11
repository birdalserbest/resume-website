// backend/frontend/src/components/HeroBackground.jsx
// Subtle animated deep-space gradient + grain overlay

export default function HeroBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10">
      {/* radial spotlight — faint blue glow near top center */}
      <div className="absolute inset-0 bg-[radial-gradient(1000px_600px_at_50%_-10%,rgba(59,130,246,0.25),transparent_60%)]" />

      {/* slow-moving blue–purple–teal gradient */}
      <div
        className="absolute inset-0 bg-200 animate-gradient-pan"
        style={{
          backgroundImage:
            "linear-gradient(120deg, rgba(29,78,216,0.18), rgba(147,51,234,0.14), rgba(14,165,233,0.14))",
        }}
      />

      {/* fine grain overlay */}
      <div className="absolute inset-0 opacity-20 mix-blend-soft-light [background-image:url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2260%22 height=%2260%22 viewBox=%220 0 60 60%22><filter id=%22n%22><feTurbulence type=%22fractalNoise%22 baseFrequency=%220.9%22 numOctaves=%223%22 stitchTiles=%22stitch%22/></filter><rect width=%2260%22 height=%2260%22 filter=%22url(%23n)%22 opacity=%220.15%22/></svg>')]" />
    </div>
  );
}
