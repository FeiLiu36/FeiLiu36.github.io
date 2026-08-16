// ======== Program table ========
function Schedule({ schedule }) {
  return (
    <section className="block" id="schedule">
      <div className="shell">
        <div className="block-head">
          <div className="block-num">§ 03 · Program</div>
          <div>
            <h2 className="block-title">Program</h2>
            <p className="block-kicker">
              Three sessions totalling three hours, plus a 30-minute coffee break. Slides are
              linked below as they become available.
            </p>
          </div>
        </div>

        <div className="prog-wrap">
          <table className="prog-table">
            <thead>
              <tr>
                <th className="c-part">Part</th>
                <th className="c-session">Session</th>
                <th className="c-dur">Duration</th>
                <th className="c-speaker">Presenter</th>
                <th className="c-slides">Slides</th>
              </tr>
            </thead>
            <tbody>
              {schedule.map((row) => (
                <tr key={row.id}>
                  <td className="c-part" data-label="Part">{row.part}</td>
                  <td className="c-session">
                    <h3 className="prog-title">{row.title}</h3>
                    {row.blurb && <p className="prog-blurb">{row.blurb}</p>}
                    <ul className="prog-topics">
                      {row.topics.map((t, i) => <li key={i}>{t}</li>)}
                    </ul>
                  </td>
                  <td className="c-dur" data-label="Duration">{row.duration}</td>
                  <td className="c-speaker" data-label="Presenter">{row.speaker}</td>
                  <td className="c-slides" data-label="Slides">
                    {row.slides ? (
                      <a
                        className="prog-slides-link"
                        href={row.slides.file}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        <img
                          className="thumb"
                          src={row.slides.cover}
                          alt={`First slide of ${row.title}`}
                          loading="lazy"
                        />
                        <span className="pdf">PDF ↓</span>
                        <span className="det">{row.slides.pages} slides · {row.slides.size}</span>
                      </a>
                    ) : (
                      <span className="prog-slides-none">to come</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
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
                <div className="avatar">
                  {p.photo
                    ? <img src={p.photo} alt={p.name} style={{width:"100%",height:"100%",objectFit:"cover",borderRadius:"3px"}} />
                    : initials}
                </div>
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
