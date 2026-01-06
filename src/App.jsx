import Header from "./components/Header"
import Footer from "./components/Footer"
import InputPanel from "./components/InputPanel"
import ResultPanel from "./components/ResultPanel"
import { useState } from "react"

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const sendRequest = async (data) => {
    const payload = data.reduce((acc, item) => {
      acc[item.id] = Number(item.value);
      return acc;
    }, {});

    setError(false)
    setLoading(true)

    try {
      const response = await fetch("http://127.0.0.1:8000/api/analyze", {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result_ = await response.json();
      onResult(result_)
    } catch (err) {
      console.error("Error:", err);
      setError("مشکلی در ارتباط با سرور رخ داد. دوباره تلاش کنید.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  const onResult = (r) => {
    setResult(r)
  }

  const resetAll = () => {
    setResult(null)
    setError(null)
  }

  return (
    <>
      <Header />

      <main className="max-w-300 mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-9">
          <InputPanel sendReq={sendRequest} resetAll={resetAll} loading={loading}/>

          <ResultPanel data={result} loading={loading} error={error}/>
        </div>
      </main>

      <Footer />
    </>
  )
}

export default App
