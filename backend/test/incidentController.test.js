const test = require("node:test");
const assert = require("node:assert/strict");
const Incident = require("../models/Incident");
const { createIncident } = require("../controllers/IncidentController");

const validBody = () => ({
  incidentType: "Harassment",
  description: "  Report description  ",
  location: {
    address: "  Reported address  ",
    coordinates: { latitude: 12.9716, longitude: 77.5946 },
  },
  incidentDate: "2026-11-27T14:30:00.000Z",
  riskLevel: "High",
  isVerified: true,
});

async function invoke(body, create = async (record) => record) {
  const originalCreate = Incident.create;
  Incident.create = create;
  const result = { statusCode: undefined, body: undefined };
  const response = {
    status(code) {
      result.statusCode = code;
      return this;
    },
    json(payload) {
      result.body = payload;
      return this;
    },
  };

  try {
    await createIncident({ body }, response);
  } finally {
    Incident.create = originalCreate;
  }
  return result;
}

test("valid request returns 201 and only persists allowed create fields", async () => {
  let persisted;
  const result = await invoke(validBody(), async (record) => {
    persisted = record;
    return { _id: "mock-id", ...record };
  });

  assert.equal(result.statusCode, 201);
  assert.equal(result.body.success, true);
  assert.equal(result.body.message, "Incident reported successfully");
  assert.equal(result.body.data._id, "mock-id");
  assert.equal(persisted.incidentType, "Harassment");
  assert.equal(persisted.description, "Report description");
  assert.equal(persisted.location.address, "Reported address");
  assert.equal(persisted.incidentDate.toISOString(), "2026-11-27T14:30:00.000Z");
  assert.equal("riskLevel" in persisted, false);
  assert.equal("isVerified" in persisted, false);
});

const invalidCases = [
  ["missing incident type", (body) => { delete body.incidentType; }],
  ["unsupported incident type", (body) => { body.incidentType = "Suspicious Activity"; }],
  ["empty description", (body) => { body.description = "  "; }],
  ["missing location address", (body) => { delete body.location.address; }],
  ["missing coordinates", (body) => { delete body.location.coordinates; }],
  ["invalid latitude", (body) => { body.location.coordinates.latitude = 91; }],
  ["invalid longitude", (body) => { body.location.coordinates.longitude = -181; }],
  ["empty coordinate strings", (body) => { body.location.coordinates.latitude = ""; body.location.coordinates.longitude = ""; }],
  ["invalid incident date", (body) => { body.incidentDate = "not-a-date"; }],
];

for (const [name, mutate] of invalidCases) {
  test(`${name} returns HTTP 400 without persistence`, async () => {
    const body = validBody();
    mutate(body);
    let called = false;
    const result = await invoke(body, async () => { called = true; });
    assert.equal(result.statusCode, 400);
    assert.equal(result.body.success, false);
    assert.ok(Array.isArray(result.body.errors));
    assert.equal(called, false);
  });
}

test("malformed request body returns HTTP 400", async () => {
  let called = false;
  const result = await invoke(null, async () => { called = true; });
  assert.equal(result.statusCode, 400);
  assert.equal(result.body.success, false);
  assert.equal(called, false);
});

test("database failure returns generic HTTP 500 without leaking details", async () => {
  const result = await invoke(validBody(), async () => {
    throw new Error("private database detail");
  });
  assert.equal(result.statusCode, 500);
  assert.deepEqual(result.body, {
    success: false,
    message: "Unable to save the incident right now.",
  });
  assert.equal(JSON.stringify(result.body).includes("private database detail"), false);
});
