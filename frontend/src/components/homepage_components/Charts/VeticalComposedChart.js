import React from "react";
import {
  ComposedChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

export const VerticalComposedChart = ({ title, data }) => {
  return (
    <ComposedChart
      layout="vertical"
      width={400}
      height={400}
      data={data}
      margin={{
        top: 20,
        right: 20,
        bottom: 0,
        left: 20,
      }}
    >
      <CartesianGrid stroke="#9fd9af" />
      <XAxis type="number" />
      <YAxis dataKey="name" type="category" scale="band" />
      <Tooltip />
      <Bar dataKey="tracks" barSize={7} fill="#8884d8" />
    </ComposedChart>
  );
};
