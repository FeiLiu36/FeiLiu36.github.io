const { useState: useStateR, useMemo: useMemoR } = React;

// ======== References ========
function References({ references }) {
  const topics = useMemoR(() => {
    const set = new Set(references.map(r => r.topic));
    return ["All", ...Array.from(set)];
  }, [references]);

  const [active, setActive] = useStateR("All");
  const filtered = active === "All" ? references : references.filter(r => r.topic === active);

  return (
    <section className="block" id="references">
      <div className="shell">
        <div className="block-head">
          <div className="block-num">§ 05 · Reading</div>
          <div>
            <h2 className="block-title">Key references</h2>
            <p className="block-kicker">
              A curated subset of the growing literature at the LLM × optimization interface.
              Filter by theme.
            </p>
          </div>
        </div>

        <div className="ref-filter">
          {topics.map((t) => (
            <button
              key={t}
              className={`ref-chip ${active === t ? "active" : ""}`}
              onClick={() => setActive(t)}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="ref-list">
          {filtered.map((r) => (
            <div className="ref-item" key={r.key + r.title}>
              <div className="ref-topic">{r.topic}</div>
              <div>
                <h4 className="ref-title">{r.title}</h4>
                <div className="ref-cite">{r.key}</div>
              </div>
              <div className="ref-venue">{r.venue}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ======== History ========
function History({ history }) {
  return (
    <section className="block" id="history">
      <div className="shell">
        <div className="block-head">
          <div className="block-num">§ 06 · History</div>
          <div>
            <h2 className="block-title">Previous editions</h2>
            <p className="block-kicker">
              A preliminary version was delivered at AAAI 2026. Content has been expanded through
              invited talks and updated research for IJCAI 2026.
            </p>
          </div>
        </div>

        <div className="history">
          {history.map((h, i) => (
            <div className={`hist-item ${i === history.length - 1 ? "current" : ""}`} key={h.name}>
              <div className="y">{h.year}</div>
              <h5>{h.name}</h5>
              <p>{h.detail}</p>
              {h.link && <a href={h.link} target="_blank" rel="noopener">↗ materials</a>}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ======== Ethics ========
function Ethics() {
  return (
    <section className="block" id="ethics">
      <div className="shell">
        <div className="block-head">
          <div className="block-num">§ 07 · Responsible use</div>
          <div>
            <h2 className="block-title">Ethics and oversight</h2>
            <p className="block-kicker">
              LLM-generated optimization artifacts are <em>proposals</em>, not authoritative
              solutions.
            </p>
          </div>
        </div>

        <div className="ethics">
          <p>
            Incorrect or hallucinated formulations can lead to unsafe or harmful decisions in
            high-stakes applications — logistics, energy, finance, healthcare. LLMs may also
            inherit biases from training data and from problem descriptions, which can propagate
            into objectives, constraints, and recommendations.
          </p>
          <p>
            The tutorial discusses these risks directly. We emphasize evaluation, validation,
            transparency, reproducibility, and human oversight, and highlight responsible-use
            considerations for deploying these methods in real-world decision systems.
          </p>
        </div>
      </div>
    </section>
  );
}

// ======== Footer ========
function Footer() {
  return (
    <footer>
      <div className="shell">
        <div className="foot-top">
          <div>
            <div className="foot-title">LLMs for Optimization — IJCAI 2026 Tutorial</div>
            <div className="foot-sub">Bremen, Germany · August 15–17, 2026</div>
          </div>
          <div className="foot-col">
            <div className="t">Materials</div>
            <a href="https://conlaw.github.io/llm_opt_tutorial/tutorial.html" target="_blank" rel="noopener">AAAI 2026 version ↗</a>
            <a href="#references">Reading list</a>
            <a href="#history">Previous editions</a>
          </div>
          <div className="foot-col">
            <div className="t">Contact</div>
            <a href="mailto:fei.liu2@uzh.ch">fei.liu2@uzh.ch</a>
            <a href="mailto:lawlessc@stanford.edu">lawlessc@stanford.edu</a>
          </div>
        </div>
        <div className="foot-bottom">
          <span>© 2026 · LLM4Opt Tutorial Organizers</span>
          <span>Last updated · April 2026</span>
        </div>
      </div>
    </footer>
  );
}

Object.assign(window, { References, History, Ethics, Footer });
