import { useEffect, useState } from "react";
import { API_BASE } from "src/config"

export default function ResumePreview() {
  const [data, setData] = useState(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/api/resume`)
      .then(r => r.json())
      .then(setData)
      .catch(e => {
        console.error("Error fetching resume:", e);
        setErr("Failed to load resume");
      });
  }, []);

  if (err) return <div className="text-red-400">{err}</div>;
  if (!data) return <div className="opacity-70">Loading resume…</div>;

  return (
    <div className="mt-6 p-6 max-w-xl mx-auto space-y-4 bg-neutral-800/50 rounded-xl">
      <div>
        <h1 className="text-3xl font-bold">{data.name}</h1>
        <p className="text-lg opacity-80">{data.title}</p>
      </div>

      <section>
        <h2 className="font-semibold">Skills</h2>
        <ul className="list-disc ml-6">
          {data.skills.map(s => <li key={s}>{s}</li>)}
        </ul>
      </section>

      <section>
        <h2 className="font-semibold">Projects</h2>
        <ul className="space-y-2">
          {data.projects.map(p => (
            <li key={p.name}>
              <span className="font-medium">{p.name}</span>: {p.desc}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}