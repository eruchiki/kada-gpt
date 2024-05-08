import * as React from "react";
import ThreadsPropsType from "./ThreadProps";

type SessionUser = {
  name?: string | null | undefined;
  email?: string | null | undefined;
  image?: string | null | undefined;
  id?: string | null | undefined;
};


type HeaderPropsType = {
  SessionUser: SessionUser | undefined;
  ThreadList: ThreadsPropsType[] | any[];
  PopUpData:{GroupId:number,CollectionList:any} | null
};
export default HeaderPropsType;
