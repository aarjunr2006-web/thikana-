import type { DirectoryMode } from "../types";
import { BoardToggle } from "./BoardToggle";
import { SearchInput } from "./SearchInput";

interface HeroProps {
  mode: DirectoryMode;
  onModeChange: (mode: DirectoryMode) => void;
  search: string;
  onSearchChange: (search: string) => void;
  stayCount: number;
  eatCount: number;
}

export function Hero({
  mode,
  onModeChange,
  search,
  onSearchChange,
  stayCount,
  eatCount,
}: HeroProps) {
  const subcopy =
    mode === "stay"
      ? `${stayCount} verified hostels & PGs within walking distance of LMC. Filter by who it's for, how close, and what's included.`
      : `${eatCount} tiffins, dhabas & bhojnalayas LMC students actually rely on. Filter by type, area, and budget.`;

  return (
    <section className="hero">
      <svg
        className="skyline"
        viewBox="0 0 1200 90"
        preserveAspectRatio="none"
        xmlns="http://www.w3.org/2000/svg"
        fill="var(--cream)"
      >
        <rect x="0" y="50" width="60" height="40" />
        <rect x="60" y="35" width="22" height="55" />
        <rect x="95" y="55" width="40" height="35" />
        <rect x="150" y="20" width="26" height="70" />
        <polygon points="150,20 163,4 176,20" />
        <rect x="195" y="48" width="50" height="42" />
        <rect x="260" y="58" width="70" height="32" />
        <rect x="345" y="30" width="20" height="60" />
        <polygon points="345,30 355,16 365,30" />
        <rect x="380" y="50" width="90" height="40" />
        <rect x="490" y="40" width="24" height="50" />
        <rect x="530" y="60" width="60" height="30" />
        <rect x="610" y="25" width="22" height="65" />
        <polygon points="610,25 621,10 632,25" />
        <rect x="650" y="52" width="80" height="38" />
        <rect x="745" y="58" width="50" height="32" />
        <rect x="810" y="34" width="20" height="56" />
        <rect x="850" y="50" width="90" height="40" />
        <rect x="960" y="22" width="24" height="68" />
        <polygon points="960,22 972,6 984,22" />
        <rect x="1005" y="55" width="70" height="35" />
        <rect x="1090" y="45" width="60" height="45" />
        <rect x="1160" y="60" width="40" height="30" />
      </svg>
      <div className="hero-inner">
        <p className="eyebrow">LMC Student Utility Directory</p>
        <h1 className="headline">
          Find a <span id="modeWord">{mode === "stay" ? "place to stay" : "place to eat"}</span>
          <br />
          near campus.
        </h1>
        <p className="subcopy">{subcopy}</p>

        <BoardToggle mode={mode} onChange={onModeChange} />
        <SearchInput value={search} onChange={onSearchChange} />
      </div>
    </section>
  );
}
