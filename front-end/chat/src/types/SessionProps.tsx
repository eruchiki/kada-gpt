import * as React from "react";

type SessionUser = {
  name?: string | null | undefined,
  email?: string | null | undefined,
  image?: string | null | undefined,
  } 
type SessionPropsType = {
  SessionUser: SessionUser |undefined
};
export default SessionPropsType;
