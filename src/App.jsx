import Header from "./components/header"
import Footer from "./components/Footer"
import InputPanel from "./components/InputPanel"
import ResultPanel from "./components/ResultPanel"
import { useState } from "react"

function App() {
  const [result, setResult] = useState(null)

  const sendRequest = async () => {
    const data = {
      "cta_position_y": 900,
      "cta_width": 150,
      "cta_height": 40,
      "contrast_ratio": 2.5,
      "whitespace_around_cta": 20,
      "scroll_depth": 30,
      "cta_click_rate": 1.5,
      "number_of_ctas": 3,
      "cta_text_length": 30,
      "time_to_cta": 15,
      "clickable_elements_before_cta": 8,
      "content_word_count": 500,
      "similar_color_elements": 4,
      "largest_other_element_size": 15000,
      "cta_mobile_width": 160,
      "cta_mobile_height": 40,
      "has_loading_animation": 0
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/api/analyze", {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result_ = await response.json();
      onResult(result_)
    } catch (error) {
      console.error("Error:", error);
    }
  }

  const onResult = (r) => {
    setResult(r)
  }
  console.log("Response from API:", result);

  return (
    <>
      <Header />

      <main className="max-w-300 mx-auto px-6 py-8">
        <div className="grid grid-cols-2 gap-6 mb-9">
          <InputPanel sendReq={sendRequest} />

          <ResultPanel data={result} />
        </div>
      </main>

      <Footer />
    </>
  )
}

export default App
