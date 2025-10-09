import {useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import ResumePreview from "./components/ResumePreview"
import BackendMessage from "./components/BasicBackendMessage"


function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-center space-y-4">
      {/* Logo section */}
      <div className="flex justify-center space-x-4 mt-6">
        <a href="https://vite.dev" target="_blank" rel="noreferrer">
          <img
            src={viteLogo}
            className="logo w-24 hover:scale-110 transition-transform"
            alt="Vite logo"
          />
        </a>
        <a href="https://react.dev" target="_blank" rel="noreferrer">
          <img
            src={reactLogo}
            className="logo react w-24 hover:scale-110 transition-transform"
            alt="React logo"
          />
        </a>
      </div>

      {/* Title */}
      <h1 className="text-4xl font-bold text-white">Vite + React</h1>

      {/* Backend test message */}
      <BackendMessage />
      <ResumePreview />

      {/* Counter card */}
      <div className="card bg-neutral-800 p-6 rounded-xl shadow-md space-y-3">
        <button
          onClick={() => setCount(count + 1)}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-md transition-colors"
        >
          count is {count}
        </button>
        <p className="text-gray-300">
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>

      <p className="read-the-docs text-sm text-gray-400">
        Click on the Vite and React logos to learn more
      </p>
    </div>
  )
}

export default App