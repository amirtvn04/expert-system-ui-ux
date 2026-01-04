import Header from "./components/header"
import Footer from "./components/Footer"
import InputPanel from "./components/InputPanel"
import ResultPanel from "./components/ResultPanel"

function App() {

  return (
    <>
      <Header />

      <main className="max-w-300 mx-auto px-6 py-8">
        <div className="grid grid-cols-2 gap-6 mb-9">
            <InputPanel />

            <ResultPanel />
        </div>
      </main>

      <Footer />
    </>
  )
}

export default App
