import * as React from "react";

type TextFormPropsType = {
  setData: React.Dispatch<React.SetStateAction<string>>;
  data: string;
  title: string;
};

export default TextFormPropsType;
