import React, { useState, useEffect } from "react";
import "./styles/styles.css";

import Header from "./components/Header";
import BreadcrumbTrail from "./components/BreadcrumbTrail";
import Controls from "./components/Controls";
import TopicCard from "./components/TopicCard";

import { useLearningPath } from "./hooks/useLearningPath";

function KnowledgeExplorer() {
  const [input, setInput] = useState("");
  const [level, setLevel] = useState("basic");
  const [currentTopic, setCurrentTopic] = useState("");
  const [pendingTopic, setPendingTopic] = useState("");
  const [breadcrumbTrail, setBreadcrumbTrail] = useState([]);
  const [breadcrumbIndex, setBreadcrumbIndex] = useState(-1);
  const [darkMode, setDarkMode] = useState(true);
  const [direction, setDirection] = useState("forward");
  const [animationState, setAnimationState] = useState("idle");
  const [visibleSummaries, setVisibleSummaries] = useState({});

  const [searchLocked, setSearchLocked] = useState(false);
  const [exploreLocked, setExploreLocked] = useState(false);
  const [breadcrumbLocked, setBreadcrumbLocked] = useState(false);

  const { data: learningData, isLoading, error } = useLearningPath(pendingTopic, level);

  useEffect(() => {
    const theme = darkMode ? "dark" : "light";
    document.documentElement.classList.remove("light", "dark");
    document.documentElement.classList.add(theme);
    localStorage.setItem("theme", theme);
  }, [darkMode]);

  useEffect(() => {
    document.title = "Knowledge Explorer";
  }, []);

  useEffect(() => {
    if (learningData?.topic) {
      setCurrentTopic(learningData.topic);

      if (breadcrumbTrail.length === 0) {
        setBreadcrumbTrail([learningData.topic]);
        setBreadcrumbIndex(0);
      }
    }
  }, [learningData, breadcrumbTrail.length]);

  const handleReset = () => {
    setInput("");
    setCurrentTopic("");
    setPendingTopic("");
    setBreadcrumbTrail([]);
    setBreadcrumbIndex(-1);
    setAnimationState("idle");
    setVisibleSummaries({});
  };

  const fetchTopic = (topic) => {
    if (!topic) return;

    setTimeout(() => {
      setPendingTopic(topic);
      setVisibleSummaries({});
      setAnimationState("enter");
      setTimeout(() => setAnimationState("idle"), 300);
    }, 200);
  };

  const handleSearch = () => {
    const trimmed = input.trim();
    if (!trimmed || trimmed === currentTopic || searchLocked) return;

    setSearchLocked(true);
    setDirection("forward");
    setAnimationState("exit");

    setTimeout(() => {
      fetchTopic(trimmed);
      setBreadcrumbTrail([]);
      setBreadcrumbIndex(0);
      setSearchLocked(false);
    }, 300);
  };

  const handleExplore = (subtopic) => {
    if (subtopic === currentTopic || exploreLocked) return;

    setExploreLocked(true);

    const updatedTrail = breadcrumbTrail
      .slice(0, breadcrumbIndex + 1)
      .concat(subtopic);

    setBreadcrumbTrail(updatedTrail);
    setBreadcrumbIndex(updatedTrail.length - 1);
    setDirection("forward");
    setAnimationState("exit");

    setTimeout(() => {
      fetchTopic(subtopic);
      setExploreLocked(false);
    }, 300);
  };

  const handleBreadcrumbClick = (index) => {
    const target = breadcrumbTrail[index];
    if (target === currentTopic || breadcrumbLocked) return;

    setBreadcrumbLocked(true);
    setDirection(index > breadcrumbIndex ? "forward" : "backward");
    setBreadcrumbIndex(index);
    setAnimationState("exit");

    setTimeout(() => {
      fetchTopic(target);
      setBreadcrumbLocked(false);
    }, 300);
  };

  const toggleSummary = (item) => {
    setVisibleSummaries((prev) => ({
      ...prev,
      [item]: !prev[item],
    }));
  };

  return (
    <div className={`${darkMode ? "dark" : ""}`} suppressHydrationWarning>
      <div
        key={darkMode ? "dark" : "light"}
        className="min-h-screen font-sans transition-colors duration-300 text-light-text dark:text-dark-text bg-light-bg dark:bg-dark-bg animate-fade"
      >
        <Header />

        {breadcrumbTrail.length > 0 && (
          <BreadcrumbTrail
            breadcrumbTrail={breadcrumbTrail}
            activeIndex={breadcrumbIndex}
            onClick={handleBreadcrumbClick}
            onReset={handleReset}
          />
        )}

        <Controls
          input={input}
          setInput={setInput}
          level={level}
          setLevel={setLevel}
          loading={isLoading || searchLocked}
          onSearch={handleSearch}
          darkMode={darkMode}
          toggleDarkMode={() => setDarkMode(!darkMode)}
        />

        <main className="max-w-3xl mx-auto px-4 overflow-hidden">
          {isLoading && (
            <p className="text-center text-gray-500 py-8">Loading...</p>
          )}

          {error && (
            <p className="text-center text-red-500 py-8">
              Failed to fetch data: {error.message}
            </p>
          )}

          {!isLoading && currentTopic && learningData && (
            <div
              className={`transition-all duration-500 transform ${
                animationState === "exit"
                  ? direction === "forward"
                    ? "-translate-x-full opacity-0"
                    : "translate-x-full opacity-0"
                  : animationState === "enter"
                  ? direction === "forward"
                    ? "translate-x-full opacity-0"
                    : "-translate-x-full opacity-0"
                  : "translate-x-0 opacity-100"
              }`}
            >
              <div className="space-y-4">
                {[learningData.topic, ...learningData.links].map((item, idx) => (
                  <TopicCard
                    key={idx}
                    index={idx}
                    item={item}
                    currentTopic={learningData.topic}
                    summary={item === learningData.topic ? learningData.summary : undefined}
                    level={level}
                    isExpanded={visibleSummaries[item]}
                    toggleSummary={toggleSummary}
                    handleExplore={handleExplore}
                  />
                ))}
              </div>
            </div>
          )}

          {!isLoading && !currentTopic && (
            <div className="text-center text-gray-500 py-16 text-lg">
              Start by entering a topic above
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default KnowledgeExplorer;
