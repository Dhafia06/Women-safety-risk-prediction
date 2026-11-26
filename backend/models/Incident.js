const mongoose = require("mongoose");

const incidentSchema = new mongoose.Schema(
  {
    incidentType: {
      type: String,
      required: true,
      enum: [
        "Harassment",
        "Theft",
        "Assault",
        "Stalking",
        "Unsafe Area",
        "Other",
      ],
    },

    description: {
      type: String,
      required: true,
      trim: true,
    },

    location: {
      address: {
        type: String,
        required: true,
      },

      coordinates: {
        latitude: {
          type: Number,
          required: true,
        },

        longitude: {
          type: Number,
          required: true,
        },
      },
    },

    incidentDate: {
      type: Date,
      required: true,
    },

    riskLevel: {
      type: String,
      enum: ["Low", "Medium", "High"],
      default: "Medium",
    },

    isVerified: {
      type: Boolean,
      default: false,
    },
  },

  {
    timestamps: true,
  },
);

const Incident = mongoose.model("Incident", incidentSchema);

module.exports = Incident;
