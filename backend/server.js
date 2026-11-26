const express = require("express");
const cors = require("cors");
const incidentRoutes = require("./routes/incidentRoutes");
require("dotenv").config();
const connectDB = require("./config/db");
const app = express();
// C:\Users\bmymu\OneDrive\Desktop\Women-safety-risk-prediction\backend\config\db.js

// Middleware
app.use(cors());
app.use(express.json());
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

// Server configuration
const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

const startServer = async () => {
  await connectDB();

  const PORT = process.env.PORT || 5000;

  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
};

startServer();