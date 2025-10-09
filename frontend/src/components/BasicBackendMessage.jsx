import { useEffect, useState } from "react";
import { API_BASE } from "src/config"

export default function BackendMessage() {
  const [msg, setMsg] = useState('Loading...')

  useEffect(() => {
    fetch(`${API_BASE}`)
      .then(r => r.json())
      .then(d => setMsg(d.message))
      .catch(() => setMsg('Failed to reach backend'))
  }, [])

  return (
    <h1 className="text-3xl font-bold mt-6 text-center text-blue-400">
      {msg}
    </h1>
  )
}