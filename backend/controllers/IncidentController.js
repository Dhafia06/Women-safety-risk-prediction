const Incident = require("../models/Incident");
const mongoose = require("mongoose");

// Create a new incident
const createIncident = async (req, res) => {
  try {
    const { incidentType, description, location, incidentDate } = req.body;

    const incident = await Incident.create({
      incidentType,
      description,
      location,
      incidentDate,
    });

    res.status(201).json({
      success: true,
      message: "Incident reported successfully",
      data: incident,
    });
  } catch (error) {
    console.error("CREATE INCIDENT ERROR:", error);
    console.log("MongoDB connection state:", mongoose.connection.readyState);

    res.status(500).json({
      success: false,
      message: error.message,
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
