import type { FoodService } from "../types";
import { getTagClass } from "./tagUtils";

interface FoodServiceCardProps {
  item: FoodService;
  onClick: () => void;
}

export function FoodServiceCard({ item, onClick }: FoodServiceCardProps) {
  const typeClass = getTagClass(item.type || "Tiffin");
  const budgetText = (item.budget_type || "Budget").toUpperCase();

  return (
    <button
      className="card ticket-card"
      onClick={onClick}
      aria-label={`View details for ${item.name || "Food Service"}`}
    >
      <div className="row-top">
        <div>
          <span className={`type-pill ${typeClass}`}>{item.type || "Tiffin"}</span>
          <h3>{item.name || "Loading..."}</h3>
        </div>
        <div className="badge-stack">
          <span className="budget-tag">{budgetText}</span>
        </div>
      </div>
      
      <div className="divider-wrap">
        <div className="line"></div>
        <div className="notch left"></div>
        <div className="notch right"></div>
      </div>

      <div className="timings">🕒 {item.timings || "Open Hours"}</div>
      <p className="usp" style={{ marginBottom: "6px" }}>{item.usp || "Home-cooked local student food"}</p>
      
      <div className="area">📍 {item.area || "Jodhpur"}</div>
      
      {/* Physical address and callable number direct display */}
      <div style={{ fontSize: "0.78rem", color: "rgba(27, 51, 73, 0.7)", marginTop: "6px", lineHeight: "1.3" }}>
        🏠 {item.address}
      </div>
      <div style={{ fontSize: "0.78rem", color: "rgba(27, 51, 73, 0.9)", fontWeight: 700, marginTop: "4px" }}>
        📞 {item.contact_number}
      </div>
    </button>
  );
}
