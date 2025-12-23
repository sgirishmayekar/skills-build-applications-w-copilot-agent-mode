export const REACT_CODESPACE_NAME = process.env.REACT_APP_CODESPACE_NAME || '';

export const BASE_HOST = REACT_CODESPACE_NAME
  ? `https://${REACT_CODESPACE_NAME}-8000.app.github.dev`
  : `${window.location.protocol}//${window.location.host}`;

export function apiUrl(path) {
  // Ensure single slashes and trailing slash
  const cleanedPath = String(path).replace(/^\/+|\/+$/g, '');
  return `${BASE_HOST}/api/${cleanedPath}/`;
}

console.log('Config: REACT_APP_CODESPACE_NAME=', REACT_CODESPACE_NAME);
console.log('Config: BASE_HOST=', BASE_HOST);
