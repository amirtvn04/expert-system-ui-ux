import EmptyState from './EmptyState'
import ResultContent from './ResultContent'

function ResultPanel({ data }) {
  const hasData = Boolean(data);

  return (
    <div
      className={`
        bg-white p-6 rounded-xl border border-black/10
        ${hasData ? "" : "flex items-center justify-center"}
      `}
    >
      {hasData ? <ResultContent data={data} /> : <EmptyState />}
    </div>
  );
}

export default ResultPanel