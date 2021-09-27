import React from "react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
} from "recharts";

export const CustomRadarChart = ({ data }) => {
  return (
    <RadarChart
      cx={200}
      cy={200}
      outerRadius={120}
      width={500}
      height={400}
      data={data}
    >
      <PolarGrid stroke="#9bd1aa" />
      <PolarAngleAxis dataKey="name" />
      <PolarRadiusAxis angle={39} domain={[0, 100]} stroke="#919191" />
      <Radar
        dataKey="average"
        stroke="#746fd6"
        fill="#8884d8"
        fillOpacity={0.6}
      />
    </RadarChart>
  );
};
