import { Select, MenuItem } from "@mui/material";
import React from "react";
import SelectPropsType from "../types/SelectProps";

const SelectForm = (props: SelectPropsType) => {
  return (
    <Select
      defaultValue={props.data}
      label={props.label}
      onChange={(e) => props.setData(e.target.value)}
    >
    {props.DataList.map((data) => (
      <MenuItem key={data.name} value={data.id}>{data.name}</MenuItem>
    ))}
    </Select>
  );
};

export default SelectForm;
