import { Select, MenuItem, InputLabel, Container, FormHelperText, FormControl } from "@mui/material";
import { useState } from "react";
import SelectPropsType from "../types/SelectProps";

const SelectForm = (props: SelectPropsType) => {
  const [selectError, setSelectError] = useState<string>();
  return (
    <FormControl error={!!selectError} sx={{ minWidth: 500 }}>
      <InputLabel id={props.label}>{props.label}</InputLabel>
      <Select
        defaultValue={props.data}
        id={props.label}
        label={props.label}
        onChange={(e) => props.setData(e.target.value)}
      >
      {props.DataList.map((data) => (
        <MenuItem key={data.name} value={data.id}>{data.name}</MenuItem>
      ))}
      </Select>
      {!!selectError && <FormHelperText>{selectError}</FormHelperText>}
    </FormControl >
  );
};

export default SelectForm;
