import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";



ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

const EquipmentBarChart = ({ distribution }) => {
  if (!distribution) return null;

  const chartData = {
    labels: Object.keys(distribution),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(distribution),
      },
    ],
  };


  return (
    <div style = {{ width: "600px", height: "400px" }}>
        <Bar data={chartData} options = {{ responsive: true, maintainAspectRatio: false }}/>
    </div>
  );
};

export default EquipmentBarChart;
