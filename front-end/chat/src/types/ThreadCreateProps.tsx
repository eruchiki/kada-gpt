import ThreadInfoPropsType from "./ThreadInfoProps";
import * as React from "react";

type CreateThreadInfoPropsType = {
  name: string;
  model_name: string;
  relate_num: number;
  collections_id: number;
  search_method: string;
  create_user_id: number;
  group_id: number;
};
type ThreadCreatePropsType = {
  ThreadInfo: CreateThreadInfoPropsType;
};

export default ThreadCreatePropsType;