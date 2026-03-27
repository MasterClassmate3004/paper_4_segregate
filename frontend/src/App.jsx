import { useState } from 'react'
import './index.css'

function App() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!file) return

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.message || "Failed to upload")
      }
      setResult(data.files)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-lg">
        <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">PDF Segregator</h1>
        
        <form onSubmit={handleUpload} className="flex flex-col gap-4">
          <div className="flex flex-col items-center justify-center w-full">
            <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors">
              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                <svg className="w-8 h-8 mb-4 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                    <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
                </svg>
                <p className="mb-2 text-sm text-gray-500"><span className="font-semibold">Click to upload</span> or drag and drop</p>
                <p className="text-xs text-gray-500">Only PDF files supported</p>
              </div>
              <input type="file" className="hidden" accept=".pdf" onChange={(e) => {
                setFile(e.target.files[0])
                setResult(null)
                setError(null)
              }} />
            </label>
            {file && <p className="mt-3 text-sm font-medium text-gray-700 bg-gray-100 px-3 py-1 rounded-full">Selected: {file.name}</p>}
          </div>

          <button 
            type="submit" 
            disabled={!file || loading}
            className="w-full text-white bg-blue-600 hover:bg-blue-700 font-medium rounded-lg text-sm px-5 py-3 mt-2 text-center transition-colors disabled:bg-blue-300 disabled:cursor-not-allowed"
          >
            {loading ? "Processing..." : "Segregate Questions"}
          </button>
        </form>

        {error && (
          <div className="mt-4 p-4 text-sm text-red-800 bg-red-50 rounded-lg border border-red-200">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-8 animate-in fade-in slide-in-from-bottom-2 duration-300">
            <h2 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">Segregated Questions</h2>
            <ul className="flex flex-col gap-3">
              {result.map((filename, i) => (
                <li key={i} className="flex justify-between items-center p-3 border border-gray-200 rounded-lg bg-gray-50 hover:bg-white hover:border-blue-300 transition-all shadow-sm">
                  <span className="text-sm font-medium text-gray-700 truncate mr-4">{filename}</span>
                  <a 
                    href={`http://localhost:8000/output/${filename}`}
                    target="_blank"
                    rel="noreferrer"
                    className="shrink-0 text-xs font-semibold text-blue-600 hover:text-blue-800 bg-blue-100 hover:bg-blue-200 rounded-md px-3 py-1.5 transition-colors focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  >
                    View PDF
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
