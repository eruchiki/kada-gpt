import * as React from "react";


type ChatHisotryPropsType = {
  id: number;
  message_text: string;
  response_text: string;
  referances: string[];
  created_at: string;
  update_at: string;
  relate_num: number;
  search_method: string;
  model_name: string;
};


export default ChatHisotryPropsType;
