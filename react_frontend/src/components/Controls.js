import React from "react";
import { FaSun, FaMoon } from "react-icons/fa";

const Controls = ({
  input,
  setInput,
  level,
  setLevel,
  loading,
  onSearch,
  darkMode,
  toggleDarkMode,
  searchHistory = [],
}) => {
  const filtered = searchHistory.filter((term) =>
    term.toLowerCase().includes(input.toLowerCase())
  );

  return (
    <section className="max-w-3xl mx-auto px-4 flex flex-wrap sm:flex-nowrap items-center gap-2 sm:gap-3 pb-4">
      <div className="relative w-full sm:flex-1">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !loading) {
              onSearch();
            }
          }}
          placeholder="Choose your starting point…"
          className="w-full border px-4 py-3 rounded-lg bg-white dark:bg-gray-800 dark:text-white dark:border-gray-600 focus:outline-none text-sm sm:text-base"
        />

        {input.length > 0 && filtered.length > 0 && !loading && (
          <ul className="absolute left-0 right-0 mt-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg shadow-lg z-50 max-h-48 overflow-y-auto">
            {filtered.map((term, i) => (
              <li
                key={i}
                className="px-4 py-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
                onClick={() => setInput(term)}
              >
                {term}
              </li>
            ))}
          </ul>
        )}
      </div>

      <select
        value={level}
        onChange={(e) => setLevel(e.target.value)}
        className="border px-3 py-2 rounded-lg bg-white dark:bg-gray-800 dark:text-white dark:border-gray-600 text-sm sm:text-base"
      >
        <option value="basic">Basic</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </select>

      <button
        onClick={loading ? null : onSearch}
        disabled={loading}
        className={`justify-center px-4 py-3 rounded-lg font-medium flex items-center gap-2 transition text-sm sm:text-base ${
          loading
            ? "bg-gray-400 cursor-not-allowed text-white"
            : "text-white bg-light-primary hover:bg-light-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
        }`}
      >
        {loading ? (
          <>
            <span className="spinner border-white border-t-gray-300" />
            Loading...
          </>
        ) : (
          "Go"
        )}
      </button>

      <button
        onClick={toggleDarkMode}
        className="text-xl px-4 py-3 rounded-full transition bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
        title="Toggle theme"
      >
        {darkMode ? <FaSun /> : <FaMoon />}
      </button>
    </section>
  );
};

export default Controls;

