
const express = require("express");
const cors = require("cors");
require("dotenv").config();

const incidentRoutes = require("./routes/incidentRoutes");
const connectDB = require("./config/db");

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use("/api/incidents", incidentRoutes);

// Test route
app.get("/", (req, res) => {
  res.send("Women's Safety Backend is Running!");
});

// Health check API
app.get("/api/health", (req, res) => {
  res.status(200).json({
    success: true,
    message: "Backend is working successfully",
    project: "Women's Safety Risk Prediction System",
  });
});

// Return malformed JSON request bodies as a consistent API error.
app.use((error, req, res, next) => {
  if (error?.type === "entity.parse.failed") {
    return res.status(400).json({
      success: false,
      message: "Request body must contain valid JSON.",
    });
  }

  return next(error);
});

// Start server after database connection
const startServer = async () => {
  try {
    await connectDB();

    const PORT = process.env.PORT || 5000;

    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
  } catch (error) {
    console.error("Server startup failed:", error.message);
    process.exit(1);
  }
};

startServer();
