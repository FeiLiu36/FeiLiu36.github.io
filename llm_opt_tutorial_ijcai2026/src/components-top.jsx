const { useState, useEffect, useMemo } = React;

// ======== Top bar ========
function TopBar() {
  return (
    <div className="topbar">
      <div className="shell topbar-inner">
        <a className="topbar-logo" href="#top">
          <span className="dot" />
          <b>LLM4Opt</b>
          <span style={{ color: "var(--muted)" }}>· IJCAI 2026 Tutorial</span>
        </a>
        <nav className="topnav">
          <a href="#abstract">Abstract</a>
          <a href="#schedule">Schedule</a>
          <a href="#presenters">Presenters</a>
          <a href="#references">References</a>
        </nav>
      </div>
    </div>
  );
}

// ======== Hero ========
function Hero({ meta }) {
  return (
    <header className="hero" id="top">
      <div className="shell">
        <div className="hero-eyebrow">
          <span>IJCAI 2026 · Tutorial Program</span>
          <span className="bar" />
          <span>Bremen · August 15–17, 2026</span>
        </div>

        <h1>
          LLMs for Optimization: From <em>Automated Modeling</em> to <em>Algorithmic Discovery</em>
        </h1>

        <p className="tagline">
          A half-day tutorial surveying how large language models are reshaping mathematical
          optimization — translating natural-language problems into formal models, configuring
          solvers, and discovering new algorithms. Designed for a broad AI audience, with no
          prior optimization expertise required.
        </p>

        <div className="meta-row">
          <div className="meta-cell">
            <div className="k">Venue</div>
            <div className="v">{meta.venue}, {meta.city}</div>
          </div>
          <div className="meta-cell">
            <div className="k">Dates</div>
            <div className="v">{meta.dates}</div>
          </div>
          <div className="meta-cell">
            <div className="k">Length</div>
            <div className="v">{meta.length}</div>
          </div>
          <div className="meta-cell">
            <div className="k">Format</div>
            <div className="v">{meta.format}</div>
          </div>
        </div>
      </div>
    </header>
  );
}

// Marquee removed for academic style — keep a no-op export for compatibility
function Marquee() { return null; }

// ======== Abstract ========
function Abstract() {
  return (
    <section className="block" id="abstract">
      <div className="shell">
        <div className="abstract">
          <div className="label">§ 01 · Abstract</div>
          <div className="body">
            <p>
              Mathematical optimization is a foundational pillar of modern AI, underpinning
              decision-making in supply chains, energy systems, finance, and scheduling.
              Despite its importance, building and deploying optimization models remains a
              challenging, expert-driven process that requires significant domain knowledge
              and technical expertise.
            </p>
            <p>
              This tutorial surveys the emerging interface between LLMs and optimization along
              two synergistic themes. First, we examine how LLMs can act as <em>copilots</em>
              across the optimization pipeline — assisting with problem formulation, model
              construction, solver configuration, and validation. Second, we explore the growing
              role of LLMs in <em>algorithmic discovery</em>, generating, refining, and discovering
              new optimization algorithms and heuristics.
            </p>
            <p>
              The tutorial bridges machine learning and optimization, covering foundational
              concepts, surveying state-of-the-art methods and systems, and highlighting key
              challenges such as correctness, robustness, and handling ambiguous problem
              specifications.
            </p>

            <div className="overview">
              <div className="ov-item">
                <div className="n">3.5 h</div>
                <div className="l">Total duration</div>
              </div>
              <div className="ov-item">
                <div className="n">5</div>
                <div className="l">Program parts</div>
              </div>
              <div className="ov-item">
                <div className="n">20+</div>
                <div className="l">References</div>
              </div>
              <div className="ov-item">
                <div className="n">4</div>
                <div className="l">Presenters</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

// ======== Objectives + audience ========
function Objectives({ objectives, audiences, prerequisites }) {
  return (
    <section className="block" id="objectives">
      <div className="shell">
        <div className="block-head">
          <div className="block-num">§ 02 · Who &amp; Why</div>
          <div>
            <h2 className="block-title">Objectives and audience</h2>
            <p className="block-kicker">
              The tutorial bridges AI researchers new to optimization, OR researchers curious about
              how LLMs can assist modeling and algorithm design, and practitioners building
              AI-enabled decision-support systems.
            </p>
          </div>
        </div>

        <div className="two-col">
          <div>
            <div className="subhead">Learning outcomes</div>
            <ol className="list-clean">
              {objectives.map((o, i) => <li key={i}><span>{o}</span></li>)}
            </ol>
          </div>
          <div>
            <div className="subhead">Intended audience</div>
            <div className="aud-grid">
              {audiences.map((a) => (
                <div className="aud-card" key={a.tag}>
                  <div className="tag">{a.tag}</div>
                  <p>{a.blurb}</p>
                </div>
              ))}
            </div>

            <div className="subhead" style={{ marginTop: 32 }}>Prerequisites</div>
            <ol className="list-clean">
              {prerequisites.map((p, i) => <li key={i}><span>{p}</span></li>)}
            </ol>
          </div>
        </div>
      </div>
    </section>
  );
}

Object.assign(window, { TopBar, Hero, Marquee, Abstract, Objectives });
