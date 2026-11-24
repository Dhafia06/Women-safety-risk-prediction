import { useState } from "react";
import "./App.css";

const incidents = [
  { location: "MG Road", type: "Harassment", risk: "High", time: "9:30 PM" },
  { location: "Indiranagar", type: "Theft", risk: "Medium", time: "8:15 PM" },
  { location: "Whitefield", type: "Harassment", risk: "Low", time: "6:45 PM" },
  {
    location: "Marathahalli",
    type: "Suspicious Activity",
    risk: "Medium",
    time: "7:20 PM",
  },
];

function App() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [menuOpen, setMenuOpen] = useState(false);

  const navigation = [
    { name: "Dashboard", icon: "▦" },
    { name: "Safety Map", icon: "⌖" },
    { name: "Report Incident", icon: "⚑" },
    { name: "Emergency SOS", icon: "🆘" },
  ];

  return (
    <div className="app">
      <aside className={`sidebar ${menuOpen ? "open" : ""}`}>
        <div className="brand">
          <div className="brand-icon">✦</div>
          <div>
            <h2>SafeHer</h2>
            <span>Women's Safety Platform</span>
          </div>
        </div>

        <div className="nav-section">
          <p className="nav-heading">MENU</p>

          {navigation.map((item) => (
            <button
              key={item.name}
              className={`nav-item ${activePage === item.name ? "active" : ""}`}
              onClick={() => {
                setActivePage(item.name);
                setMenuOpen(false);
              }}
            >
              <span>{item.icon}</span>
              {item.name}
            </button>
          ))}
        </div>

        <div className="sidebar-bottom">
          <div className="help-card">
            <div className="help-icon">♥</div>
            <h4>Your safety matters</h4>
            <p>Stay aware. Stay connected. Stay safe.</p>
          </div>
          <div className="profile">
            <div className="avatar">D</div>
            <div>
              <h4>Welcome User</h4>
              <span>Personal Account</span>
            </div>
          </div>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <button
            className="menu-toggle"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            ☰
          </button>
          <div>
            <p className="breadcrumb">Pages / {activePage}</p>
            <h2>{activePage}</h2>
          </div>
          <div className="topbar-right">
            <span className="status-dot"></span>
            <span>System Online</span>
            <div className="top-avatar">D</div>
          </div>
        </header>

        {activePage === "Dashboard" && (
          <Dashboard setActivePage={setActivePage} />
        )}

        {activePage === "Safety Map" && <SafetyMap />}

        {activePage === "Report Incident" && <ReportIncident />}

        {activePage === "Emergency SOS" && <EmergencySOS />}
      </main>
    </div>
  );
}

function Dashboard({ setActivePage }) {
  return (
    <div className="content">
      <div className="welcome">
        <div>
          <h1>Your Safety Dashboard</h1>
          <p>Stay informed about your surroundings and travel confidently.</p>
        </div>
        <span className="date-badge">● Safety monitoring dashboard</span>
      </div>

      <section className="stats-grid">
        <StatCard
          icon="⌖"
          title="Locations Monitored"
          value="128"
          change="Sample data"
        />
        <StatCard
          icon="⚑"
          title="Reported Incidents"
          value="246"
          change="Sample data"
        />
        <StatCard
          icon="✓"
          title="Low Risk Areas"
          value="72%"
          change="Illustrative estimate"
        />
        <StatCard
          icon="♥"
          title="Emergency Contacts"
          value="03"
          change="Demo account"
        />
      </section>

      <section className="dashboard-grid">
        <div className="panel map-preview">
          <div className="panel-header">
            <div>
              <h3>Safety Overview</h3>
              <p>Explore location-based safety information</p>
            </div>
            <button
              className="text-button"
              onClick={() => setActivePage("Safety Map")}
            >
              View Map →
            </button>
          </div>

          <div className="map-placeholder">
            <div className="map-grid"></div>
            <div className="map-label label-one">MG Road</div>
            <div className="map-label label-two">Indiranagar</div>
            <div className="map-label label-three">Whitefield</div>
            <div className="map-pin pin-one">●</div>
            <div className="map-pin pin-two">●</div>
            <div className="map-pin pin-three">●</div>
            <div className="map-center">
              <span>⌖</span>
              <p>Map preview</p>
              <small>Connect Mapbox to view live locations</small>
            </div>
            <div className="map-legend">
              <span>
                <i className="low"></i> Low
              </span>
              <span>
                <i className="medium"></i> Medium
              </span>
              <span>
                <i className="high"></i> High
              </span>
            </div>
          </div>
        </div>

        <div className="panel quick-actions">
          <div className="panel-header">
            <div>
              <h3>Quick Actions</h3>
              <p>Access safety features</p>
            </div>
          </div>

          <button
            className="action-card"
            onClick={() => setActivePage("Safety Map")}
          >
            <span className="action-icon purple">⌖</span>
            <div>
              <h4>Explore Safety Map</h4>
              <p>Check location risk levels</p>
            </div>
            <b>→</b>
          </button>

          <button
            className="action-card"
            onClick={() => setActivePage("Report Incident")}
          >
            <span className="action-icon orange">⚑</span>
            <div>
              <h4>Report an Incident</h4>
              <p>Share a safety concern</p>
            </div>
            <b>→</b>
          </button>

          <button
            className="action-card"
            onClick={() => setActivePage("Emergency SOS")}
          >
            <span className="action-icon red">🆘</span>
            <div>
              <h4>Emergency SOS</h4>
              <p>Access emergency assistance</p>
            </div>
            <b>→</b>
          </button>
        </div>
      </section>

      <section className="panel incidents-panel">
        <div className="panel-header">
          <div>
            <h3>Recent Safety Reports</h3>
            <p>Illustrative sample incident data</p>
          </div>
          <button
            className="text-button"
            onClick={() => setActivePage("Report Incident")}
          >
            Report Incident +
          </button>
        </div>

        <IncidentTable />
      </section>

      <p className="disclaimer">
        Demo interface: statistics and incident locations are illustrative, not
        verified real-world safety information.
      </p>
    </div>
  );
}

function StatCard({ icon, title, value, change }) {
  return (
    <div className="stat-card">
      <div className="stat-top">
        <span>{title}</span>
        <div className="stat-icon">{icon}</div>
      </div>
      <h2>{value}</h2>
      <p>{change}</p>
    </div>
  );
}

function IncidentTable() {
  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Location</th>
            <th>Incident Type</th>
            <th>Risk Level</th>
            <th>Reported Time</th>
          </tr>
        </thead>
        <tbody>
          {incidents.map((incident, index) => (
            <tr key={index}>
              <td>{incident.location}</td>
              <td>{incident.type}</td>
              <td>
                <span className={`risk-badge ${incident.risk.toLowerCase()}`}>
                  {incident.risk}
                </span>
              </td>
              <td>{incident.time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function SafetyMap() {
  return (
    <div className="content">
      <div className="welcome">
        <div>
          <h1>Location Safety Map</h1>
          <p>Explore sample risk information across locations.</p>
        </div>
      </div>

      <div className="panel map-page">
        <div className="panel-header">
          <div>
            <h3>Interactive Map</h3>
            <p>Mapbox integration will be added in the next stage.</p>
          </div>
        </div>
        <div className="map-placeholder large-map">
          <div className="map-grid"></div>
          <div className="map-center">
            <span>⌖</span>
            <h3>Mapbox Integration Pending</h3>
            <p>
              Live map and location-based risk visualization will appear here.
            </p>
          </div>
          <div className="map-legend">
            <span>
              <i className="low"></i> Low Risk
            </span>
            <span>
              <i className="medium"></i> Medium Risk
            </span>
            <span>
              <i className="high"></i> High Risk
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

function ReportIncident() {
  const [form, setForm] = useState({
    location: "",
    type: "",
    description: "",
  });

  const [message, setMessage] = useState("");

  function handleSubmit(e) {
    e.preventDefault();

    if (!form.location || !form.type || !form.description) {
      setMessage("Please complete all fields.");
      return;
    }

    setMessage(
      "Demo only: report validated locally. Backend submission is not connected yet.",
    );
    setForm({ location: "", type: "", description: "" });
  }

  return (
    <div className="content">
      <div className="welcome">
        <div>
          <h1>Report an Incident</h1>
          <p>Help build awareness by reporting safety-related incidents.</p>
        </div>
      </div>

      <div className="panel form-panel">
        <h3>Incident Details</h3>
        <p className="form-description">
          Please provide accurate information. Avoid including unnecessary
          personal details.
        </p>

        <form onSubmit={handleSubmit}>
          <label>Incident Location</label>
          <input
            value={form.location}
            onChange={(e) => setForm({ ...form, location: e.target.value })}
            placeholder="Enter location"
          />

          <label>Incident Type</label>
          <select
            value={form.type}
            onChange={(e) => setForm({ ...form, type: e.target.value })}
          >
            <option value="">Select incident type</option>
            <option>Harassment</option>
            <option>Theft</option>
            <option>Assault</option>
            <option>Suspicious Activity</option>
            <option>Other</option>
          </select>

          <label>Description</label>
          <textarea
            rows="5"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            placeholder="Describe the incident..."
          />

          <button className="primary-button" type="submit">
            Submit Report
          </button>
          {message && <p className="form-message">{message}</p>}
        </form>
      </div>
    </div>
  );
}

function EmergencySOS() {
  const [location, setLocation] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  function getLocation() {
    if (!navigator.geolocation) {
      setMessage("Geolocation is not supported by this browser.");
      return;
    }

    setLoading(true);
    setMessage("");

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
        setLoading(false);
      },
      () => {
        setMessage(
          "Unable to retrieve location. Please allow location access.",
        );
        setLoading(false);
      },
      { enableHighAccuracy: true, timeout: 10000 },
    );
  }

  return (
    <div className="content">
      <div className="welcome">
        <div>
          <h1>Emergency SOS</h1>
          <p>Access your location information in an emergency.</p>
        </div>
      </div>

      <div className="panel sos-panel">
        <div className="sos-symbol">SOS</div>
        <h2>Emergency Assistance</h2>
        <p>
          Retrieve your current GPS location for sharing with trusted contacts.
        </p>

        <button className="sos-button" onClick={getLocation} disabled={loading}>
          {loading ? "Getting Location..." : "Get My Current Location"}
        </button>

        {location && (
          <div className="location-result">
            <h4>Current GPS Coordinates</h4>
            <p>Latitude: {location.latitude}</p>
            <p>Longitude: {location.longitude}</p>
            <a
              href={`https://www.google.com/maps?q=${location.latitude},${location.longitude}`}
              target="_blank"
              rel="noreferrer"
            >
              View on Google Maps
            </a>
          </div>
        )}

        {message && <p className="form-message">{message}</p>}

        <p className="sos-note">
          Demo only: this feature retrieves GPS coordinates. It does not send
          SOS alerts or contact emergency services yet.
        </p>
      </div>
    </div>
  );
}

export default App;
