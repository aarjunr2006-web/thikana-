import type { Accommodation } from "../types";
import { getTagClass } from "./tagUtils";

interface AccommodationCardProps {
  item: Accommodation;
  index: number;
  onClick: () => void;
}

export function AccommodationCard({ item, index, onClick }: AccommodationCardProps) {
  const serialNumber = (index + 1).toString().padStart(2, "0");
  const audienceClass = getTagClass(item.target_audience);

  return (
    <button
      className="card tag-card"
      onClick={onClick}
      aria-label={`View details for ${item.name}`}
    >
      <div className="row-top">
        <span className="tag-badge">TAG · {serialNumber}</span>
        <span className={`audience-pill ${audienceClass}`}>
          {item.target_audience}
        </span>
      </div>
      <h3>{item.name}</h3>
      <div className="area">📍 {item.area}</div>
      
      {/* Full physical address and contact phone info */}
      <div style={{ fontSize: "0.78rem", color: "rgba(27, 51, 73, 0.7)", marginTop: "6px", lineHeight: "1.3" }}>
        🏠 {item.address}
      </div>
      <div style={{ fontSize: "0.78rem", color: "rgba(27, 51, 73, 0.9)", fontWeight: 700, marginTop: "4px" }}>
        📞 {item.contact_number}
      </div>

      <span className="stamp" style={{ marginTop: "14px" }}>
        {item.distance_from_college_km.toFixed(1)} KM FROM LMC
      </span>
      
      <div className="feature-row">
        {item.features.map((feature, idx) => (
          <span key={idx} className="feature-chip">
            {feature}
          </span>
        ))}
      </div>
    </button>
  );
}
