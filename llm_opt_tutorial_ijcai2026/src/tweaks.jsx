const { useState: useStateTw, useEffect: useEffectTw } = React;

// Default tweak values — edited in place by the host when user toggles.
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "accent": "teal",
  "theme": "light",
  "density": "normal"
}/*EDITMODE-END*/;

const ACCENTS = [
  { id: "teal",  color: "oklch(0.48 0.08 210)" },
  { id: "rust",  color: "oklch(0.52 0.12 42)"  },
  { id: "olive", color: "oklch(0.50 0.08 120)" },
  { id: "plum",  color: "oklch(0.45 0.10 310)" },
  { id: "ink",   color: "oklch(0.30 0.01 260)" },
];

function applyTweaks(t) {
  const root = document.documentElement;
  root.setAttribute("data-accent", t.accent);
  root.setAttribute("data-theme", t.theme);
  root.setAttribute("data-density", t.density);
}

function Tweaks() {
  const [open, setOpen] = useStateTw(false);
  const [vals, setVals] = useStateTw(TWEAK_DEFAULTS);
  const [available, setAvailable] = useStateTw(false);

  // Apply on mount + whenever values change
  useEffectTw(() => { applyTweaks(vals); }, [vals]);

  // Announce availability to parent + listen for activate/deactivate
  useEffectTw(() => {
    const onMsg = (e) => {
      if (!e.data || typeof e.data !== "object") return;
      if (e.data.type === "__activate_edit_mode")   { setOpen(true); setAvailable(true); }
      if (e.data.type === "__deactivate_edit_mode") { setOpen(false); setAvailable(false); }
    };
    window.addEventListener("message", onMsg);
    // Announce only AFTER listener is registered
    window.parent && window.parent.postMessage({ type: "__edit_mode_available" }, "*");
    return () => window.removeEventListener("message", onMsg);
  }, []);

  const update = (key, val) => {
    const next = { ...vals, [key]: val };
    setVals(next);
    window.parent && window.parent.postMessage({ type: "__edit_mode_set_keys", edits: { [key]: val } }, "*");
  };

  if (!available || !open) return null;

  return (
    <div className="tweaks open">
      <div className="tweaks-head">
        <span>Tweaks</span>
        <span style={{ color: "var(--muted)" }}>LLM4Opt · IJCAI 2026</span>
      </div>
      <div className="tweaks-body">
        <div className="tw-row">
          <div className="tw-label">Accent</div>
          <div className="tw-swatches">
            {ACCENTS.map((a) => (
              <button
                key={a.id}
                className={`tw-sw ${vals.accent === a.id ? "active" : ""}`}
                style={{ background: a.color }}
                onClick={() => update("accent", a.id)}
                title={a.id}
              />
            ))}
          </div>
        </div>

        <div className="tw-row">
          <div className="tw-label">Theme</div>
          <div className="tw-seg">
            {["light", "dark"].map((t) => (
              <button
                key={t}
                className={vals.theme === t ? "active" : ""}
                onClick={() => update("theme", t)}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        <div className="tw-row">
          <div className="tw-label">Density</div>
          <div className="tw-seg">
            {["compact", "normal", "spacious"].map((d) => (
              <button
                key={d}
                className={vals.density === d ? "active" : ""}
                onClick={() => update("density", d)}
              >
                {d}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { Tweaks, TWEAK_DEFAULTS, applyTweaks });
