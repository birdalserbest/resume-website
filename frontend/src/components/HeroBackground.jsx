// frontend/src/components/HeroBackground.jsx
// subtle animated gradient + grain overlay (tweak colors in PRESETS below)

const PRESETS = {
  // mature/classic — indigo → violet with a soft slate vibe
  mature: {
    // spotlight color (top-center glow)
    spotlight: "rgba(79,70,229,0.18)", // indigo-600 @ ~18%
    // main animated gradient stops
    stops: [
      "rgba(51,65,85,0.14)", // slate-700
      "rgba(99,102,241,0.14)", // indigo-500
      "rgba(139,92,246,0.12)", // violet-400
    ],
  },

  // current techy — blue → purple → teal (what you had)
  tech: {
    spotlight: "rgba(59,130,246,0.18)", // blue-500
    stops: [
      "rgba(29,78,216,0.18)", // blue-700
      "rgba(147,51,234,0.14)", // purple-700
      "rgba(14,165,233,0.14)", // sky-500
    ],
  },

  // cinematic pastel gradient — rich but gentle lavender & blue blend
  dreamyAurora: {
    spotlight: "rgba(174, 132, 255, 0.32)", // glowing violet halo
    stops: [
      "rgba(125, 211, 252, 0.24)", // light sky blue
      "rgba(168, 139, 253, 0.22)", // periwinkle-lavender
      "rgba(252, 165, 241, 0.20)", // soft pink glow
    ],
  },

  // pretty — cinematic dark indigo + rose-violet depth
  pretty: {
    spotlight: "rgba(147,112,219,0.22)", // soft violet glow
    stops: [
      "rgba(17,24,39,0.15)", // slate-900 base
      "rgba(79,70,229,0.20)", // indigo-600
      "rgba(236,72,153,0.16)", // rose-500 accent
    ],
  },
}

// choose which palette to use
const ACTIVE = "pretty"

export default function HeroBackground() {
  const { spotlight, stops } = PRESETS[ACTIVE]
  const gradient = `linear-gradient(120deg, ${stops[0]}, ${stops[1]}, ${stops[2]})`

  return (
    <div className="pointer-events-none fixed inset-0 -z-10">
      {/* radial spotlight — faint glow near top center */}
      <div
        className="absolute inset-0"
        style={{
          background: `radial-gradient(1000px 600px at 50% -10%, ${spotlight}, transparent 60%)`,
        }}
      />

      {/* slow-moving gradient */}
      <div
        className="absolute inset-0 bg-200 animate-gradient-pan"
        style={{ backgroundImage: gradient }}
      />

      {/* fine grain overlay */}
      <div className="absolute inset-0 opacity-20 mix-blend-soft-light [background-image:url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2260%22 height=%2260%22 viewBox=%220 0 60 60%22><filter id=%22n%22><feTurbulence type=%22fractalNoise%22 baseFrequency=%220.9%22 numOctaves=%223%22 stitchTiles=%22stitch%22/></filter><rect width=%2260%22 height=%2260%22 filter=%22url(%23n)%22 opacity=%220.15%22/></svg>')]" />
    </div>
  )
}
