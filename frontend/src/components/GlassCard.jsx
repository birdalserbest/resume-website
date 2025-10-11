export default function GlassCard({ children, className = "" }) {
  return (
    <div
      className={[
        "backdrop-blur-xl bg-neutral-900/40", // glass effect
        "border border-white/10 rounded-2xl", // subtle frame
        "shadow-[0_8px_30px_rgba(0,0,0,0.25)]", // depth
        "w-full", // inherit child width (Chat controls width)
        className,
      ].join(" ")}
    >
      {children}
    </div>
  );
}
