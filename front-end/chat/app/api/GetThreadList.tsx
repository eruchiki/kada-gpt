import axios from "axios";

const GetThreadList = (userid: string) => {
  const url = `${process.env.HOST_URL}/chat/${userid}/thread`;
  const threadlist = axios.get(url);
  return threadlist;
};

export default GetThreadList;
