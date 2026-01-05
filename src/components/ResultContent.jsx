import MetricBar from "./elements/MetricBar"

function ResultContent({ data }) {
    return (
        <>
            <h3 className='text-2xl font-bakh-bold mb-7'>📊نتایج تحلیل و مسیر استدلال</h3>

            <div className='bg-blue-50 border-blue-300 border-2 rounded-lg p-6 space-y-7'>
                <MetricBar label="نمره دیده‌شدن CTA" value={data.visibility_score} />
                <MetricBar label="نمره کلیک‌پذیری CTA" value={data.clickability_score} />
                <MetricBar label="میزان اطمینان سیستم" value={data.overall_certainty * 100} />
            </div>

            <h5 className="text-sm font-bakh-bold mt-7 mb-2">مسیر استدلال و قوانین فعال‌شده:</h5>

            <pre className="rounded-xl border border-black/10 bg-gray-50 p-3 whitespace-pre-wrap font-mono text-sm">
                {data.detailed_explanation}
            </pre>
        </>
    )
}

export default ResultContent