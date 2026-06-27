import { useEffect, useRef } from "react";
import type { DirectoryMode } from "../types";

interface DetailPanelProps {
  mode: DirectoryMode;
  item: any | null;
  onClose: () => void;
}

export function DetailPanel({ mode, item, onClose }: DetailPanelProps) {
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);
  const panelRef = useRef<HTMLElement>(null);

  const isOpen = !!item;

  // Manage focus trap and restoration for accessibility
  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement as HTMLElement;
      // Focus the close button once panel transitions in
      const timer = setTimeout(() => {
        closeButtonRef.current?.focus();
      }, 100);

      // Add escape key listener
      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === "Escape") {
          onClose();
        }
      };
      document.addEventListener("keydown", handleKeyDown);

      // Prevent background scrolling
      document.body.style.overflow = "hidden";

      return () => {
        clearTimeout(timer);
        document.removeEventListener("keydown", handleKeyDown);
        document.body.style.overflow = "";
      };
    } else {
      // Restore focus to triggering card when closing
      previousFocusRef.current?.focus();
    }
  }, [isOpen, onClose]);

  if (!isOpen || !item) return null;

  // Map and contact action details
  const googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
    item.name + " " + item.address
  )}`;

  const isContactable =
    item.contact_number &&
    !item.contact_number.includes("Walk-in") &&
    !item.contact_number.includes("Listed");
  const telLink = isContactable
    ? `tel:${item.contact_number.replace(/\s+/g, "")}`
    : "#";
  const contactText = isContactable ? item.contact_number : item.contact_number;

  const isJustdial = item.contact_number && item.contact_number.includes("Justdial");
  const finalContactHref = isJustdial ? "https://www.justdial.com/Jodhpur" : telLink;

  const endpoint =
    mode === "stay"
      ? `/api/v1/accommodations/${item.id}`
      : mode === "eat"
      ? `/api/v1/food-services/${item.id}`
      : `/api/v1/fast-food-spots/${item.id}`;

  return (
    <>
      {/* Dimmed Overlay click wrapper */}
      <div
        className={`overlay ${isOpen ? "open" : ""}`}
        onClick={onClose}
        aria-hidden="true"
      ></div>

      <aside
        ref={panelRef}
        className={`detail-panel ${isOpen ? "open" : ""}`}
        role="dialog"
        aria-modal="true"
        aria-label={`${item.name} details`}
      >
        <button
          ref={closeButtonRef}
          className="detail-close"
          onClick={onClose}
          aria-label="Close details"
        >
          ✕
        </button>

        <div id="detailContent">
          <p className="detail-eyebrow">
            {mode === "stay"
              ? "ACCOMMODATION"
              : mode === "eat"
              ? "FOOD SERVICE"
              : "FAST FOOD SPOT"}
          </p>
          <h2>{item.name}</h2>

          {mode === "stay" ? (
            <>
              <div className="detail-stats">
                <div className="stat-box">
                  <div className="label">Distance</div>
                  <div className="value">
                    {item.distance_from_college_km.toFixed(1)} km
                  </div>
                </div>
                <div className="stat-box">
                  <div className="label">Audience</div>
                  <div className="value">{item.target_audience}</div>
                </div>
                <div className="stat-box">
                  <div className="label">Area</div>
                  <div className="value">{item.area}</div>
                </div>
              </div>

              <div className="detail-section">
                <h4>What's included</h4>
                <ul className="checklist">
                  {item.features.map((feature: string, idx: number) => (
                    <li key={idx}>{feature}</li>
                  ))}
                </ul>
              </div>
            </>
          ) : mode === "eat" ? (
            <>
              <div className="detail-stats">
                <div className="stat-box">
                  <div className="label">Type</div>
                  <div className="value">{item.type}</div>
                </div>
                <div className="stat-box">
                  <div className="label">Budget</div>
                  <div className="value">{item.budget_type}</div>
                </div>
                <div className="stat-box">
                  <div className="label">Area</div>
                  <div className="value">{item.area}</div>
                </div>
              </div>

              <div className="detail-section">
                <h4>Timings</h4>
                <p className="detail-usp">{item.timings}</p>
              </div>

              <div className="detail-section">
                <h4>Why students go here</h4>
                <p className="detail-usp">{item.usp}</p>
              </div>
            </>
          ) : (
            <>
              <div className="detail-stats">
                <div className="stat-box">
                  <div className="label">Avg Cost</div>
                  <div className="value">₹{item.average_cost_for_two} / two</div>
                </div>
                <div className="stat-box">
                  <div className="label">Area</div>
                  <div className="value">{item.area}</div>
                </div>
              </div>

              <div className="detail-section">
                <h4>Specialties</h4>
                <div className="feature-row" style={{ marginTop: "0" }}>
                  {item.specialties.map((spec: string, idx: number) => (
                    <span
                      key={idx}
                      className="feature-chip"
                      style={{
                        background: "rgba(247, 239, 224, 0.08)",
                        color: "var(--cream)",
                        border: "1px solid rgba(247, 239, 224, 0.2)",
                      }}
                    >
                      {spec}
                    </span>
                  ))}
                </div>
              </div>

              {item.top_items && Object.keys(item.top_items).length > 0 && (
                <div className="detail-section">
                  <h4>Menu & Pricing</h4>
                  <div
                    style={{
                      background: "rgba(247, 239, 224, 0.04)",
                      border: "1px dashed rgba(247, 239, 224, 0.15)",
                      borderRadius: "10px",
                      padding: "14px",
                      fontFamily: "Space Mono, monospace",
                      fontSize: "0.82rem",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: "6px",
                      }}
                    >
                      {(Object.entries(item.top_items) as [string, number][]).map(([name, price]) => (
                        <div
                          key={name}
                          style={{
                            display: "flex",
                            justifyContent: "space-between",
                          }}
                        >
                          <span style={{ color: "rgba(247, 239, 224, 0.75)" }}>
                            {name}
                          </span>
                          <span
                            style={{ color: "var(--saffron)", fontWeight: 700 }}
                          >
                            ₹{price}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </>
          )}

          {/* Real-World Direction and Contact CTA triggers */}
          <div className="cta-row">
            <a
              className="btn btn-primary"
              href={googleMapsUrl}
              target="_blank"
              rel="noopener noreferrer"
            >
              Get Directions
            </a>
            <a
              className={`btn btn-secondary ${
                !isContactable && !isJustdial ? "opacity-50 pointer-events-none" : ""
              }`}
              href={finalContactHref}
              target={isJustdial ? "_blank" : undefined}
              rel={isJustdial ? "noopener noreferrer" : undefined}
            >
              {isContactable ? "Call Now" : contactText}
            </a>
          </div>

          <p className="api-note">Synced from GET {endpoint}</p>
        </div>
      </aside>
    </>
  );
}
