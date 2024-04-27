import axios from "axios";

const GetUser = async (userid: string) => {
  const url = `${process.env.API_URL}/chat/users/${userid}`;
  const userlist = await axios.get(url);
  console.log(userlist)
  return userlist.data.result
}
export default GetUser;
