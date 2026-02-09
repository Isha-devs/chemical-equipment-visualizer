import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement } from "chart.js";

ChartJS.register(ArcElement);

const TestChart = () => {
  return (
    <div style={{ width: 300, height: 300 }}>
      <Pie
        data={{
          labels: ["A", "B"],
          datasets: [{ data: [1, 2] }],
        }}
        options={{ maintainAspectRatio: false }}
      />
    </div>
  );
};

export default TestChart;
