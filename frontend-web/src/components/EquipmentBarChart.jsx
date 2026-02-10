// import React from "react";
// import { Bar } from "react-chartjs-2";
// import {
//   Chart as ChartJS,
//   CategoryScale,
//   LinearScale,
//   BarElement,
//   Tooltip,
//   Legend,
// } from "chart.js";



// ChartJS.register(
//   CategoryScale,
//   LinearScale,
//   BarElement,
//   Tooltip,
//   Legend
// );

// const EquipmentBarChart = ({ distribution }) => {
//   if (!distribution) return null;

//   const chartData = {
//     labels: Object.keys(distribution),
//     datasets: [
//       {
//         label: "Equipment Count",
//         data: Object.values(distribution),
//       },
//     ],
//   };


//   return (
//     <div style = {{ width: "600px", height: "400px" }}>
//         <Bar data={chartData} options = {{ responsive: true, maintainAspectRatio: false }}/>
//     </div>
//   );
// };

// export default EquipmentBarChart;






import React from "react";
import { Bar } from "react-chartjs-2";

const EquipmentBarChart = ({ distribution }) => {
  if (!distribution || Object.keys(distribution).length === 0) {
    return <p>No bar chart data available</p>;
  }

  const data = {
    labels: Object.keys(distribution),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(distribution),
        backgroundColor: "#4f46e5",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: false },
    },
  };

  return (
    <div style={{ width: "600px", margin: "auto" }}>
      <Bar 
      key={JSON.stringify(distribution)}
      data={data} options={options} />
    </div>
  );
};

export default EquipmentBarChart;
