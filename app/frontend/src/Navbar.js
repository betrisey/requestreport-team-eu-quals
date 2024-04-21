import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="bg-blue-600 p-4 shadow-lg rounded-b-lg">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-white font-bold text-lg">
          requestreport 📨🚨
        </Link>
        <ul className="flex items-center gap-6">
          <li>
            <Link
              to="/request"
              className="text-white hover:text-blue-200 transition duration-150 ease-in-out"
            >
              request 📨
            </Link>
          </li>
          <li>
            <Link
              to="/report"
              className="text-white hover:text-blue-200 transition duration-150 ease-in-out"
            >
              report 🚨
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
