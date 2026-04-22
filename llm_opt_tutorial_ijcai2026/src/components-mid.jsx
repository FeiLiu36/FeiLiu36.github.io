const { useState: useStateSch, useMemo: useMemoSch } = React;

// ======== Schedule ========
function Schedule({ schedule }) {
  const [open, setOpen] = useStateSch(new Set(["intro"]));
  const toggle = (id) => {
    setOpen((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  // Build running-time stamps starting at a nominal 09:00
  const stamps = useMemoSch(() => {
    let m = 9 * 60;
    return schedule.map((s) => {
      const start = m;
      m += s.minutes;
      const h = Math.floor(start / 60);
      const min = start % 60;
      return `${String(h).padStart(2, "0")}:${String(min).padStart(2, "0")}`;
    });
  }, [schedule]);

  return (
    <section className="block" id="schedule">
      <div className="shell">
        <div className="block-head">
          <div className="block-num">§ 03 · Program</div>
          <div>
            <h2 className="block-title">Detailed schedule</h2>
            <p className="block-kicker">
              Total duration 3 hours 30 minutes with a 30-minute coffee break. Start times are
              placeholders relative to a 09:00 session start — click any row to expand.
            </p>
          </div>
        </div>

        <div className="schedule">
          {schedule.map((row, i) => {
            const isBreak = row.id === "break";
            const isOpen = open.has(row.id);
            return (
              <div
                key={row.id}
                className={`sch-row ${isOpen ? "open" : ""} ${isBreak ? "is-break" : ""}`}
                onClick={() => !isBreak && toggle(row.id)}
              >
                <div className="sch-num">
                  {stamps[i]} · {row.part}
                </div>
                <div className="sch-dur">{row.duration}</div>
                <div>
                  <h3 className="sch-title">{row.title}</h3>
                  {row.blurb && <p className="sch-blurb">{row.blurb}</p>}
                  {!isBreak && (
                    <div className="sch-detail">
                      <ul>
                        {row.bullets.map((b, j) => <li key={j}>{b}</li>)}
                      </ul>
                    </div>
                  )}
                </div>
                <div className="sch-speaker">{row.speaker || ""}</div>
                <div className="sch-caret">{isBreak ? "" : "+"}</div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

// ======== Presenters ========
function Presenters({ presenters }) {
  return (
    <section className="block" id="presenters">
      <div className="shell">
        <div className="block-head">
          <div className="block-num">§ 04 · Organizers</div>
          <div>
            <h2 className="block-title">Presenters</h2>
            <p className="block-kicker">
              Four researchers working at the boundary of machine learning, operations research,
              and human–computer interaction.
            </p>
          </div>
        </div>

        <div className="people">
          {presenters.map((p) => {
            const initials = p.name.split(" ").map(w => w[0]).join("");
            return (
              <div className="person" key={p.name}>
                <div className="avatar">{initials}</div>
                <div>
                  <h4>{p.name}</h4>
                  <p className="aff">{p.affiliation}</p>
                  <p className="bio">{p.blurb}</p>
                  <div className="links">
                    <a href={`mailto:${p.email}`}>{p.email}</a>
                    {p.link && p.link !== "#" && <a href={p.link} target="_blank" rel="noopener">↗ homepage</a>}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

Object.assign(window, { Schedule, Presenters });
