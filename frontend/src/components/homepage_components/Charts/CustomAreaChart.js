import React from "react";
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Area,
  AreaChart,
} from "recharts";

export const CustomAreaChart = ({ title, data }) => {
  return (
    <AreaChart width={800} height={400} data={data}>
      <CartesianGrid strokeDasharray="3 3" stroke="#9fd9af" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Area
        type="monotone"
        dataKey="tracks"
        stroke="#746fd6"
        fill="#8884d8"
        fillOpacity={0.6}
      />
    </AreaChart>
  );
};
