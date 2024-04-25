import axios from "axios";

const GetUser = async (userid:string) => {
  const url = `${process.env.HOST_URL}/users/${userid}`;
  const userlist = axios.post(url);
  return (await userlist).data;
};

export default GetUser;
