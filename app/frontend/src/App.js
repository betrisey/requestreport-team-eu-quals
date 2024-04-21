import { HashRouter, Route, Routes } from "react-router-dom";
import Report from "./Report";
import Navbar from "./Navbar";
import Request from "./Request";

function App() {
  return (
    <HashRouter>
      <Navbar />
      <div className="container mx-auto p-4">
        <Routes>
          <Route path="/request" element={<Request />} />
          <Route path="/report" element={<Report />} />
          <Route
            path="/"
            element={<Request />}
          />
        </Routes>
      </div>
    </HashRouter>
  );
}

export default App;
