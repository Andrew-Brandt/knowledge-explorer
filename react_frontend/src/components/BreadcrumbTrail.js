import React from "react";
import { FaHome } from "react-icons/fa";

const BreadcrumbTrail = ({ breadcrumbTrail, activeIndex, onClick, onReset }) => {
  return (
    <nav className="max-w-3xl mx-auto px-4 py-4 text-sm text-gray-500 dark:text-gray-300 text-center">
      <ul className="inline-flex flex-wrap items-center justify-center gap-2">
        <li>
          <button
            onClick={onReset}
            className="hover:text-red-500 transition text-lg"
            title="Home"
          >
            <FaHome />
          </button>
        </li>
        {breadcrumbTrail.map((crumb, index) => (
          <React.Fragment key={`${crumb}-${index}`}>
            <li>→</li>
            <li>
              <button
                onClick={() => onClick(index)}
                className={`hover:text-blue-500 transition ${
                  index === activeIndex ? "underline font-semibold text-blue-500" : ""
                }`}
              >
                {crumb}
              </button>
            </li>
          </React.Fragment>
        ))}
      </ul>
    </nav>
  );
};

export default BreadcrumbTrail;
