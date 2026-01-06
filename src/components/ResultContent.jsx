import MetricBar from "./elements/MetricBar"

function ResultContent({ data }) {
    const activeDataLength = data.activated_rules.length
    const activeData = data.activated_rules
    const recommendations = data.recommendations

    const activeClass = {
        weak: "bg-red-50 border border-red-600 text-red-800",
        good: "bg-blue-50 border border-blue-600 text-blue-800",
        excellent: "bg-green-50 border border-green-600 text-green-800",
        medium: "bg-yellow-50 border border-yellow-600 text-yellow-800"
    }

    return (
        <>
            <h3 className='text-2xl font-bakh-bold mb-7'>📊نتایج تحلیل و مسیر استدلال</h3>

            <div className='bg-blue-50 border-blue-400 border-2 rounded-lg p-3 md:p-5 space-y-7'>
                <MetricBar label="نمره دیده‌شدن CTA" value={data.visibility_score} />
                <MetricBar label="نمره کلیک‌پذیری CTA" value={data.clickability_score} />
                <MetricBar label="میزان اطمینان سیستم" value={data.overall_certainty * 100} />
                <div className="mt-8">
                    <span className="font-bakh-bold ml-1.5">وضعیت کلی:</span>
                    <div className={` inline-block px-3 py-1.5 text-sm rounded-lg text-white font-bakh-bold 
                    ${(data.summary.status_emoji === "weak") ? ' bg-red-500 border border-red-600' : ""}
                    ${(data.summary.status_emoji === "good") ? ' bg-blue-500 border border-blue-600' : ""}
                    ${(data.summary.status_emoji === "excellent") ? ' bg-green-500 border border-green-600' : ""}
                    ${(data.summary.status_emoji === "medium") ? ' bg-yellow-500 border border-yellow-600' : ""}
                    `}>
                        <span>{data.summary.overall_status}</span>
                    </div>
                </div>
            </div>

            <div className={`border-2 rounded-lg p-2 md:p-5 mt-6 ${activeClass[data.summary.status_emoji]}`}>
                <span className="font-bakh-bold mb-2 inline-block">پیشنهادات سیستم برای بهبود: </span>
                {recommendations.length > 0 && recommendations.map((item, index) => (<p className="mt-2" key={index}>{index + 1} . {item}</p>))}
                {recommendations.length === 0 && (<p>✨ طراحی شما عالی است! نیازی به بهبود فوری نیست.</p>)}
            </div>

            <div className="bg-purple-50 border-purple-400 border-2 rounded-lg p-2 md:p-5 mt-6 text-purple-800">
                <span className="font-bakh-bold mb-2 inline-block">قوانین اعمال شده: </span>
                {activeDataLength > 0 ? (
                    <>
                        <span>
                            {activeDataLength}
                        </span>
                        <div>
                            {activeData.map(item => item.rule_id).join("   |   ")}
                        </div>
                    </>
                ) : (
                    <p>
                        تمامی قوانین بر روی داده‌های شما بررسی شد و <span className="font-bakh-bold underline">همه آن‌ها پاس شدند</span>.
                    </p>
                )}
            </div>

            <h5 className="text-sm font-bakh-bold mt-7 mb-2">مسیر استدلال و قوانین فعال‌شده:</h5>

            <pre className="rounded-xl border border-black/10 bg-gray-50 p-3 whitespace-pre-wrap font-mono text-sm overflow-auto max-h-150">
                {data.detailed_explanation}
            </pre>
        </>
    )
}

export default ResultContent