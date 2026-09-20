import { BrowserRouter, Routes, Route } from "react-router-dom";

import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import AnalyzeTender from "./pages/AnalyzeTender";
import StandardsAnalysis from "./pages/StandardsAnalysis";
import AuditPage from "./pages/AuditPage";
import StandardsGraph from "./components/StandardsGraph";

import "./App.css";
import Header from "./components/Header";

function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">

        <Sidebar />

        <div className="main-area">

          <Header />

          <main className="page-content">
            <Routes>

              <Route
                path="/"
                element={<Dashboard />}
              />

              <Route
                path="/analyze"
                element={<AnalyzeTender />}
              />

              <Route
                path="/standards"
                element={<StandardsAnalysis />}
              />

              <Route
                path="/audit"
                element={<AuditPage />}
              />

              <Route
                path="/graph"
                element={<StandardsGraph />}
              />

            </Routes>
          </main>

        </div>

      </div>
    </BrowserRouter>
  );
}

export default App;