import React from "react";
import { RadialBarChart, RadialBar, Legend, Tooltip } from "recharts";

const barColors = [
  "#8884d8",
  "#83a6ed",
  "#8dd1e1",
  "#82ca9d",
  "#a4de6c",
  "#d0ed57",
  "#ffc658",
];

export const CustomRadialBarChart = ({ data }) => {
  if (data) {
    for (let [index, value] of data.entries()) {
      value["fill"] = barColors[index];
    }
  }

  return (
    <RadialBarChart
      width={400}
      height={250}
      innerRadius="10%"
      outerRadius="80%"
      data={data}
      startAngle={180}
      endAngle={0}
    >
      <RadialBar
        minAngle={15}
        label={{ fill: "#666", position: "insideStart" }}
        background
        clockWise={true}
        dataKey="tracks"
      />
      <Legend
        iconSize={10}
        width={120}
        height={140}
        layout="vertical"
        verticalAlign="middle"
        align="right"
      />
      <Tooltip />
    </RadialBarChart>
  );
};
