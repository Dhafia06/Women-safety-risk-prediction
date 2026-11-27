const express = require("express");
const router = express.Router();

const {
  createIncident,
  getIncidents,
  getIncidentById,
  updateIncident,
  deleteIncident,
} = require("../controllers/IncidentController");

router.post("/", createIncident);

router.get("/", getIncidents);

router.get("/:id", getIncidentById);

router.put("/:id", updateIncident);

router.delete("/:id", deleteIncident);

module.exports = router;
