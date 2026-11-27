const Incident = require("../models/Incident");
const mongoose = require("mongoose");

// Create a new incident
const createIncident = async (req, res) => {
  try {
    const body = req.body;
    const supportedIncidentTypes = [
      "Harassment",
      "Theft",
      "Assault",
      "Stalking",
      "Unsafe Area",
      "Other",
    ];

    if (!body || typeof body !== "object" || Array.isArray(body)) {
      return res.status(400).json({
        success: false,
        message: "A valid JSON object is required.",
      });
    }

    const { incidentType, description, location, incidentDate } = body;
    const latitude = location?.coordinates?.latitude;
    const longitude = location?.coordinates?.longitude;
    const parsedDate = typeof incidentDate === "string" ? new Date(incidentDate) : new Date(NaN);
    const errors = [];

    if (!supportedIncidentTypes.includes(incidentType)) {
      errors.push("A supported incidentType is required.");
    }
    if (typeof description !== "string" || !description.trim()) {
      errors.push("A non-empty description is required.");
    }
    if (typeof location?.address !== "string" || !location.address.trim()) {
      errors.push("A non-empty location.address is required.");
    }
    if (
      typeof latitude !== "number" ||
      !Number.isFinite(latitude) ||
      latitude < -90 ||
      latitude > 90
    ) {
      errors.push("location.coordinates.latitude must be a number from -90 to 90.");
    }
    if (
      typeof longitude !== "number" ||
      !Number.isFinite(longitude) ||
      longitude < -180 ||
      longitude > 180
    ) {
      errors.push("location.coordinates.longitude must be a number from -180 to 180.");
    }
    if (
      typeof incidentDate !== "string" ||
      !incidentDate.trim() ||
      Number.isNaN(parsedDate.getTime())
    ) {
      errors.push("A valid incidentDate is required.");
    }

    if (errors.length) {
      return res.status(400).json({
        success: false,
        message: "Incident details are invalid.",
        errors,
      });
    }

    const incident = await Incident.create({
      incidentType,
      description: description.trim(),
      location: {
        address: location.address.trim(),
        coordinates: { latitude, longitude },
      },
      incidentDate: parsedDate,
    });

    res.status(201).json({
      success: true,
      message: "Incident reported successfully",
      data: incident,
    });
  } catch (error) {
    console.error("CREATE INCIDENT ERROR:", error.message);

    res.status(500).json({
      success: false,
      message: "Unable to save the incident right now.",
    });
  }
};

// Get all incidents
const getIncidents = async (req, res) => {
  try {
    const incidents = await Incident.find().sort({
      createdAt: -1,
    });

    res.status(200).json({
      success: true,
      count: incidents.length,
      data: incidents,
    });
  } catch (error) {
    console.error("GET INCIDENTS ERROR:", error);
    console.log("MongoDB connection state:", mongoose.connection.readyState);

    res.status(500).json({
      success: false,
      message: error.message,
    });
  }
};


const getIncidentById = async (req, res) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({
        success: false,
        message: "Invalid incident ID",
      });
    }

    const incident = await Incident.findById(id);

    if (!incident) {
      return res.status(404).json({
        success: false,
        message: "Incident not found",
      });
    }

    res.status(200).json({
      success: true,
      data: incident,
    });
  } catch (error) {
    console.error("GET INCIDENT BY ID ERROR:", error);

    res.status(500).json({
      success: false,
      message: error.message,
    });
  }
};


const updateIncident = async (req, res) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({
        success: false,
        message: "Invalid incident ID",
      });
    }

    const incident = await Incident.findByIdAndUpdate(id, req.body, {
      new: true,
      runValidators: true,
    });

    if (!incident) {
      return res.status(404).json({
        success: false,
        message: "Incident not found",
      });
    }

    res.status(200).json({
      success: true,
      message: "Incident updated successfully",
      data: incident,
    });
  } catch (error) {
    console.error("UPDATE INCIDENT ERROR:", error);

    res.status(400).json({
      success: false,
      message: error.message,
    });
  }
};

const deleteIncident = async (req, res) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({
        success: false,
        message: "Invalid incident ID",
      });
    }

    const incident = await Incident.findByIdAndDelete(id);

    if (!incident) {
      return res.status(404).json({
        success: false,
        message: "Incident not found",
      });
    }

    res.status(200).json({
      success: true,
      message: "Incident deleted successfully",
    });
  } catch (error) {
    console.error("DELETE INCIDENT ERROR:", error);

    res.status(500).json({
      success: false,
      message: error.message,
    });
  }
};

module.exports = {
  createIncident,
  getIncidents,
  getIncidentById,
  updateIncident,
  deleteIncident,
};
