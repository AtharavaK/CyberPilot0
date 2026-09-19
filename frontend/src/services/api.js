const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * Start a new security scan.
 * @param {string} targetUrl
 * @returns {Promise<{scan_id: string, status: string, message: string}>}
 */
export async function startScan(targetUrl) {
  const res = await fetch(`${BASE_URL}/scan/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ target_url: targetUrl }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to start scan');
  }
  return res.json();
}

/**
 * Poll the status/result of a scan by its ID.
 * @param {string} scanId
 * @returns {Promise<object>}
 */
export async function getScanStatus(scanId) {
  const res = await fetch(`${BASE_URL}/scan/${scanId}/status`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to get scan status');
  }
  return res.json();
}
