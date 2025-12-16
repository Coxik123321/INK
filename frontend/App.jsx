import Dashboard from "./pages/Dashboard";
import Defects from "./pages/Defects";
import Reports from "./pages/Reports";

export default function App() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Pipeline AI DSS</h1>
      <Dashboard />
      <Defects />
      <Reports />
    </div>
  );
}
