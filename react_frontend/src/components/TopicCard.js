import React from "react";
import { useSummary } from "../hooks/useSummary";

const SubtopicSummary = ({ item, level }) => {
  const { data, isLoading } = useSummary(item, level);

  if (isLoading) return <p>Loading...</p>;

  const summaryIsMissing = data?.toLowerCase().includes("not available");

  return (
    <>
      <p className="text-sm whitespace-pre-line">{data}</p>
      {summaryIsMissing && (
        <div className="text-red-400 text-sm italic mt-2">
          We couldn't find a summary for this topic — try rephrasing it!
        </div>
      )}
    </>
  );
};

const TopicCard = ({
  index,
  item,
  currentTopic,
  summary,
  level,
  isExpanded,
  toggleSummary,
  handleExplore,
}) => {
  const isMain = item === currentTopic;

  return (
    <div className="rounded-xl shadow-md px-4 py-3 bg-white dark:bg-gray-800 transition">
      <div className="flex flex-wrap justify-between items-start gap-3 mt-3 mb-2">
        <h3 className="text-lg sm:text-xl font-semibold flex-1">
          {index + 1}. {item || "[Untitled]"}
        </h3>

        {!isMain && (
          <div className="flex flex-wrap gap-2 min-w-fit">
            <button
              onClick={() => toggleSummary(item)}
              className="text-sm sm:text-base font-medium px-3 py-2 rounded bg-light-primary hover:bg-light-accent dark:bg-dark-primary dark:hover:bg-dark-accent text-white transition"
            >
              {isExpanded ? "Collapse Summary" : "Read Summary"}
            </button>

            <button
              onClick={() => handleExplore(item)}
              className="text-sm sm:text-base font-medium px-3 py-2 rounded bg-emerald-600 hover:bg-emerald-700 text-white transition"
            >
              Explore
            </button>
          </div>
        )}
      </div>

      <div
        className={`
          overflow-hidden transition-all duration-500 ease-in-out
          px-4 py-3 border rounded
          bg-gray-50 dark:bg-gray-700 
          dark:text-white text-sm whitespace-pre-line
          ${isMain || isExpanded ? "max-h-[2000px] opacity-100" : "max-h-0 opacity-0"}
        `}
      >
        <div
          className={`
            transition-opacity duration-500 ease-in-out delay-150
            ${isMain || isExpanded ? "opacity-100" : "opacity-0"}
          `}
        >
          {isMain ? (
            <p className="text-sm whitespace-pre-line">{summary}</p>
          ) : (
            isExpanded && <SubtopicSummary item={item} level={level} />
          )}
        </div>
      </div>
    </div>
  );
};

export default TopicCard;

