import React, { useState } from "react";
import UploadCSV from "../components/UploadCSV";
import History from "../components/History";
import EquipmentPieChart from "../components/EquipmentPieChart";
import EquipmentBarChart from "../components/EquipmentBarChart";

const Dashboard = () => {
  const [summary, setSummary] = useState(null);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Chemical Equipment Parameter Visualizer</h1>

      <UploadCSV onUploadSuccess={setSummary} />

      {summary && (
        <>
          <h2>Summary</h2>

          <p>Total Equipment: {summary.total_equipment}</p>
          <p>Average Flowrate: {summary.average_flowrate}</p>
          <p>Average Pressure: {summary.average_pressure}</p>
          <p>Average Temperature: {summary.average_temperature}</p>



          {/* PIE CHART */}
          <h3>Equipment Type Distribution (Pie)</h3>

          <EquipmentPieChart
            distribution={summary.equipment_type_distribution}
          />


          {/* BAR CHART */}
          <h3>Equipment Type Distribution (Bar)</h3>

          <EquipmentBarChart
            distribution={summary.equipment_type_distribution}
          />
          
          
        </>
      )}

      <hr />
      <History />
    </div>
  );
};

export default Dashboard;
