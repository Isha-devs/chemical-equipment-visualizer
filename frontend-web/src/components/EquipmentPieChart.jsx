import React from "react";
import { Pie } from "react-chartjs-2";

const EquipmentPieChart = ({ distribution }) => {
  if (!distribution || Object.keys(distribution).length === 0) {
    return <p>No pie chart data available</p>;
  }

  const data = {
    labels: Object.keys(distribution),
    datasets: [
      {
        data: Object.values(distribution),
        backgroundColor: [
          "#4f46e5",
          "#06b6d4",
          "#22c55e",
          "#f97316",
          "#ec4899",
        ],
      },
    ],
  };

  return (
    <div style={{ width: "400px", margin: "auto" }}>
      <Pie key={JSON.stringify(distribution)} data={data} />
    </div>
  );
};

export default EquipmentPieChart;
