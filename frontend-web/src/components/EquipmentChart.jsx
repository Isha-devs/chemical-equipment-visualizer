import React from "react";
import { Pie } from "react-chartjs-2";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";


ChartJS.register(ArcElement, Tooltip, Legend);

const EquipmentChart = ({ data }) => {
  if (!data || Object.keys(data).length === 0) {
    return <p>No chart data available</p>;
  }

  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(data),
        backgroundColor: [
          "#36A2EB",
          "#FF6384",
          "#FFCE56",
          "#4BC0C0",
          "#9966FF",
          "#FF9F40",
        ],
        
      },
    ],
  };

  return (
    <div style={{ width: "400px", height: "400px", marginTop: "20px" }}>
      <Pie data={chartData} options = {{ responsive: true, maintainAspectRatio: false }} />
    </div>
  );
};

export default EquipmentChart;




