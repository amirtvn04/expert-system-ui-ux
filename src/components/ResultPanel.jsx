import EmptyState from './EmptyState'
import ResultContent from './ResultContent'

function ResultPanel({ data, loading, error }) {

  return (
    <div
      className={`
        bg-white p-6 rounded-xl border border-black/10 
        ${(!error && !loading && data) ? "animate-fadeIn" : ""} 
        ${data ? "" : "flex items-center justify-center "}
      `}
    >
     {loading && (
        <EmptyState label={"⏳ در حال تحلیل داده‌ها..."} />
     )}

     {error && (
        <EmptyState label={error} />
     )}

     {!error && !loading && !data && (
        <EmptyState label={"مقادیر را وارد کرده و دکمه تحلیل را بزنید"} />
     )}

     {!error && !loading && data && (
        <ResultContent data={data} />
     )}
      
    </div>
  );
}

export default ResultPanel