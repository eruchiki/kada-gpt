import * as React from "react";

type SelectPropsType = {
  setData: React.Dispatch<React.SetStateAction<any>>;
  data: any;
  DataList: Array<any>;
  label: string;
};

export default SelectPropsType;
