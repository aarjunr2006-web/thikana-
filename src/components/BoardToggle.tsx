import type { DirectoryMode } from "../types";

interface BoardToggleProps {
  mode: DirectoryMode;
  onChange: (mode: DirectoryMode) => void;
}

export function BoardToggle({ mode, onChange }: BoardToggleProps) {
  return (
    <div className="board" role="tablist" aria-label="Switch directory">
      <button
        className={`board-tile ${mode === "stay" ? "active" : ""}`}
        role="tab"
        aria-selected={mode === "stay"}
        onClick={() => onChange("stay")}
      >
        STAY
      </button>
      <button
        className={`board-tile ${mode === "eat" ? "active" : ""}`}
        role="tab"
        aria-selected={mode === "eat"}
        onClick={() => onChange("eat")}
      >
        EAT
      </button>
      <button
        className={`board-tile ${mode === "fast_food" ? "active" : ""}`}
        role="tab"
        aria-selected={mode === "fast_food"}
        onClick={() => onChange("fast_food")}
      >
        FAST FOOD
      </button>
    </div>
  );
}
