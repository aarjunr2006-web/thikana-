import type { FastFoodSpot } from "../types";
import { getTagClass } from "./tagUtils";

interface FastFoodCardProps {
  item: FastFoodSpot;
  onClick: () => void;
}

export function FastFoodCard({ item, onClick }: FastFoodCardProps) {
  // Use olive/saffron style tags for fast food
  const tagClass = getTagClass("Dhaba"); // tag-rose
  const cost = item.average_cost_for_two || 200;
  const specialties = item.specialties || [];
  const topItems = item.top_items ? Object.entries(item.top_items) : [];

  return (
    <button
      className="card ticket-card"
      onClick={onClick}
      aria-label={`View details for ${item.name || "Fast Food Spot"}`}
    >
      <div className="row-top">
        <div>
          <span className={`type-pill ${tagClass}`}>FAST FOOD</span>
          <h3>{item.name || "Loading..."}</h3>
        </div>
        <div className="badge-stack">
          <span className="budget-tag" style={{ color: "var(--saffron)" }}>
            ₹{cost} FOR TWO
          </span>
        </div>
      </div>

      <div className="divider-wrap">
        <div className="line"></div>
        <div className="notch left"></div>
        <div className="notch right"></div>
      </div>

      <div className="detail-row" style={{ display: "flex", flexDirection: "column", gap: "4px", fontSize: "0.8rem", color: "rgba(27, 51, 73, 0.72)", fontWeight: 600 }}>
        <span>📍 {item.area || "Jodhpur"}</span>
        <span style={{ fontSize: "0.75rem", color: "rgba(27, 51, 73, 0.7)", fontWeight: 500 }}>🏠 {item.address}</span>
        <span style={{ color: "rgba(27, 51, 73, 0.9)", fontWeight: 700 }}>📞 {item.contact_number}</span>
      </div>

      {topItems.length > 0 && (
        <div
          style={{
            marginTop: "12px",
            backgroundColor: "rgba(27, 51, 73, 0.04)",
            border: "1px dashed rgba(27, 51, 73, 0.2)",
            borderRadius: "8px",
            padding: "10px",
            fontFamily: "Space Mono, monospace",
            fontSize: "0.75rem",
          }}
        >
          <div style={{ textTransform: "uppercase", letterSpacing: "0.05em", color: "rgba(27, 51, 73, 0.6)", fontWeight: 700, borderBottom: "1px dashed rgba(27,51,73,0.15)", paddingBottom: "4px", marginBottom: "6px" }}>
            🧾 Best Sellers
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
            {topItems.map(([name, price]) => (
              <div key={name} style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "rgba(27, 51, 73, 0.85)" }}>{name}</span>
                <span style={{ color: "var(--saffron)", fontWeight: 700 }}>₹{price}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {specialties.length > 0 && (
        <div className="feature-row" style={{ marginTop: "12px" }}>
          {specialties.map((spec, idx) => (
            <span key={idx} className="feature-chip" style={{ fontSize: "0.68rem" }}>
              {spec}
            </span>
          ))}
        </div>
      )}
    </button>
  );
}
