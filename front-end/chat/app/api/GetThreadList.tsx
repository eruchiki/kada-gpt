import axios from "axios";

const GetThreadList = (userid: string) => {
  const url = `/${userid}/thread`;
  const threadlist = axios.post(url);
  return threadlist;
};

export default GetThreadList;
