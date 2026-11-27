# Incident Reporting Integration

## Objective

Connect the existing React incident form to the existing Express incident creation endpoint. The form collects the fields required by the current Mongoose `Incident` schema and reports validation, network, and server outcomes. MongoDB Atlas configuration is still pending.

## API

`POST /api/incidents`

Required JSON fields:

- `incidentType`: one of `Harassment`, `Theft`, `Assault`, `Stalking`, `Unsafe Area`, or `Other`.
- `description`: non-empty text.
- `location.address`: non-empty incident address.
- `location.coordinates.latitude`: finite number from -90 to 90.
- `location.coordinates.longitude`: finite number from -180 to 180.
- `incidentDate`: valid ISO date-time string (the browser converts the selected local date and time to UTC).

Example request:

```json
{
  "incidentType": "Harassment",
  "description": "User-entered description",
  "location": {
    "address": "User-entered incident address",
    "coordinates": { "latitude": 12.9716, "longitude": 77.5946 }
  },
  "incidentDate": "2026-11-27T14:30:00.000Z"
}
```

On successful persistence, the API returns HTTP 201:

```json
{
  "success": true,
  "message": "Incident reported successfully",
  "data": { "_id": "...", "incidentType": "Harassment" }
}
```

The actual `data` object is the created Mongoose document and includes the schema fields and generated timestamps. `riskLevel`, `isVerified`, and timestamps are not accepted from this create form; schema defaults remain in effect.

## Validation and errors

The frontend and create controller both validate the incident type, required text, coordinate presence and ranges, and occurrence date. The API returns HTTP 400 with `success: false` and a readable message (and field errors for validation failures). A successful create returns HTTP 201. Unexpected persistence errors return HTTP 500 with a generic message that does not expose database details. Malformed JSON is returned as HTTP 400 JSON by the server error middleware.

The form shows separate validation, network/timeout, and server response messages. It disables submission while waiting, preserves values on failure, and clears the form only after HTTP 201 with `success: true`.

## Location and date limitations

Address and coordinates are entered manually until map selection is implemented. The coordinate fields are labelled temporary. The optional current-location action first asks the user to confirm that their current GPS position is where the incident occurred. GPS permission denial and unavailable location are reported; no address geocoding is performed.

The incident occurrence field uses the browser's local `datetime-local` input. Its value is converted to an ISO UTC timestamp before submission. The selected time is not silently replaced with the current time.

## Development proxy and production API base

Vite proxies `/api` requests to `http://localhost:5000`, matching the backend's current default port. Start the frontend and backend development servers separately. The backend still requires a database connection before it starts listening.

For a future deployment with a separately hosted API, set the frontend build environment variable `VITE_API_BASE_URL` to the API origin (for example, `https://api.example.com`). The form appends `/api/incidents`. Keep deployment-specific values in the deployment environment; do not commit credentials. For same-origin deployment, leave this variable unset and route `/api` through the web server/reverse proxy.

## Files changed

- `frontend/src/App.jsx` — updated the existing report form, validation, GPS confirmation, request, and submission states.
- `frontend/src/App.css` — added styles for location controls and status messages.
- `frontend/vite.config.js` — added the `/api` development proxy.
- `backend/routes/incidentRoutes.js` — aligned controller import casing with the existing filename.
- `backend/controllers/IncidentController.js` — added create-only request validation and safe error responses.
- `backend/server.js` — added JSON handling for malformed request bodies. Existing database-first startup and its single `app.listen()` remain.
- `backend/package.json` — connected the test script to Node's built-in test runner.
- `backend/test/incidentController.test.js` — added mocked persistence tests; no database connection is made.

## Testing

From the repository root:

```powershell
cd frontend
npm run lint
npm run build
```

In another terminal:

```powershell
cd backend
npm test
```

The backend tests replace `Incident.create` with an in-memory mock and do not connect to MongoDB. They cover valid creation, invalid/missing fields, malformed body values, coordinate errors, invalid date, generic database failure, response status/body, and exclusion of client-supplied risk/verification fields.

## Verification status

- `backend`: `npm test` — 12 tests passed, 0 failed. Persistence was mocked; no database connection was made.
- `frontend`: `npm run lint` — passed.
- `frontend`: `npm run build` — passed.

These checks do not verify a real MongoDB write. Atlas integration remains pending and must be validated only after MongoDB configuration is provided.
