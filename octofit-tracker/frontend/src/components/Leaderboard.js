import React, { useEffect, useState } from 'react';
import { apiUrl } from '../config';

export default function Leaderboard() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [selected, setSelected] = useState(null);

  const endpoint = 'leaderboard';
  const url = apiUrl(endpoint);

  const fetchData = () => {
    setLoading(true);
    setError(null);
    console.log('[Leaderboard] Fetching from', url);
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        console.log('[Leaderboard] Fetched data:', data);
        const list = Array.isArray(data) ? data : data?.results ?? [];
        setItems(list);
      })
      .catch((err) => {
        console.error('[Leaderboard] Fetch error', err);
        setError(err?.message ?? String(err));
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
  }, [url]);

  return (
    <div className="container container-main mt-4">
      <div className="card card-fixed">
        <div className="card-body">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h2 className="h4 mb-0">Leaderboard</h2>
            <div>
              <button className="btn btn-sm btn-secondary me-2" onClick={fetchData}>Refresh</button>
              <a className="btn btn-sm btn-outline-primary" href={url} target="_blank" rel="noreferrer">Open API</a>
            </div>
          </div>

          <p className="text-muted mb-2">Endpoint: <code>{url}</code></p>

          {loading && <div className="alert alert-info">Loading...</div>}
          {error && <div className="alert alert-danger">Error: {error}</div>}

          <div className="table-responsive">
            <table className="table table-striped table-hover table-fixed">
              <thead>
                <tr>
                  <th style={{width: '8%'}}>ID</th>
                  <th style={{width: '35%'}}>User</th>
                  <th style={{width: '42%'}}>Score / Info</th>
                  <th style={{width: '15%'}}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((it, idx) => (
                  <tr key={it.id ?? idx}>
                    <td>{it.id ?? '-'}</td>
                    <td>{it.username ?? it.name ?? '—'}</td>
                    <td><small className="text-muted">{it.score ?? it.points ?? JSON.stringify(it).slice(0, 100)}</small></td>
                    <td>
                      <button className="btn btn-sm btn-primary me-2" onClick={() => { setSelected(it); setShowModal(true); }}>View</button>
                    </td>
                  </tr>
                ))}
                {items.length === 0 && !loading && (
                  <tr><td colSpan={4} className="text-center text-muted">No leaderboard entries</td></tr>
                )}
              </tbody>
            </table>
          </div>

          <div className="mt-3">
            <h6 className="mb-1">Raw data</h6>
            <div className="code-block">{JSON.stringify(items, null, 2)}</div>
          </div>
        </div>
      </div>

      {showModal && (
        <>
          <div className="modal-backdrop-custom" onClick={() => setShowModal(false)} />
          <div className="modal modal-custom" tabIndex={-1} role="dialog">
            <div className="modal-dialog modal-lg" role="document">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">Leaderboard item</h5>
                  <button type="button" className="btn-close" aria-label="Close" onClick={() => setShowModal(false)} />
                </div>
                <div className="modal-body"><pre>{JSON.stringify(selected, null, 2)}</pre></div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Close</button>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
