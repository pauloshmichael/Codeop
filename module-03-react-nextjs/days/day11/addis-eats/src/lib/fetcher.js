/**
 * @file fetcher.js
 * @description SWR-compatible fetch wrapper for Addis Eats.
 *
 * SWR expects a "fetcher" function that accepts a URL string (or key) and
 * returns a Promise resolving to the parsed data. By default SWR uses the
 * browser's native fetch, but providing our own fetcher lets us:
 *  - automatically throw on non-OK HTTP responses (so SWR treats them as errors)
 *  - add global request options (e.g. credentials, headers) in one place
 *  - make error messages more descriptive for debugging
 *
 * Usage example with useSWR:
 *   const { data, error } = useSWR("/api/orders/ord-123", fetcher);
 */

/**
 * Fetches a URL and returns the parsed JSON response.
 * Throws an enriched Error if the response is not OK.
 *
 * @param {string} url — the resource URL to fetch
 * @returns {Promise<unknown>} parsed JSON data
 */
export async function fetcher(url) {
  const res = await fetch(url, {
    credentials: "same-origin", // send cookies for session auth
  });

  if (!res.ok) {
    // Attempt to parse an error message from the response body
    let message = `HTTP ${res.status} — ${res.statusText}`;
    try {
      const json = await res.json();
      if (json?.error) message = json.error;
    } catch {
      // body wasn't JSON — keep the default message
    }
    const err = new Error(message);
    err.status = res.status;
    throw err;
  }

  return res.json();
}
